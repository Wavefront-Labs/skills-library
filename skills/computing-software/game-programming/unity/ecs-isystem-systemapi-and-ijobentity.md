---
id: computing-software.game-programming.unity.ecs-isystem-systemapi-and-ijobentity
name: ecs-isystem-systemapi-and-ijobentity
category: computing-software
field: game-programming
product: unity
tags: [unity, dots, unity-dots, isystem, ijobentity, systemapi, entityquery, entitycommandbuffer, burst, refrw, entities, game-programming]
level: advanced
status: docs-checked
description: "Unity Entities 1.3: ISystem callbacks and order, IJobEntity Execute parameters, query attributes and scheduling, and EntityCommandBuffer temporary entities and job safety."
sources: ["https://docs.unity3d.com/Packages/com.unity.entities@1.3/manual/systems-isystem.html", "https://docs.unity3d.com/Packages/com.unity.entities@1.3/manual/iterating-data-ijobentity.html", "https://docs.unity3d.com/Packages/com.unity.entities@1.3/manual/systems-entity-command-buffers.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ECS systems: ISystem, IJobEntity and command buffers

**Goal:** write unmanaged systems that schedule jobs and defer structural changes (Entities 1.3 manual).

## ISystem
- Implement `ISystem` for an unmanaged system. Required methods (can be Burst compiled): `OnCreate`,
  `OnUpdate`, `OnDestroy`, each taking `ref SystemState` (access to `World`, `WorldUnmanaged`,
  `EntityManager`). There is no base class, unlike `SystemBase`.
- Optional `ISystemStartStop`: `OnStartRunning` (before the first `OnUpdate`, and when a system resumes
  after being stopped or disabled) and `OnStopRunning` (when disabled or no entities match the system's
  required components).
- Order: `OnCreate`, `OnStartRunning`, `OnUpdate` (every frame while the system has work, see
  `ShouldRunSystem`), `OnStopRunning` (also before `OnDestroy`; triggered when nothing matches
  `RequireForUpdate` or `Enabled` is false), `OnDestroy`. Without `RequireForUpdate` the system runs
  continuously unless disabled or destroyed. A parent system group's `OnUpdate` triggers its systems.
- All system events run on the main thread. Best practice: use `OnUpdate` to schedule jobs for most of
  the work, via `IJobEntity` (reusable across systems) or `IJobChunk` (per archetype chunk).

## IJobEntity
- A struct with the `partial` keyword (source generation creates an `IJobChunk` struct in
  `project/Temp/GeneratedCode`) and your own `Execute` method. Works identically with `SystemBase` and
  `ISystem`. Example from the page: `void Execute(ref SampleComponent sample) { sample.Value += 1f; }`
  scheduled with `new ASampleJob().ScheduleParallel();`.
- Query: built automatically from the `Execute` parameters, or pass your own, e.g.
  `ScheduleParallel(query)`.
- Job-struct attributes: `WithAll`, `WithAny`, `WithNone`, `WithChangeFilter` (also on an Execute
  argument), `WithOptions`. `[EntityIndexInQuery]` goes on an `int` parameter. Job attributes such as
  `BurstCompile`, `DeallocateOnJobCompletion`, `NativeDisableParallelForRestriction` also work.
- Execute parameters: `IComponentData` and `ICleanupComponentData` (`ref` read-write, `in` read-only);
  shared component (`in`; managed ones cannot be Burst compiled or scheduled, use `.Run`); managed
  components (value copy or `in`; `ref` is an error; use `.Run`); `Entity` (value copy only);
  `DynamicBuffer<T>` (`ref` or `in`); `IAspect`; and `int` with `[ChunkIndexInQuery]`,
  `[EntityIndexInChunk]` or `[EntityIndexInQuery]`. Adding `EntityIndexInChunk` and `ChunkIndexInQuery`
  gives a unique identifier per entity. `EntityIndexInQuery` calls
  `EntityQuery.CalculateBaseEntityIndexArray[Async]`, which negatively affects performance.
- Page recommends IJobEntity over `Entities.ForEach` where possible (reusable across systems, much
  shorter compile time).

## EntityCommandBuffer (ECB)
- Stores a queue of thread-safe commands for playback later: schedule structural changes from jobs and
  apply on the main thread after jobs complete; also usable on the main thread to delay changes or play a
  set of changes back multiple times. Methods mirror `EntityManager` (`CreateEntity(EntityArchetype)`,
  `DestroyEntity`, `SetComponent<T>`, `AddComponent<T>`, `RemoveComponent<T>(EntityQuery)`).
- Entities from `CreateEntity()`/`Instantiate()` are temporary until playback: usable by later commands in
  the same buffer and inside unmanaged component values (including dynamic buffer entity fields). Passing
  one to an `EntityManager` method, or into a different command buffer, throws. After playback you cannot
  tell which real entity corresponds to a temporary one.
- The job safety handle exists only in the Editor, not in player builds. It throws if you use the ECB
  (`AddComponent`, `Playback`, `Dispose`...) while a scheduled job using it is incomplete, or schedule
  another job on it that does not depend on the first.
- Best practice: a separate ECB per distinct job, since consecutive jobs may use overlapping sort keys
  (for example both using `ChunkIndexInQuery`) and their commands may interleave.

## Checked
Date: 2026-11-07

Read in full: the ISystem overview, the IJobEntity page including all its examples, and the Entity
command buffer overview. The page linked "Use an entity command buffer" and "playback" pages,
`SystemAPI.Query`, `RefRW`/`RefRO` and system group pages were not opened.

Removed because the three pages do not confirm it: the `SystemAPI.Query` foreach sample and `RefRW`
`ValueRW` usage, `[BurstCompile]` on the system, `SystemAPI.Time` and `GetSingleton`, the
`EndSimulationEntityCommandBufferSystem.Singleton` / `AsParallelWriter` recipe, the ExpireJob sample,
"enableable components instead of add/remove", `[UpdateInGroup]`/`[UpdateBefore]`/`[UpdateAfter]`,
`FixedStepSimulationSystemGroup`, `PhysicsSystemGroup`, `ComponentLookup` with
`[NativeDisableParallelForRestriction]` guidance, "state.Dependency chaining" and the Verify list
(Systems window, Profiler, Burst Inspector).

Method: documentation only; no commands were run.
