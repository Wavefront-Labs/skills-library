---
id: computing-software.game-programming.unity.ecs-component-types-and-dynamic-buffers
name: ecs-component-types-and-dynamic-buffers
category: computing-software
field: game-programming
product: unity
tags: [unity, unity-dots, ecs-component-types, dynamicbuffer, enableable-components, game-programming]
level: practitioner
status: draft
description: "Pick the right Unity Entities component type: IComponentData, tags, IBufferElementData, shared, cleanup, enableable and managed components, with archetype cost trade-offs."
sources: ["https://docs.unity3d.com/Packages/com.unity.entities@1.3/manual/components-type.html", "https://docs.unity3d.com/Packages/com.unity.entities@1.3/manual/components-buffer.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Entities component types and dynamic buffers

**Goal:** model data so queries are fast and structural changes rare.

## Types
| Type | Use | Notes |
|---|---|---|
| `IComponentData` (unmanaged struct) | per-entity data | default; chunk-stored, Burst-friendly |
| Tag (empty struct) | filtering | zero size, adding/removing = structural change |
| `IEnableableComponent` | toggling state | `SetComponentEnabled` without moving chunks; queries skip disabled |
| `IBufferElementData` + `DynamicBuffer<T>` | per-entity arrays | `[InternalBufferCapacity(n)]` inline, spills to heap |
| `ISharedComponentData` | grouping by value | changing value moves entity to another chunk; use for render mesh, team id |
| `ICleanupComponentData` | teardown | survives entity destruction until removed by a system |
| managed `class : IComponentData` | references | no Burst, no jobs; avoid in hot paths |
| Singleton | one-off data | `SystemAPI.GetSingleton<T>()` |

## Dynamic buffers
```csharp
[InternalBufferCapacity(8)]
public struct Waypoint : IBufferElementData { public float3 Value; }
// baking:
var buf = AddBuffer<Waypoint>(entity); buf.Add(new Waypoint { Value = p });
// system:
foreach (var (wps, xf) in SystemAPI.Query<DynamicBuffer<Waypoint>, RefRW<LocalTransform>>()) { ... }
```
- Capacity reserved inline even if empty: big capacities bloat chunks (fewer entities per chunk). Use
  0 for rarely-used large buffers.
- Structural changes invalidate `DynamicBuffer` handles; re-fetch after ECB playback.
- `BufferLookup<T>` for random access in jobs (`[ReadOnly]` if not writing).

## State modelling
- Frequently toggled state -> enableable component (no chunk move).
- Rare state changes (dead, spawned) -> tag via ECB is fine.
- Avoid per-frame Add/Remove of components on many entities.

## Gotchas
- Chunk is 16 KB; huge components reduce entities per chunk and cache efficiency.
- Shared component with many distinct values fragments chunks (one value per chunk).
- Enableable components still occupy memory and are iterated via bitmask checks.

## Verify
- [ ] Entities > Archetypes window: entities-per-chunk reasonable, no unexpected archetype explosion.
- [ ] Profiler: no structural-change spikes in steady state.
