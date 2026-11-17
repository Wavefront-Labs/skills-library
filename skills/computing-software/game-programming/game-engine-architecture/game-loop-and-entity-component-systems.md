---
id: computing-software.game-programming.game-engine-architecture.game-loop-and-entity-component-systems
name: game-loop-and-entity-component-systems
category: computing-software
field: game-programming
product: game-engine-architecture
tags: [game-engine-architecture, game-loop, main-loop, entity-component-system, ecs, archetype, sparse-set, data-oriented-design, dod, cache-locality, struct-of-arrays, soa, aos, memory-allocators, arena-allocator, frame-allocator, pool-allocator, job-system, entt, flecs, unity-dots, bevy, frame-budget]
level: advanced
status: draft
description: "Structure an engine's core: the frame loop and update phases, ECS storage (archetypes vs sparse sets), data-oriented layout for cache, and frame/pool allocators."
sources: ["https://gameprogrammingpatterns.com/game-loop.html", "Gregory, Game Engine Architecture (3rd ed.)", "https://github.com/skypjack/entt", "https://www.flecs.dev/flecs/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Game loop and entity-component systems

**Goal:** an engine core whose frame is predictable and profileable, whose game objects
are composed rather than inherited, and whose hot loops are laid out for the CPU cache.

## 1. The frame
A typical single-threaded frame, in order:
```
poll OS events / input
fixed-step simulation (0..n steps, accumulator — see game-physics fixed-timestep skill)
variable-step update (gameplay, AI, animation)
late update (camera, attachments)
build render lists → submit to GPU (often on a render thread, one frame behind)
audio update
end-of-frame: deferred destruction, reset frame allocator, present
```
- Budget: 16.67 ms at 60 fps, 8.33 ms at 120. Instrument each phase (Tracy, Superluminal,
  Unreal Insights, Unity Profiler) from day one.
- **Defer structural changes** (spawn/destroy/add component) to a sync point; mutating
  containers while iterating them is a top source of engine crashes.
- Multi-threading: a job system (worker threads pulling small tasks, dependencies as a
  graph) beats one thread per subsystem; the main thread mostly schedules.

## 2. Why components, not inheritance
Deep hierarchies (`Actor → Pawn → Enemy → FlyingEnemy → FlyingShootingEnemy`) collapse
when a design needs a flying *non*-enemy that shoots. Composition: an entity is an ID;
data lives in components (`Transform`, `Velocity`, `Health`, `Flying`); behaviour lives in
**systems** that iterate entities having a given set of components.

## 3. ECS storage — the two main designs
| | Archetype (Unity DOTS, Flecs, Bevy) | Sparse set (EnTT) |
|---|---|---|
| Layout | Entities with the *same component set* share tables; each component is a contiguous column | One packed array per component type + sparse index by entity ID |
| Iterating many components | Very fast: all columns aligned | Fast for one type; joins iterate the smallest set and look up others |
| Add/remove component | Moves the entity to another table (cost) | Cheap: insert/erase in one array |
| Good for | Stable compositions, huge counts | Frequently toggled components (tags/states) |

Minimal system shape (EnTT):
```cpp
void movement(entt::registry& reg, float dt) {
    auto view = reg.view<Position, const Velocity>();
    for (auto [e, p, v] : view.each()) { p.x += v.x * dt; p.y += v.y * dt; }
}
```
Rules of thumb: components are plain data (no virtuals, no pointers to other entities —
store entity IDs and check validity, since IDs carry a generation/version to detect reuse);
systems are where logic lives; keep components small and split hot from cold fields.

## 4. Data-oriented design in one paragraph
A cache miss to main memory costs on the order of 100+ cycles; arithmetic is nearly free
by comparison. So lay out data by **how it's iterated**: struct-of-arrays (`x[], y[], z[]`)
for loops touching one or two fields across thousands of items; array-of-structs when you
always use the whole struct. Process in batches, avoid pointer chasing (linked lists,
`std::vector<Base*>` of heap objects with virtual `update()`), and remove branches from hot
loops by sorting items into separate arrays by type/state. Measure with a profiler that
shows cache misses (VTune, perf, AMD uProf).

## 5. Memory
- Avoid general `malloc/new` in the frame: they're slow, lock, and fragment.
- **Frame (linear/arena) allocator:** bump a pointer; reset the whole thing at end of
  frame. Perfect for temporary per-frame data.
- **Pool allocator:** fixed-size blocks with a free list for particles, bullets, components.
- **Double-buffered frame allocator** when data must survive into the next frame (render thread).
- Track allocations per subsystem with tags so budgets are visible.

## Gotchas
- An ECS doesn't fix a bad design by itself; tiny toy demos hide the cost of structural
  changes and cross-entity queries (e.g. "nearest enemy" needs a spatial index, not a scan).
- Order of systems is behaviour. Make it explicit (a schedule), not registration order.
- Pointers/references into component arrays are invalidated when the array grows.

## Verify
- [ ] Frame phases are instrumented; you can name the most expensive one.
- [ ] No spawn/destroy during iteration — all deferred to a sync point.
- [ ] Hot systems iterate contiguous arrays (check with a profiler, not by assumption).
- [ ] Zero general-heap allocations per frame in steady state.
- [ ] Entity references are generation-checked IDs, not raw pointers.
