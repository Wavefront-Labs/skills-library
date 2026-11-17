---
id: computing-software.computer-graphics-engineering.rendering-techniques.ray-triangle-intersection-moller-trumbore
name: ray-triangle-intersection-moller-trumbore
category: computing-software
field: computer-graphics-engineering
product: rendering-techniques
tags: [computer-graphics-engineering, rendering-techniques, ray-tracing, ray-triangle-intersection, moller-trumbore, watertight-intersection, barycentric-hit, edge-functions, self-intersection]
level: practitioner
status: docs-checked
description: "Ray-triangle intersection as pbrt-v4 does it: translate, permute and shear into ray space, edge functions, double-precision fallback, barycentrics and conservative t."
sources: ["https://pbr-book.org/4ed/Shapes/Triangle_Meshes"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Ray-triangle intersection (watertight, as in pbrt-v4)

**Goal:** the core primitive test of CPU ray tracers: correct barycentrics and hit distance, and no
cracks between adjacent triangles. Source: pbrt-v4 section 6.5.3 (`IntersectTriangle`). The
Moller-Trumbore algorithm is mentioned there only as the way to get barycentrics of a point
direction in the triangle (solve the ray equals barycentric interpolation linear system); its
original paper could not be read as text, so no Moller-Trumbore code is given here.

## 1. Algorithm (pbrt's IntersectTriangle)
1. **Degenerate test first:** return no hit if `LengthSquared(Cross(p2 - p0, p1 - p0)) == 0`. After
   the transform a degenerate triangle could become non-degenerate through round-off, and later
   code cannot compute valid geometry for it.
2. **Transform to ray space:** translate vertices by the ray origin, permute axes so `z` is the
   dimension where `|ray.d|` is largest (this guarantees nonzero `d.z`), then shear x and y with
   `Sx = -d.x/d.z`, `Sy = -d.y/d.z`; z is scaled by `Sz = 1/d.z` only if needed later. The
   permutation and shear depend only on the ray, so a fast tracer can precompute them per ray.
3. **Edge functions** in 2D (the ray is now the z axis through the origin):
   `e0 = p1t.x*p2t.y - p1t.y*p2t.x`, `e1 = p2t.x*p0t.y - p2t.y*p0t.x`,
   `e2 = p0t.x*p1t.y - p0t.y*p1t.x` (computed with a difference-of-products helper).
4. **Double-precision fallback:** if any edge function is exactly zero (float build), recompute
   all three in double. This is what makes the test watertight for rays through shared edges.
5. **Reject:** if edge values have mixed signs, no hit. `det = e0 + e1 + e2`; `det == 0` means
   the ray is edge-on, so no hit (a closed mesh gives a neighbour hit instead).
6. **Scaled hit distance:** `tScaled = e0*z0 + e1*z1 + e2*z2` with sheared z values. Test against
   the ray range without dividing: with `det > 0` reject if `tScaled <= 0 || tScaled > tMax*det`
   (flip the comparisons for `det < 0`).
7. **Barycentrics:** `b_i = e_i / det`, `t = tScaled / det`. They sum to 1.
8. **Conservative t check:** compute error bounds and reject if `t <= deltaT`, so the computed
   hit is conservatively greater than zero (pbrt uses floating-point error bounds built from
   `gamma(n)` factors on the sheared coordinates, `deltaZ`, `deltaE` and `deltaT`).

Interpolate attributes with the barycentrics: `p = b0*p0 + b1*p1 + b2*p2` (same for uv). pbrt
also bounds the error of the hit point as `gamma(7) * (|b0 p0| + |b1 p1| + |b2 p2|)` so rays
spawned from it can be offset correctly.

## 2. Notes
- pbrt computes the geometric normal as the normalised cross product of two edges and flips it
  when the mesh orientation is reversed or the transform swaps handedness.
- pbrt's GPU path uses hardware ray-triangle intersection that reports the triangle index and
  barycentrics, and builds the surface interaction from those with the same code as the CPU.
- The page does not discuss back-face culling or epsilon choices; do not assume pbrt's behaviour
  applies to a culling variant.

## Verify
- [ ] Ray grid fired at a finely tessellated closed mesh: zero escaped rays.
- [ ] Unit tests: edge hits, vertex hits, rays parallel to the plane, degenerate triangles.
- [ ] Barycentrics sum to 1 and reproduce the hit position.

## Checked
Checked 2026-11-08 against pbrt-v4 chapter 6 section 6.5 (Triangle Meshes). The Moller-Trumbore
and Woop et al. watertight papers (PDFs) did not extract to readable text, so the earlier
Moller-Trumbore code, the back-face and epsilon advice, the Ray Tracing Gems self-intersection
reference, the DXR and Vulkan statement and the Real-Time Rendering book source were removed.
Method: docs-only read of cited pages, 2026-11-08
