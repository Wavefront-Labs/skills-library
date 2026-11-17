---
id: computing-software.game-programming.unity.raycastcommand-batched-queries
name: raycastcommand-batched-queries
category: computing-software
field: game-programming
product: unity
tags: [unity, unity-physics, raycastcommand, spherecastcommand, batched-queries, job-system, physics-queries, game-programming]
level: advanced
status: docs-checked
description: "Batch hundreds of Unity physics raycasts with RaycastCommand and ScheduleBatch in the job system: setup, QueryParameters, multi-hit results and when it pays off."
sources: ["https://docs.unity3d.com/ScriptReference/RaycastCommand.html", "https://docs.unity3d.com/ScriptReference/RaycastCommand.ScheduleBatch.html", "https://docs.unity3d.com/ScriptReference/QueryParameters.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Batched queries with RaycastCommand

**Goal:** run many raycasts (AI line of sight, wheel probes, bullets) asynchronously and in parallel in one batch.

```csharp
using Unity.Collections; using Unity.Jobs; using UnityEngine;

var cmds = new NativeArray<RaycastCommand>(n, Allocator.TempJob);
var hits = new NativeArray<RaycastHit>(n * maxHits, Allocator.TempJob);
var qp = new QueryParameters(losMask, false, QueryTriggerInteraction.Ignore, false);
for (int i = 0; i < n; i++)
    cmds[i] = new RaycastCommand(origins[i], dirs[i], qp, distances[i]);

JobHandle h = RaycastCommand.ScheduleBatch(cmds, hits, 32, maxHits);
// ... other main-thread work ...
h.Complete();
for (int i = 0; i < n; i++) {
    RaycastHit first = hits[i * maxHits];
    bool blocked = first.collider != null;
}
cmds.Dispose(); hits.Dispose();
```

## Facts that bite
- The results buffer cannot be read until the job has completed.
- The result for the command at index N starts at index `N * maxHits` of the results buffer.
- If `maxHits` exceeds the real number of hits, the remaining slots are invalid. The first invalid result has a null collider; later invalid slots are not written to, so their colliders are not guaranteed to be null. Stop the loop at the first invalid result.
- `ScheduleBatch(commands, results, minCommandsPerJob, maxHits, dependsOn)`: `minCommandsPerJob` is the minimum number of commands performed in one job, `maxHits` the maximum number of colliders a ray can hit, and `dependsOn` a `JobHandle` that must finish first (for example a job that fills the commands). There is also an overload without `maxHits`.
- `QueryParameters` holds `layerMask`, `hitTriggers`, `hitBackfaces` and `hitMultipleFaces`; `QueryParameters.Default` gives defaults. Only `RaycastCommand` supports hitting multiple mesh faces; with `hitMultipleFaces` set, size `maxHits` and the results array to hold all hits. Solid shapes (sphere, capsule, box, convex) return at most one result.
- `QueryParameters` is shared with `BoxcastCommand`, `CapsulecastCommand` and `SpherecastCommand`.
- Only `BatchQuery.ExecuteRaycastJob` is logged in the Profiler; query count information is not logged.
- Compare with `Physics.Raycast` and `Physics.RaycastAll` for the single-query equivalents.

## Checked
Method: 2026-11-09 docs-only read of the RaycastCommand, RaycastCommand.ScheduleBatch (signature and parameters) and QueryParameters script reference pages. Removed unconfirmed claims: multi-hit ordering, Physics.SyncTransforms advice, other command types beyond the three listed on the QueryParameters page, the payoff threshold, `colliderInstanceID` test (replaced by the documented null collider), and the Verify list.
