---
id: computing-software.game-programming.game-engine-architecture.frustum-and-occlusion-culling
name: frustum-and-occlusion-culling
category: computing-software
field: game-programming
product: game-engine-architecture
tags: [game-engine-architecture, rendering-engine, frustum-culling, occlusion-culling, visibility, hi-z, portals, pvs, gpu-driven-culling, bounding-spheres, game-programming]
level: advanced
status: draft
description: "Cull invisible objects before rendering: frustum plane tests on bounds, SIMD batch culling, occlusion via Hi-Z, software rasterized occluders, portals/PVS, and measuring wins."
sources: ["https://www.gameenginebook.com/", "https://www.realtimerendering.com/", "https://advances.realtimerendering.com/s2015/aaltonenhaar_siggraph2015_combined_final_footer_220dpi.pdf"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Frustum and occlusion culling

**Goal:** submit only what can be seen, so CPU submission and GPU vertex work scale with visible
objects, not with level size (Gregory GEA ch. 11.2.7; Real-Time Rendering ch. 19).

## Frustum culling
Extract the 6 planes from the view-projection matrix (Gribb/Hartmann method), normalise them, test
each object's bounding sphere or AABB:
```cpp
bool sphereInFrustum(const Plane planes[6], Vec3 c, float r) {
    for (int i = 0; i < 6; ++i)
        if (dot(planes[i].n, c) + planes[i].d < -r) return false;   // fully outside one plane
    return true;                                                     // inside or intersecting
}
// AABB: test the "positive vertex" (corner farthest along the plane normal) against each plane.
```
- Data-oriented: store bounds for all objects in contiguous SoA arrays (centers x/y/z, radii) and test
  4/8 at a time with SIMD; tens of thousands of objects in well under a millisecond.
- Hierarchical: test BVH/octree nodes first; a fully inside node skips its children's tests; fully
  outside rejects the subtree.
- Shadow cascades and reflection probes need their own frustum culls.

## Occlusion culling
Objects inside the frustum but hidden behind others.
| Technique | Notes |
|---|---|
| **Precomputed PVS** (cells -> visible set) | Static levels; baked (Umbra in Unity/older Unreal). Cheap at runtime, no dynamic occluders. |
| **Portals and cells** | Indoor levels; clip frustum through doorway portals. |
| **Software occlusion** | Rasterize a few big low-poly occluders to a small depth buffer on CPU (Intel Masked Occlusion Culling), test object bounds against it. |
| **Hardware occlusion queries** | Results arrive a frame or more later; use with conservative fallbacks; avoid stalls. |
| **Hi-Z / GPU-driven** | Build a depth pyramid from last frame's (or this frame's early) depth; compute shader tests bounds against it and writes indirect draw args. Two-pass: draw last frame's visible set, build Hi-Z, test the rest. Modern engines (Nanite-era) do this per cluster. |

## Practical rules
- Use the cheapest test that removes most work; measure object counts before/after each stage.
- Small objects at distance: combine with LOD and distance culling (per-object max draw distance).
- Avoid popping: conservative bounds, and a one-frame latency tolerance with Hi-Z from last frame
  plus reprojection.
- Engines: Unity camera Occlusion Culling (baked Umbra) + per-layer cull distances; Unreal
  hardware occlusion queries/HZB occlusion and precomputed visibility volumes; Godot occluder
  instances (Embree-based software raster) for 3D.

## Verify
- [ ] Debug counter of submitted vs total objects per view; frozen-camera visualization of culled objects.
- [ ] CPU culling time per frame within budget (e.g. < 0.5 ms for 50k objects).
- [ ] No visible popping when turning quickly or emerging from behind occluders.
