---
id: computing-software.computer-graphics-engineering.graphics-math.gjk-and-epa-algorithms
name: gjk-and-epa-algorithms
category: computing-software
field: computer-graphics-engineering
product: graphics-math
tags: [computer-graphics-engineering, graphics-math, intersection-tests, gjk, epa, minkowski-difference, convex-collision, penetration-depth]
level: advanced
status: draft
description: "Implement GJK for convex distance/overlap and EPA for penetration depth: support functions, Minkowski difference simplex cases, termination tolerances and robustness pitfalls."
sources: ["https://caseymuratori.com/blog_0003", "https://dyn4j.org/2010/04/gjk-gilbert-johnson-keerthi/", "https://dyn4j.org/2010/05/epa-expanding-polytope-algorithm/", "https://realtimecollisiondetection.net/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# GJK and EPA

## Support functions
Convex shapes are described only by `support(d)` = farthest point along d. Minkowski difference
support: `S(d) = supportA(d) - supportB(-d)`. Examples: sphere `c + r d/|d|`; box
`c + sum sign(d . u_i) e_i u_i`; polytope = max over vertices (hill climbing for large hulls);
capsule = segment support + radius. Margins (rounded shapes) improve robustness.

## GJK (overlap / distance)
The shapes overlap iff the origin is inside A - B. Build a simplex (point, segment, triangle,
tetrahedron) of support points that moves toward the origin:
```
d = initial direction; simplex = [S(d)]; d = -simplex[0]
loop:
    p = S(d)
    if dot(p, d) < 0: return NO_OVERLAP          # cannot pass the origin
    simplex.add(p)
    if doSimplex(simplex, d): return OVERLAP      # origin enclosed (tetrahedron)
```
`doSimplex` finds the sub-feature (vertex/edge/face region) closest to the origin, drops other points
and sets d toward the origin from that feature. For distance queries, terminate when the progress
`dot(p, d) - dot(closest, d)` falls below a relative tolerance and return the closest-point
barycentric combination (gives witness points on A and B).

## EPA (penetration depth)
Starting from GJK's enclosing tetrahedron, repeatedly expand the polytope toward the face closest to
the origin with `S(face normal)` until the new point is no farther than the face (within tolerance).
Result: penetration normal and depth for contact generation.

## Robustness
- Degenerate simplices (collinear/coplanar points), touching contact, and float error cause cycling:
  cap iterations (e.g. 32 to 64), use relative tolerances, keep the best result.
- EPA is fragile near-touching; engines prefer GJK on margin-shrunk shapes for shallow contacts and
  use EPA only for deep penetration.
- libccd, Bullet's `btGjkEpa2`, Jolt and Box2D v3 are good references.

## Verify
Random convex pairs vs brute-force polytope distance (e.g. via linear programming or exhaustive
feature pairs); test touching, deeply overlapping and far-apart cases.
