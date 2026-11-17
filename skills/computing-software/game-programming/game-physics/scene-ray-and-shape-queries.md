---
id: computing-software.game-programming.game-physics.scene-ray-and-shape-queries
name: scene-ray-and-shape-queries
category: computing-software
field: game-programming
product: game-physics
tags: [game-physics, raycast-query, scene-queries, overlap-query, game-programming]
level: practitioner
status: verified
description: "Use physics scene queries well: raycast, sweep and overlap APIs, closest vs any vs all hits, filtering, batching and initial-overlap gotchas."
sources: ["https://nvidia-omniverse.github.io/PhysX/physx/5.4.1/docs/SceneQueries.html", "https://github.com/jrouwe/JoltPhysics", "https://docs.unity3d.com/ScriptReference/Physics.SphereCast.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Ray and shape queries against a scene

**Goal:** answer gameplay questions (line of sight, ground under feet, what is in this explosion)
correctly and cheaply.

## Query kinds
- **Raycast:** origin, unit direction, max distance. Modes: closest hit, any hit (fast early-out
  for occlusion/LOS; PhysX `eANY_HIT` reports the first hit found, which may not be the closest), all hits (PhysX touch buffers hold hits no farther than the blocking hit;
  the docs state no ordering, so sort yourself).
- **Sweep (shape cast):** move a sphere/capsule/box along a ray; for character ground checks and
  thick bullets.
- **Overlap:** which shapes intersect a volume now; for explosions, triggers, spawn validation.

## Filtering
Use collision layers/filter data in the query, not post-filtering. PhysX: `PxQueryFilterData`
with `PxFilterData` word0..3 masks, `PxQueryFlag::eSTATIC | eDYNAMIC | ePREFILTER` (pre-filter runs before the exact tests; post-filter after); Jolt: `BroadPhaseLayerFilter`
+ `ObjectLayerFilter` + `BodyFilter` (+ `ShapeFilter`). Exclude the querying body itself (Godot: the `exclude` array of the query parameters).

## Gotchas
- **Initial overlap:** engines treat a sweep that starts inside geometry differently: PhysX reports an initial-overlap hit at distance 0 and, with `PxHitFlag::eMTD`,
  computes the minimum translation direction (distance becomes the negative penetration depth); Unity's `SphereCast` does not detect colliders it starts inside; Godot's `cast_motion` ignores shapes already colliding.
  Start sweeps slightly back.
- **Back faces:** triangle meshes are single sided: PhysX needs `PxHitFlag::eMESH_BOTH_SIDES`, Jolt `RayCastSettings::mBackFaceMode = CollideWithBackFaces`, to report back-face hits.
- **Stale data:** queries against the physics scene see the last simulated state; changed Transforms need a sync before querying (Unity `Physics.SyncTransforms` applies Transform changes to the physics engine).
- **Precision:** offset the origin by a small skin along the normal when chaining rays (bounces).

## Performance
- Use any-hit for visibility; it stops at the first hit.
- Batch queries per frame and run them on worker threads (Unity `RaycastCommand` runs raycasts asynchronously and in parallel as a job; PhysX has batched queries (`PxBatchQueryExt`) and a Threading chapter on reading while simulating).
- Limit max distance; infinite rays traverse the whole tree.

## Verify
- Debug-draw every query for one frame; count queries per frame against budget.

## Checked (2026-10-22)
- PhysX 5.4.1 SceneQueries page (fetched): closest-hit default, touch buffers (touches no farther than the block, no ordering stated), `eANY_HIT` ('first encountered hit, which may not be the closest'), pre/post filter, `PxBatchQueryExt`; `PxQueryFiltering.h`: `eSTATIC`, `eDYNAMIC`, `ePREFILTER`; `geometry/PxGeometryHit.h`: `eMESH_BOTH_SIDES`, `eMTD` ('distance negative if shapes overlap'); CharacterControllers page: eMTD and initial overlap.
- Jolt master: `BodyFilter.h`, `ObjectLayer.h`, `BroadPhaseLayer.h` filter classes, `NarrowPhaseQuery::CastShape`, `MeshShape.h` ('single sided', `mBackFaceMode`). Godot `PhysicsDirectSpaceState3D.xml` (`cast_motion` ignores already-colliding shapes) and ray-casting docs source (`exclude`). Unity ScriptReference: `SphereCast` note on overlapping colliders, `Physics.SyncTransforms`, `RaycastCommand`.
- Removed the claim that a PhysX initial-overlap normal is 'meaningless' (the docs say only eMTD is guaranteed to give an appropriate normal) and the 'thread-safe read locks' wording.
- Performance advice (limit max distance, any-hit for visibility) is general guidance consistent with the any-hit docs above.
