---
id: computing-software.game-programming.game-engine-architecture.update-method-ordering-and-phases
name: update-method-ordering-and-phases
category: computing-software
field: game-programming
product: game-engine-architecture
tags: [game-engine-architecture, game-programming-patterns, update-method, tick-groups, update-order, frame-phases, script-execution-order, game-programming]
level: practitioner
status: draft
description: "Apply the Update Method pattern safely: per-object update, explicit frame phases and tick groups, order dependencies, adding/removing objects mid-update and one-frame-lag bugs."
sources: ["https://gameprogrammingpatterns.com/update-method.html", "https://dev.epicgames.com/documentation/en-us/unreal-engine/actor-ticking-in-unreal-engine", "https://docs.unity3d.com/Manual/execution-order.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Update method ordering and phases

**Goal:** many objects each simulate one frame of behaviour via `update(dt)` (Nystrom, GPP "Update
Method"), with an order that is explicit rather than accidental.

## The pattern and its traps
```cpp
for (size_t i = 0; i < entities.size(); ++i) entities[i]->update(dt);
```
- **Order dependence:** A reads B's position; if B updates after A, A sees last frame's value.
  Sometimes fine; for parent/child, camera-follow and attachments it causes one-frame lag/jitter.
- **Spawning during update:** append to the list; iterate with an index bound captured at start
  (`n = size()` before the loop) so newborns start next frame, or push to a pending list.
- **Removing during update:** never erase in place. Mark dead and compact after the loop (or
  swap-and-pop with index adjustment if order does not matter).
- Inactive objects: keep them out of the list rather than `if (!active) return;` for thousands.

## Phases instead of one big loop
Split the frame into named phases and assign each system/component to one:
`Input -> PrePhysics (gameplay intent) -> Physics -> PostPhysics (react to contacts, ragdoll sync)
-> Animation -> PostAnimation (IK, attachments) -> Camera -> UI -> Render submit`.
Within a phase, declare dependencies (system B after system A) rather than relying on registration
order. ECS engines express this as system groups with `UpdateBefore/After` attributes.

## Engine mapping
- **Unreal tick groups:** `TG_PrePhysics`, `TG_DuringPhysics`, `TG_PostPhysics`, `TG_PostUpdateWork`;
  `AddTickPrerequisiteActor/Component` for explicit dependencies; `TickInterval` for slow updaters.
- **Unity:** `Update`, `LateUpdate` (cameras, follow), `FixedUpdate`; `[DefaultExecutionOrder(n)]`
  or Script Execution Order settings for the few that must run first; Entities `UpdateInGroup`.
- **Godot:** `_process`/`_physics_process` order follows the tree; `process_priority` and
  `process_physics_priority` reorder (lower runs first).

## Variable update frequency
Not everything needs every frame: AI perception at 5-10 Hz, far-away actors throttled (significance
manager / LOD for ticking), staggered across frames by `id % N` so cost spreads evenly.

## Verify
- [ ] A camera following a physics object shows no jitter (camera runs after physics and animation).
- [ ] Spawning and destroying 1,000 objects in one update pass neither crashes nor skips others.
- [ ] Dependency graph or tick-group assignment is documented and asserted (cycle detection).
