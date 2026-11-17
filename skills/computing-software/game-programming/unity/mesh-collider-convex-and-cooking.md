---
id: computing-software.game-programming.unity.mesh-collider-convex-and-cooking
name: mesh-collider-convex-and-cooking
category: computing-software
field: game-programming
product: unity
tags: [unity, mesh-collider, physics, convex, cooking-options, colliders, game-programming]
level: practitioner
status: docs-checked
description: "Use Unity MeshCollider: Convex and its 255-triangle limit, cooking options, Read/Write requirement, and pre-baking meshes with Physics.BakeMesh (EntityId) on worker threads."
sources: ["https://docs.unity3d.com/Manual/class-MeshCollider.html", "https://docs.unity3d.com/ScriptReference/MeshColliderCookingOptions.html", "https://docs.unity3d.com/ScriptReference/Physics.BakeMesh.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MeshCollider convex and cooking

**Goal:** accurate collision for complex geometry without physics spikes. Unity 6000.x docs.

## Component facts
- A Mesh Collider builds a collider from a mesh asset; it can be more accurate than primitives for complex geometry, but
  for moving or dynamic objects primitive colliders can be more efficient (more stability, better-performing simulation).
- **Convex** mesh colliders can collide with other mesh colliders and are limited to 255 triangles.
- **Is Trigger**: other colliders pass through and trigger `OnTriggerEnter/Stay/Exit`.
- **Provides Contacts**: generates contact data at all times; resource-intensive, so off by default.
- **Mesh**: you must enable the mesh's Read/Write property to use it in the Mesh Collider. Project Auditor (Window >
  Analysis > Project Auditor), Game Objects view, can find such issues across the project.
- **Layer Overrides**: Layer Override Priority (higher value wins on conflict), Include Layers, Exclude Layers.

## Cooking options
`MeshColliderCookingOptions` is a `[Flags]` enum: `None`, `CookForFasterSimulation`, `EnableMeshCleaning`,
`WeldColocatedVertices`, `UseFastMidphase`. In the Inspector: None (off), Everything (the default; all enabled).
- **Cook for Faster Simulation**: preprocesses mesh data into memory to speed runtime calculations; off means faster
  cooking but slower data retrieval at runtime.
- **Enable Mesh Cleaning**: removes degenerate (collinear) triangles and other artifacts for more accurate contacts; off
  means faster cooking, less optimization.
- **Weld Colocated Vertices**: combines vertices at the same position; same trade-off.
- **Use Fast Midphase**: uses the fastest mid-phase structure for the output platform (no R-Trees); disable it if you hit
  midphase issues, and Unity uses the slower legacy algorithm.
- If Cooking Options differ from the default (everything enabled except None), the mesh must have `isReadable` true.

## Pre-baking with Physics.BakeMesh
Baking creates the spatial search acceleration structures a MeshCollider needs. Normally it happens when the component is
instantiated or when `sharedMesh` is set. It is resource-intensive, so you can pre-bake at a quiet moment or spread it
across cores. The mesh instance stores the baked data.
```csharp
// public static void BakeMesh(EntityId meshEntityId, bool convex, MeshColliderCookingOptions cookingOptions)
// public static void BakeMesh(EntityId meshEntityId, bool convex)   // default cooking options
Physics.BakeMesh(mesh.GetEntityId(), false, cookingOptions);
```
- The `int` instance-ID overloads are obsolete and removed; use the `EntityId` overloads (`mesh.GetEntityId()`).
- In the Player, BakeMesh requires Read/Write on the mesh; in the Editor it needs no extra setting.
- A MeshCollider reuses the baked mesh only if its `cookingOptions` exactly match those used to bake, its transform allows
  mesh sharing (scale not negative and not skewed; negative scale is fine only when not convex), and the mesh geometry has
  not changed since the bake.
- Adding a MeshCollider to a GameObject that already has a MeshFilter sets `sharedMesh` automatically and may re-bake.
- BakeMesh is thread-safe and computes on the calling thread, but never call it on the same mesh from several threads at
  once. The page's job example collects `NativeArray<EntityId>` ids on the main thread, runs an `IJobParallelFor` that
  calls `Physics.BakeMesh(meshIds[index], false)`, completes it, then creates the MeshCollider components on the main
  thread.

## Checked
Date: 2026-11-07.
Read in full: "Mesh collider component reference", `MeshColliderCookingOptions` and `Physics.BakeMesh` (6000.6 docs,
including both examples). The linked "Prepare a mesh for mesh colliders" page was not opened.
Corrected: the draft's BakeJob used `mesh.GetInstanceID()` with `NativeArray<int>`; the current page uses `EntityId` and
marks the `int` overloads as removed. The draft said "Use Fast Midphase: desktop-capable platforms"; the page says the
fastest algorithm available for the output platform.
Removed as unconfirmed: "non-convex only on static or kinematic" and the dynamic-Rigidbody error, non-convex-vs-non-convex
rules, triggers must be convex, hull simplification and bulging, compound collider and `_COL` mesh advice, the
tunnelling/CCD gotcha, scaling recook claim, and the invented Verify checklist.
Method: documentation only; no commands were run.
