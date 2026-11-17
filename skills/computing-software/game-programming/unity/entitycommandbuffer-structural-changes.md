---
id: computing-software.game-programming.unity.entitycommandbuffer-structural-changes
name: entitycommandbuffer-structural-changes
category: computing-software
field: game-programming
product: unity
tags: [unity, unity-dots, ecb-playback, entitycommandbuffer, structural-changes, game-programming]
level: practitioner
status: docs-checked
description: "Record structural changes in Unity Entities with EntityCommandBuffer: system-provided ECB singletons, automatic playback, placeholder entities and one ECB per job."
sources: ["https://docs.unity3d.com/Packages/com.unity.entities@1.3/manual/systems-entity-command-buffers.html", "https://docs.unity3d.com/Packages/com.unity.entities@1.3/manual/systems-entity-command-buffer-automatic-playback.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# EntityCommandBuffer structural changes

**Goal:** schedule structural changes (create or destroy entities, add or remove components) from jobs, or delay them on
the main thread, using an entity command buffer (ECB) instead of changing entities mid-iteration.

## What an ECB is
An ECB stores a queue of thread-safe commands you add to and later play back. Its methods mirror `EntityManager`:
`CreateEntity(EntityArchetype)`, `DestroyEntity(Entity)`, `SetComponent<T>(Entity, T)`, `AddComponent<T>(Entity)`,
`RemoveComponent<T>(EntityQuery)`. Uses: schedule structural changes from jobs, change things on the main thread after
jobs complete, delay changes, or play back a set of changes more than once.

## System-provided ECBs (automatic playback)
Use an `EntityCommandBufferSystem` instead of playing back yourself:
1. Get the singleton of the ECB system that should do the playback.
2. Create an `EntityCommandBuffer` from it.
3. Record commands.

```csharp
var singleton = SystemAPI.GetSingleton<FooECBSystem.Singleton>();
EntityCommandBuffer ecb = singleton.CreateCommandBuffer(state.WorldUnmanaged);
new MyParallelRecordingJob() { ecbParallel = ecb.AsParallelWriter() }.Schedule();
```
(`FooECBSystem` is the doc's placeholder for a real ECB system; `GetSingleton` registers the job so the ECB system
completes it.)

Do not manually play back or dispose an ECB created through an `EntityCommandBufferSystem`. Each update, that system
completes all registered jobs and jobs scheduled against its singleton, plays back all its ECBs in the order they were
created, then disposes them.

Default systems in the default world: `BeginInitialization`, `EndInitialization`, `BeginFixedStepSimulation`,
`EndFixedStepSimulation`, `BeginVariableRateSimulation`, `EndVariableRateSimulation`, `BeginSimulation`,
`EndSimulation` and `BeginPresentation`, each with the suffix `EntityCommandBufferSystem`. There is no
`EndPresentationEntityCommandBufferSystem`: structural changes cannot happen in the frame after rendering data is handed
to the renderer, so use `BeginInitializationEntityCommandBufferSystem` (the end of one frame is the start of the next).
You can write your own `EntityCommandBufferSystem` subclass with `[UpdateInGroup]`/`[UpdateAfter]` and a `Singleton`
implementing `IECBSingleton`; the automatic-playback page has the full example.

## One ECB per job
Use a separate ECB for each distinct job. If consecutive jobs share an ECB they might use overlapping sort keys (for
example both using `ChunkIndexInQuery`) and their recorded commands might interleave.

## Placeholder (temporary) entities
`CreateEntity()` and `Instantiate()` only record commands. They return `Entity` values with negative indices that stand
for entities that do not exist yet. They are valid only in later commands of the same ECB:
- a later command in the same buffer can target one (for example `AddComponent<T>(e)`);
- component values (including `IBufferElementData` with entity fields) recorded in `AddComponent`, `SetComponent` or
  `SetBuffer` can reference one; playback remaps it to the real entity.

Passing a placeholder to an `EntityManager` method, or using it in a different ECB, throws an exception. After
playback there is no way to find which real entity a placeholder became.

## Manual ECB
`new EntityCommandBuffer(Allocator.TempJob)`, record, then `ecb.Playback(state.EntityManager);` and `ecb.Dispose();`
(as in the doc's example). This is the case where you play back and dispose yourself.

## Safety checks
The ECB has a job safety handle, available only in the Editor, not in player builds. It throws if you access the ECB
(`AddComponent`, `Playback`, `Dispose` and so on) while a scheduled job using it is incomplete, or schedule another job
that accesses the same ECB without depending on the earlier job.

## Checked
Date: 2026-11-07.
Read in full: "Entity command buffer overview" (command list, temporary entities, safety, one ECB per job note) and
"Automatic play back and disposal of entity command buffers" (steps, Important note, default ECB systems list,
no-EndPresentation reason, custom ECB system, deferred entities, both code blocks). Both pages are Entities 1.3.
Removed as unconfirmed by those pages: the `[ChunkIndexInQuery]`/`IJobEntity` sample and "deterministic sort key"
claim, "do not use thread index", the `EndInitialization` advice for spawns, the claims that large ECBs are slow or that
enableable components are preferable, "sync point" statements, the exception claims about destroyed entities or missing
components, and the invented Verify checklist. The linked pages "Use an entity command buffer" and "Entity command
buffer playback" were not opened.
Method: documentation only; no commands were run.
