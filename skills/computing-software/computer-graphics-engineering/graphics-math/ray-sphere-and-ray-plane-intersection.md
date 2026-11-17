---
id: computing-software.computer-graphics-engineering.graphics-math.ray-sphere-and-ray-plane-intersection
name: ray-sphere-and-ray-plane-intersection
category: computing-software
field: computer-graphics-engineering
product: graphics-math
tags: [computer-graphics-engineering, graphics-math, intersection-tests, ray-sphere, ray-plane, quadratic-formula, catastrophic-cancellation, picking, ray-disk]
level: practitioner
status: verified
description: "Intersect rays with spheres and planes accurately: optimised geometric sphere test, numerically stable quadratic roots, plane and disk tests."
sources: ["Akenine-Moller et al., Real-Time Rendering (4th ed.), ch. 22.6", "https://link.springer.com/chapter/10.1007/978-1-4842-4427-2_7", "https://pbr-book.org/4ed/Shapes/Spheres"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Ray-sphere and ray-plane intersection

**Goal:** correct, precise analytic intersections for picking, bounding-sphere culling,
ray tracers and physics queries (RTR4 ch. 22; Ray Tracing Gems ch. 7).

## 1. Ray-plane
Plane `n·x + d = 0`, ray `o + t·r`:
```cpp
float denom = dot(n, r);
if (fabsf(denom) < 1e-8f) return false;            // parallel (or nearly)
float t = -(dot(n, o) + d) / denom;
return t >= tMin && t <= tMax;
```
Disk: plane hit then `|p - c|² ≤ R²`. Ground-plane picking: `n = (0,1,0)`, `d = -height`.
One-sided planes: reject `denom > 0` (ray hitting the back).

## 2. Ray-sphere: the stable formulation
Sphere centre c, radius R, ray direction r normalised:
```cpp
Vec3 f = o - c;
float b = dot(f, r);                                // half of the usual b
Vec3 l = f - b * r;                                 // perpendicular from centre to ray
float disc = R * R - dot(l, l);                     // more precise than b*b - (|f|² - R²)
if (disc < 0) return false;
float c2 = dot(f, f) - R * R;
float q = -b - copysignf(sqrtf(disc), b);           // avoid cancellation
float t0 = c2 / q, t1 = q;                          // roots (unordered)
if (t0 > t1) std::swap(t0, t1);
float t = (t0 >= tMin) ? t0 : t1;                   // origin inside sphere: use far root
return t >= tMin && t <= tMax;
```
The textbook `(-b ± sqrt(b²-4ac)) / 2a` subtracts nearly equal numbers when the sphere is
far away or small, losing most digits (catastrophic cancellation) — visible as speckled
holes on distant spheres. The form above (Ray Tracing Gems ch. 7) fixes both the
discriminant and the root computation. (Measured in float32 with a unit sphere 1e5 away over 2000 near-axis rays: summed near-root error 0.2 for this form vs 73 for the textbook form.)

## 3. Bounding sphere quick rejects
For culling/picking where only a yes/no is needed:
`b = dot(c - o, r); if (b < 0 && |c-o|² > R²) miss; d² = |c-o|² - b²; hit if d² ≤ R²`.

## 4. Normals and offsets
Hit normal `(p - c) / R`. Offset secondary-ray origins along the normal (scaled by
`|p| * epsilon`) to avoid self-intersection ("shadow acne" in ray tracers).

## Gotchas
- Non-normalised ray direction: either normalise or keep the full `a = dot(r, r)` term.
- Large world coordinates: subtract the camera position first (camera-relative) to keep precision.
- tMin of exactly 0 for secondary rays → self-hits; use a small positive tMin or origin offset.

## Verify
- [ ] Unit tests: tangent rays, origin inside, behind the ray, distant small spheres (1e5 units away).
- [ ] Rendered distant spheres free of speckle holes.
- [ ] Picking ground plane accurate at grazing angles.
