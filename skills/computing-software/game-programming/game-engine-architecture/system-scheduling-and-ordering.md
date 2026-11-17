---
id: computing-software.game-programming.game-engine-architecture.system-scheduling-and-ordering
name: system-scheduling-and-ordering
category: computing-software
field: game-programming
product: game-engine-architecture
tags: [game-engine-architecture, system-scheduling, ecs, update-order, game-programming]
level: practitioner
status: draft
description: "Schedule ECS systems: explicit ordering constraints, read/write sets for parallel execution, sync points, fixed vs variable groups and debugging order bugs."
sources: ["https://bevy-cheatbook.github.io/programming/schedules.html", "https://docs.unity3d.com/Packages/com.unity.entities@1.3/manual/systems-update-order.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# System scheduling and ordering

**Goal:** systems run in a correct, explicit order and in parallel where safe.

## Ordering constraints
Declare dependencies instead of relying on registration order:
- Unity Entities: `[UpdateInGroup(typeof(SimulationSystemGroup))]`,
  `[UpdateBefore(typeof(TransformSystemGroup))]`, `[UpdateAfter(...)]`.
- Bevy: `app.add_systems(Update, (input, movement.after(input), collision.after(movement)))`,
  system sets with `configure_sets` and `chain()`.
- flecs: pipeline phases (`OnLoad`, `PreUpdate`, `OnUpdate`, `OnValidate`, `PostUpdate`, `PreStore`, `OnStore`).

Group into phases (input -> simulation -> physics -> late update -> presentation) and order within
phases only where a real data dependency exists.

## Parallelism from access sets
Each system declares component reads/writes. The scheduler runs systems concurrently when write
sets don't overlap others' read or write sets. Bevy derives this from query types (`&T` vs `&mut T`);
Unity's job dependencies come from `ComponentLookup` and query read/write declarations.

## Sync points
Structural changes (command buffers) and main-thread-only work force sync points; minimise and
batch them (Unity: one ECB system per group end).

## Fixed vs variable
Physics and gameplay simulation in a fixed-timestep group (may run 0..N times per frame); rendering
prep once per frame. Systems reading simulation output for rendering must interpolate.

## Debugging order bugs
- One-frame lag symptoms (camera trailing by a frame) usually mean a reader runs before the writer.
- Dump the resolved schedule at startup (Bevy schedule graph via `bevy_mod_debugdump`, Unity
  Systems window) and check ambiguities: Bevy can report systems with conflicting access and no
  ordering (`ambiguity_detection`).

## Verify
- Ambiguity detection reports zero unresolved conflicts; profiler shows expected parallel lanes.
