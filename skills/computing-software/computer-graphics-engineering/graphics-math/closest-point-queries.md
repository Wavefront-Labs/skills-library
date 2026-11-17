---
id: computing-software.computer-graphics-engineering.graphics-math.closest-point-queries
name: closest-point-queries
category: computing-software
field: computer-graphics-engineering
product: graphics-math
tags: [computer-graphics-engineering, graphics-math, intersection-tests, closest-point, point-triangle-distance, segment-segment-distance, distance-queries, collision-detection]
level: practitioner
status: draft
description: "Compute closest points: point to segment, triangle (Voronoi regions), box and convex shapes, segment-segment distance, and accelerated closest-point-on-mesh queries."
sources: ["https://realtimecollisiondetection.net/", "https://www.geometrictools.com/Documentation/DistancePoint3Triangle3.pdf", "https://trimesh.org/trimesh.proximity.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Closest point queries

## Point to segment AB
```cpp
vec3 closestOnSegment(vec3 p, vec3 a, vec3 b) {
    vec3 ab = b - a;
    float t = dot(p - a, ab) / dot(ab, ab);         // guard dot(ab,ab) == 0
    return a + clamp(t, 0.0f, 1.0f) * ab;
}
```

## Point to triangle (Ericson, Voronoi regions)
Check vertex regions (A, B, C), then edge regions (AB, AC, BC) using barycentric-style dot products,
else the face interior. Avoids computing the plane projection and then clipping, and is robust.
Returns the point plus the feature (vertex/edge/face) it lies on, useful for contact generation and
signed distance sign determination (use angle-weighted pseudo-normals at edges/vertices).

## Point to AABB / OBB
Clamp each coordinate to the box range (in OBB local axes for OBB). Distance = |p - clamped|.

## Segment to segment
Solve for parameters s, t minimising |P(s) - Q(t)|^2, clamp to [0,1] and re-solve the other parameter
(Ericson 5.1.9). Handle parallel segments (denominator near 0) explicitly. Basis of capsule-capsule
collision.

## Convex shapes
GJK gives the distance and closest points between any two convex shapes described by support
functions.

## Closest point on a mesh
Use a BVH over triangles with box-distance pruning: `trimesh.proximity.closest_point(mesh, pts)`,
Open3D `RaycastingScene.compute_closest_points`, libigl `point_mesh_squared_distance`, or
Embree/`fcpw` for speed. Signed distance: sign from winding number or pseudo-normals.

## Verify
Compare against brute-force sampling of the shape (dense points on triangle) for random queries;
distances must never be larger than the brute-force minimum.
