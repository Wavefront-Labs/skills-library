---
id: computing-software.computer-graphics-engineering.graphics-math.ray-obb-and-obb-intersection-tests
name: ray-obb-and-obb-intersection-tests
category: computing-software
field: computer-graphics-engineering
product: graphics-math
tags: [computer-graphics-engineering, graphics-math, intersection-tests, ray-obb, obb, separating-axis-theorem, collision-detection, bounding-volumes]
level: practitioner
status: draft
description: "Test rays and boxes against oriented bounding boxes: slab test in OBB local space, separating axis test for OBB-OBB (15 axes), epsilon handling and building OBBs."
sources: ["https://realtimecollisiondetection.net/", "https://www.realtimerendering.com/intersections.html", "https://www.geometrictools.com/Documentation/DynamicCollisionDetection.pdf"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Ray-OBB and OBB tests

OBB = centre c, orthonormal axes u0,u1,u2, half-extents e0,e1,e2.

## Ray-OBB: transform into box space
```cpp
bool rayOBB(vec3 o, vec3 d, const OBB& b, float& tmin) {
    vec3 p = o - b.c;
    vec3 ol(dot(p, b.u[0]), dot(p, b.u[1]), dot(p, b.u[2]));
    vec3 dl(dot(d, b.u[0]), dot(d, b.u[1]), dot(d, b.u[2]));
    return rayAABB(ol, dl, -b.e, b.e, tmin);        // standard slab test, t is unchanged (rigid map)
}
```
Same t because the map is rigid (no scale). For an OBB given as a 4x4 world matrix with scale,
transform the ray by the inverse matrix and keep d unnormalised: t still refers to the original ray.

## OBB-OBB: separating axis theorem
Test 15 axes: 3 face normals of A, 3 of B, 9 cross products `A_i x B_j`. Boxes are disjoint if, on any
axis L, `|T . L| > rA + rB` where `rA = sum e_i |u_i . L|`. Ericson's implementation computes
`R = A^T B` once and adds epsilon to `|R|` entries to handle nearly parallel edges (cross products
near zero). Early-out on the first separating axis.

## Point and sphere vs OBB
Closest point: clamp the point's local coordinates to [-e, e] and transform back; sphere overlaps if
the distance to the closest point is at most the radius.

## Building OBBs
- From PCA of the vertices (covariance eigenvectors): fast, can be poor for uneven vertex density;
  use the convex hull's surface-weighted covariance.
- Minimum-volume: rotating calipers on the hull (2D), DiTO or exhaustive search (3D) for tighter fits.

## Verify
Randomised tests against a brute-force reference (SAT vs GJK distance or mesh intersection) including
nearly parallel and touching configurations.
