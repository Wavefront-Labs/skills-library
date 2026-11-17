---
id: computing-software.game-programming.game-engine-architecture.ecs-world-queries-and-spawning
name: ecs-world-queries-and-spawning
category: computing-software
field: game-programming
product: game-engine-architecture
tags: [game-engine-architecture, entity-component-system, ecs, world-queries, command-buffer, structural-changes, entt, flecs, prefab-instantiation, game-programming]
level: advanced
status: draft
description: "Use an ECS world day to day: spawning from prefabs, queries with filters, deferring structural changes with command buffers, and iteration safety (EnTT/flecs)."
sources: ["https://github.com/skypjack/entt/wiki/Crash-Course:-entity-component-system", "https://www.flecs.dev/flecs/md_docs_2Queries.html", "https://www.flecs.dev/flecs/md_docs_2PrefabsManual.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# ECS world queries and spawning

**Goal:** create, query and destroy entities in an ECS without invalidating iterations or losing
performance.

## Spawning
EnTT:
```cpp
entt::registry reg;
auto e = reg.create();
reg.emplace<Position>(e, 0.f, 0.f);
reg.emplace<Velocity>(e, 1.f, 0.f);
reg.emplace<Enemy>(e);              // empty tag component
```
flecs with prefabs (shared defaults, instances inherit or copy components):
```cpp
flecs::world w;
auto Goblin = w.prefab("Goblin").set<Health>({20}).set<Speed>({3.f});
auto g = w.entity().is_a(Goblin).set<Position>({5, 0});   // instance overrides position
```

## Queries
EnTT views (fast, no caching) and groups (owned storage reordering for max speed):
```cpp
for (auto [e, pos, vel] : reg.view<Position, const Velocity>(entt::exclude<Frozen>).each())
    pos.x += vel.dx * dt;
```
flecs cached queries/systems:
```cpp
w.system<Position, const Velocity>("Move").without<Frozen>()
 .each([](Position& p, const Velocity& v) { p.x += v.dx; });
```
Filters: required (with), excluded (without), optional components, tags, relationships (flecs:
`ChildOf`, custom pairs). Iterate the smallest component set first (EnTT views pick the smallest pool
automatically).

## Structural changes during iteration
Adding/removing components or creating/destroying entities moves data between archetypes (flecs,
Unity Entities) or reorders pools (EnTT groups): doing it while iterating can skip or double-visit
entities or invalidate references.
- Defer: record changes in a **command buffer** and apply after the loop (flecs defers automatically
  inside systems; Unity uses `EntityCommandBuffer`; EnTT: collect entities then act, or use
  `registry.destroy(view.begin(), view.end())` patterns documented as safe).
- EnTT specifically allows destroying/removing the *current* entity during view iteration, but not
  adding components to the iterated pools; check the library's rules.
- Prefer tag toggles/enableable components over add/remove for frequent state flips.

## Lifetimes and references
Store entity ids, check validity before use (`reg.valid(e)`, `e.is_alive()`); ids are versioned
(see game-engine-architecture generational-handles). Destroy related entities via relationships
(flecs `ChildOf` cascades) or explicit cleanup systems.

## Verify
- [ ] Spawning/destroying during systems never crashes or skips entities (stress test with random churn).
- [ ] Hot queries iterate contiguous data (profile cache misses / time per entity).
- [ ] No stale entity ids used after destruction (validity checks or asserts).
