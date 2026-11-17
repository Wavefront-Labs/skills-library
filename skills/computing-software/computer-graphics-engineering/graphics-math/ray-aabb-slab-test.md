---
id: computing-software.computer-graphics-engineering.graphics-math.ray-aabb-slab-test
name: ray-aabb-slab-test
category: computing-software
field: computer-graphics-engineering
product: graphics-math
tags: [computer-graphics-engineering, graphics-math, intersection-tests, ray-aabb, slab-test, inverse-direction, nan-handling, bvh-traversal, branchless]
level: practitioner
status: verified
description: "Implement the ray-AABB slab test robustly and fast: precomputed inverse direction, IEEE infinity behaviour for axis-parallel rays, NaN cases."
sources: ["Akenine-Moller et al., Real-Time Rendering (4th ed.), ch. 22.7", "https://tavianator.com/2022/ray_box_boundary.html", "https://jcgt.org/published/0002/02/02/paper.pdf", "https://pbr-book.org/4ed/Shapes/Basic_Shape_Interface#Bounds3::IntersectP"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Ray-AABB slab test

**Goal:** the inner-loop box test of every BVH traversal, picking, and culling query —
correct for all ray directions and fast (RTR4 ch. 22).

## 1. The algorithm
An AABB is the intersection of three slabs. For each axis compute the ray parameters where it
enters and leaves the slab; the ray hits the box if the latest entry precedes the earliest exit.
```cpp
// invDir = 1 / dir, precomputed once per ray
bool rayAABB(const Vec3& o, const Vec3& invDir, const AABB& b, float tMax, float& tNear) {
    Vec3 t0 = (b.min - o) * invDir;
    Vec3 t1 = (b.max - o) * invDir;
    Vec3 tmin = min(t0, t1), tmax = max(t0, t1);
    float tEnter = max(max(tmin.x, tmin.y), max(tmin.z, 0.0f));   // clamp to ray start
    float tExit  = min(min(tmax.x, tmax.y), min(tmax.z, tMax));   // and to current closest hit
    tNear = tEnter;
    return tEnter <= tExit;
}
```
Branchless min/max maps to SIMD and GPU instructions (`fminf`/`fmaxf`, `min3`/`max3`).

## 2. Axis-parallel rays (division by zero)
With IEEE floats `1/0 = ±inf`, so `(b.min - o) * inf` gives ±inf and the slab test still
works — **except** when the origin lies exactly on a slab plane: `0 * inf = NaN`.
- `fminf/fmaxf` return the non-NaN operand (verified for numpy `fmin`; plain `minimum` propagates NaN), which makes the test behave correctly in most
  implementations — order operands deliberately (Tavian Barnes' analysis).
- Or nudge zero direction components to a tiny epsilon before inverting.
Never compile with fast-math flags that assume no NaN/inf (`-ffast-math`) for this code.

## 3. Robustness for watertight traversal
Floating-point rounding can make a ray slip between adjacent boxes. PBR's approach:
multiply `tExit` by `1 + 2*gamma(3)` (conservative bound) so near-misses count as hits.
False positives only cost time; false negatives create holes.

## 4. Use in BVH traversal
- Pass `tMax` = closest hit so far: boxes behind an existing hit are rejected.
- Test both children, push the far one, visit the near one first (sort by `tNear`).
- Shadow/occlusion rays: any hit terminates (no sorting needed).
- Precompute per-ray `invDir` and `o * invDir` to turn the subtraction+multiply into an FMA:
  `t = b * invDir - (o * invDir)`.

## Gotchas
- Returning only a bool loses `tNear` needed for ordering.
- Boxes with min > max (empty/uninitialised) must be rejected explicitly or made impossible.
- Double-sided intervals: rays starting inside the box get tEnter = 0 — correct for most uses.

## Verify
- [ ] Unit tests: axis-parallel rays, origin on faces/edges/corners, inside-box origins, misses by 1 ulp.
- [ ] Brute-force comparison vs a double-precision reference on random rays (no false negatives).
- [ ] Traversal benchmark rays/s compared before/after optimisation.
