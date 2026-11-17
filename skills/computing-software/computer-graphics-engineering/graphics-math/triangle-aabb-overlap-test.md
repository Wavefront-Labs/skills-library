---
id: computing-software.computer-graphics-engineering.graphics-math.triangle-aabb-overlap-test
name: triangle-aabb-overlap-test
category: computing-software
field: computer-graphics-engineering
product: graphics-math
tags: [computer-graphics-engineering, graphics-math, intersection-tests, triangle-aabb, separating-axis-theorem, voxelization, bvh, collision-detection]
level: advanced
status: draft
description: "Implement the triangle-box overlap test (Akenine-Moller SAT): 13 axes, box-centred coordinates, plane-box test, and use in voxelisation, BVH building and conservative culling."
sources: ["https://fileadmin.cs.lth.se/cs/Personal/Tomas_Akenine-Moller/code/tribox_tam.pdf", "https://realtimecollisiondetection.net/", "https://www.realtimerendering.com/intersections.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Triangle-box overlap

## Akenine-Moller SAT (13 axes)
1. Translate triangle so the box centre is at the origin (box = half-extents h).
2. **3 box face normals** (x, y, z): triangle's AABB vs box (min/max of vertex coordinates against +-h).
3. **1 triangle normal**: plane-box test. With n and d = -n . v0, box overlaps the plane if
   `|d| <= h . |n|`.
4. **9 cross-product axes** `e_i x f_j` (box axes x triangle edges): project triangle (2 distinct
   values needed per axis thanks to the structure) and box radius `r = h . |axis|`, separated if the
   triangle's interval is entirely outside [-r, r].
Any separating axis -> no overlap. Order tests cheapest/most likely first (AABB test first is common).

```cpp
// example of one cross axis: a = (0, -f.z, f.y) for e_x x f
float p0 = a.y * v0.y + a.z * v0.z, p2 = a.y * v2.y + a.z * v2.z;
float r = h.y * fabsf(f.z) + h.z * fabsf(f.y);
if (fminf(p0, p2) > r || fmaxf(p0, p2) < -r) return false;
```

## Uses
- **Voxelisation**: which voxels a triangle touches (conservative surface voxelisation). Faster
  specialised version: Schwarz-Seidel's triangle/box with precomputed edge functions per triangle.
- BVH/octree building: clip-aware binning of triangles into nodes.
- Collision broad/mid-phase against grids.

## Robustness
Degenerate (zero-area) triangles: the normal axis is zero; handle as segments or skip. Use consistent
`<`/`<=` so touching triangles count once on shared boundaries in voxelisation (tie-breaking rule).

## Verify
Compare against an exact reference (clip the triangle by the 6 box planes; non-empty polygon means
overlap) on millions of random cases, including triangles exactly on box faces.
