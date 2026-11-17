---
id: mathematics.geometry-and-topology.computational-geometry.robust-orientation-tests-and-convex-hulls
name: robust-orientation-tests-and-convex-hulls
category: mathematics
field: geometry-and-topology
product: computational-geometry
tags: [computational-geometry, convex-hull, orientation-predicate, orient2d, ccw, cross-product, monotone-chain, andrew-algorithm, graham-scan, robust-predicates, exact-arithmetic, floating-point, degeneracy, collinear-points, shewchuk, cgal, qhull, scipy-spatial, segment-intersection, point-in-polygon, delaunay]
level: practitioner
status: docs-checked
description: "Build geometric algorithms on a sign-exact orientation test: the orient2d determinant, Andrew's monotone-chain convex hull, collinear handling, and why float epsilons fail."
sources:
  - https://www.cs.cmu.edu/~quake/robust.html
  - https://doc.cgal.org/latest/Kernel_23/classCGAL_1_1Exact__predicates__inexact__constructions__kernel.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Robust orientation tests and convex hulls

**Goal:** implement 2-D geometric algorithms (convex hull, segment intersection,
point-in-polygon) that give correct, consistent answers — including on collinear,
duplicate and nearly-degenerate inputs.

## 1. Everything is one predicate
`orient(a, b, c) = (b.x − a.x)(c.y − a.y) − (b.y − a.y)(c.x − a.x)`
is twice the signed area of triangle abc: **> 0** left turn (counter-clockwise),
**< 0** right turn, **= 0** collinear. Hull, intersection, triangulation and
point-in-polygon tests reduce to signs of this (and, for Delaunay, `incircle`).
The algorithm is correct only if these **signs** are correct.

## 2. Convex hull: Andrew's monotone chain, O(n log n)
```python
def orient(a, b, c):
    return (b[0]-a[0])*(c[1]-a[1]) - (b[1]-a[1])*(c[0]-a[0])

def convex_hull(points):
    pts = sorted(set(points))            # by x, then y; duplicates removed
    if len(pts) <= 2:
        return pts
    lower, upper = [], []
    for p in pts:
        while len(lower) >= 2 and orient(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    for p in reversed(pts):
        while len(upper) >= 2 and orient(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    return lower[:-1] + upper[:-1]       # CCW order, collinear boundary points dropped
```
Change `<= 0` to `< 0` to **keep** collinear boundary points — but then all-collinear
inputs need special handling (the two chains duplicate points).

## 3. Why floating point breaks this
With doubles, `orient` is computed with rounding error; near-collinear triples can get
the **wrong sign**, and different triples can get mutually inconsistent signs — the hull
code then loops, drops true vertices, or returns a non-convex polygon. The Shewchuk
page notes that the sign of a small determinant is hard to get right when it is close
to zero, and that one fix is exact arithmetic.
**Adding an epsilon (`if abs(d) < 1e-9: treat as 0`) does not fix it**: the test is no
longer transitive, so inconsistencies just move.

## 4. Fixes, in order of preference
1. **Integer coordinates** (snap/scale input to a grid) and exact integer arithmetic,
   making sure the integer type cannot overflow in the determinant.
2. **Robust predicates:** Shewchuk's adaptive orientation and incircle tests (the
   algorithms do only as much work as needed to guarantee a correct result). CGAL's
   `CGAL::Exact_predicates_inexact_constructions_kernel` provides exact geometric
   predicates, but constructions are not exact in general.
3. **Exact rationals** (Python `fractions.Fraction`, GMP): slow but simple for prototypes.
4. Constructed points (computed intersections) are inexact even with exact predicates
   (per the CGAL kernel documentation); avoid feeding them back into predicates.

## 5. Other predicates built from orient
- **Segments ab, cd intersect** ⇔ orient(a,b,c), orient(a,b,d) have opposite signs and
  orient(c,d,a), orient(c,d,b) do too; zero cases need collinear-overlap checks
  (bounding-box test).
- **Point in convex polygon (CCW):** orient(vᵢ, vᵢ₊₁, p) ≥ 0 for every edge.
- **Polygon orientation:** sign of the shoelace sum.

## Gotchas
- Sorting must be total and deterministic — break ties by y.
- Duplicate points create zero-length edges; dedupe first.
- Library hull codes handle degenerate input differently; read their documentation.
- 3-D hulls need orient3d (4×4 determinant) and face-consistency care; use a library.

## Verify
- [ ] Hull vertices are CCW: every consecutive triple has orient > 0.
- [ ] Every input point satisfies orient(vᵢ, vᵢ₊₁, p) ≥ 0 for all hull edges.
- [ ] Degenerate tests pass: all collinear, all identical, 1–3 points, duplicates.
- [ ] Results match a trusted library on random and adversarial (near-collinear) inputs.

## Checked
2026-11-01. Confirmed: CGAL kernel documentation (exact predicates, inexact constructions
in general); Shewchuk's robust-predicates page (orientation and incircle tests, adaptive
precision, exact arithmetic as a fix). The orientation formula and monotone-chain code
are standard mathematics, not tool claims.
Removed: the 2164-of-4096 calibration figure, bit-width rules, the Rust crate, Qhull option
and error-code details, SciPy test claim.
Method: documentation only; no commands were run.
