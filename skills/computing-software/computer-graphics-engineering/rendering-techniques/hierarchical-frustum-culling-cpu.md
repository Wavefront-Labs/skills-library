---
id: computing-software.computer-graphics-engineering.rendering-techniques.hierarchical-frustum-culling-cpu
name: hierarchical-frustum-culling-cpu
category: computing-software
field: computer-graphics-engineering
product: rendering-techniques
tags: [computer-graphics-engineering, rendering-techniques, acceleration-lod, hierarchical-culling, frustum-culling, plane-masking, simd-culling, bvh, scene-graph]
level: practitioner
status: draft
description: "Cull efficiently on the CPU: sphere/AABB vs frustum plane tests, hierarchical culling with BVH/octree and plane masking, SIMD batch tests and temporal coherence."
sources: ["https://www.realtimerendering.com/", "https://fgiesen.wordpress.com/2010/10/17/view-frustum-culling/", "https://www.gamedevs.org/uploads/fast-extraction-viewing-frustum-planes-from-world-view-projection-matrix.pdf"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# CPU frustum culling and hierarchical culling

## 1. Extract planes
From the view-projection matrix (Gribb & Hartmann): rows combine to six planes:
```cpp
// row-major M (row i = M[i]); planes as (a,b,c,d), inside if dot(p, (x,y,z,1)) >= 0
left   = M[3] + M[0];  right  = M[3] - M[0];
bottom = M[3] + M[1];  top    = M[3] - M[1];
near   = M[2];         // D3D/Vulkan [0,1] depth; GL [-1,1]: M[3] + M[2]
far    = M[3] - M[2];
// normalise each plane by length(a,b,c)
```

## 2. Tests
- **Sphere**: outside if `dot(n, c) + d < -r` for any plane.
- **AABB** (centre c, half-extents e): effective radius per plane
  `r = e.x*|n.x| + e.y*|n.y| + e.z*|n.z|`; outside if `dot(n,c) + d < -r`; fully inside if
  `> r` for all planes.
- These are conservative (boxes near frustum corners pass); fine for culling.

## 3. Hierarchical culling
Over a BVH/octree/scene hierarchy:
- If a node is fully outside, skip its subtree.
- If fully inside a plane, mark the plane as satisfied and **don't test it again** for children
  (plane masking bitmask). If fully inside all planes, accept the whole subtree without tests.
- **Plane coherency**: remember which plane rejected an object last frame and test it first.

## 4. SIMD and data layout
- Store bounds in SoA (`cx[], cy[], cz[], r[]`) and test 4/8/16 objects per instruction against
  each plane; flat arrays of thousands of objects often beat pointer-chasing hierarchies.
- Multithread by splitting object ranges; write visible indices into per-thread lists.

## 5. Beyond the frustum
Combine with distance culling, small-object (screen-size) culling, occlusion culling (software
rasterised depth or GPU Hi-Z) and per-shadow-view culling using the same code path.

## Gotchas
- Plane extraction must match the API depth range (GL vs D3D/Vulkan near plane).
- Infinite far plane: drop the far test.
- Large objects partially intersecting shouldn't be split; just draw them.

## Verify
- [ ] Debug freeze-frustum mode shows culled objects disappearing exactly outside the frozen frustum.
- [ ] Culling time per frame measured; scales sublinearly with object count when hierarchical.
