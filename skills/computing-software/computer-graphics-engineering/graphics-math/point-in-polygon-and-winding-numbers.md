---
id: computing-software.computer-graphics-engineering.graphics-math.point-in-polygon-and-winding-numbers
name: point-in-polygon-and-winding-numbers
category: computing-software
field: computer-graphics-engineering
product: graphics-math
tags: [computer-graphics-engineering, graphics-math, intersection-tests, point-in-polygon, winding-number, even-odd-rule, polygon, inside-outside-test]
level: practitioner
status: draft
description: "Decide if a point is inside a polygon: crossing (even-odd) vs winding number rules, robust edge-crossing code, holes and self-intersections, and 3D generalised winding numbers."
sources: ["https://en.wikipedia.org/wiki/Point_in_polygon", "https://www.w3.org/TR/SVG2/painting.html#WindingRule", "https://igl.ethz.ch/projects/winding-number/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Point in polygon and winding numbers

## Winding number (non-zero rule)
```cpp
float isLeft(vec2 a, vec2 b, vec2 p) { return (b.x-a.x)*(p.y-a.y) - (p.x-a.x)*(b.y-a.y); }
int winding(vec2 p, const std::vector<vec2>& v) {
    int wn = 0;
    for (size_t i = 0, n = v.size(); i < n; ++i) {
        vec2 a = v[i], b = v[(i + 1) % n];
        if (a.y <= p.y) { if (b.y > p.y && isLeft(a, b, p) > 0) ++wn; }   // upward crossing, p left
        else            { if (b.y <= p.y && isLeft(a, b, p) < 0) --wn; }  // downward crossing, p right
    }
    return wn;           // inside if wn != 0
}
```
The half-open `<=`/`>` comparison on y counts vertices exactly once, so rays through vertices are
handled without special cases.

## Crossing number (even-odd)
Count edge crossings of a horizontal ray; odd = inside. Same complexity; differs from non-zero only for
self-intersecting or overlapping polygons.

## Which rule
- Matches renderers: SVG/Canvas `fill-rule` (`nonzero` default, `evenodd`), TrueType (non-zero),
  PostScript both. Use the same rule as the data's source.
- Polygons with holes: either store holes with opposite orientation (non-zero works) or use even-odd.
- `cv2.pointPolygonTest(contour, pt, measureDist)` returns +1/0/-1 (or signed distance).
- Shapely/GEOS for GIS work (with proper boundary semantics).

## Points on the boundary
Decide explicitly: treat as inside, outside, or a separate result; exact arithmetic (integers or
robust predicates like Shewchuk's orient2d) when points can lie exactly on edges.

## Many queries
Precompute a grid or trapezoidal map, or rasterise the polygon into a mask for pixel queries.

## 3D: generalised winding number
For triangle meshes (possibly non-watertight), the sum of solid angles subtended by triangles / 4 pi
gives inside (about 1) vs outside (about 0) robustly (Jacobson et al.); libigl `winding_number`,
fast approximations with hierarchical evaluation.

## Verify
Tests: convex, concave, self-intersecting star (rules differ), holes, points exactly on vertices and
edges.
