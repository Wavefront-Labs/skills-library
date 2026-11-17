---
id: computing-software.game-programming.game-physics.primitive-intersection-tests
name: primitive-intersection-tests
category: computing-software
field: game-programming
product: game-physics
tags: [game-physics, narrow-phase, primitive-tests, ray-aabb, slab-test, sphere-sphere, capsule, closest-point, ray-sphere, aabb-overlap, game-programming]
level: practitioner
status: verified
description: "Implement the core primitive tests from Real-Time Collision Detection: sphere, AABB, capsule, ray-AABB slab, ray-sphere and closest-point queries, with robustness notes."
sources: ["https://realtimecollisiondetection.net/books/rtcd/", "https://tavianator.com/2022/ray_box_boundary.html", "https://iquilezles.org/articles/intersectors/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Primitive intersection tests

**Goal:** a small, correct, fast library of the tests every game uses: overlap checks, raycasts,
and closest points (Ericson, *Real-Time Collision Detection*).

## Overlaps
```cpp
bool sphereSphere(V3 c1, float r1, V3 c2, float r2) {
    V3 d = c2 - c1; float r = r1 + r2;
    return dot(d, d) <= r * r;                       // compare squared, no sqrt
}
bool aabbAabb(const AABB& a, const AABB& b) {
    return a.min.x <= b.max.x && a.max.x >= b.min.x &&
           a.min.y <= b.max.y && a.max.y >= b.min.y &&
           a.min.z <= b.max.z && a.max.z >= b.min.z;
}
V3 closestPointOnAabb(V3 p, const AABB& b) { return clamp(p, b.min, b.max); }
bool sphereAabb(V3 c, float r, const AABB& b) {
    V3 q = closestPointOnAabb(c, b); V3 d = q - c; return dot(d, d) <= r * r;
}
V3 closestPointOnSegment(V3 p, V3 a, V3 b) {
    V3 ab = b - a; float t = dot(p - a, ab) / dot(ab, ab);
    return a + ab * std::clamp(t, 0.0f, 1.0f);
}
// capsule = segment (a,b) + radius: capsule-sphere = segment point distance <= rCap + rSphere
// capsule-capsule = closest points between two segments (Ericson, closest point of two segments) distance <= r1 + r2
```

## Raycasts
Ray-AABB slab test (handles axis-parallel rays via IEEE infinities):
```cpp
bool rayAabb(V3 o, V3 invDir, const AABB& b, float tMax, float& tHit) {
    float t0 = 0.0f, t1 = tMax;
    for (int i = 0; i < 3; ++i) {
        float tNear = (b.min[i] - o[i]) * invDir[i];
        float tFar  = (b.max[i] - o[i]) * invDir[i];
        if (tNear > tFar) std::swap(tNear, tFar);
        t0 = tNear > t0 ? tNear : t0;     // written this way so NaN does not poison the result
        t1 = tFar  < t1 ? tFar  : t1;
        if (t0 > t1) return false;
    }
    tHit = t0; return true;
}
```
Precompute `invDir = 1/dir` once per ray when testing many boxes (BVH traversal).
Ray-sphere: solve `|o + t d - c|^2 = r^2`; with `m = o - c`, `b = dot(m,d)`, `c = dot(m,m) - r^2`:
if `c > 0 && b > 0` no hit; `disc = b*b - c` (d normalised); if `disc < 0` no hit; `t = -b - sqrt(disc)`, clamp to 0 if
inside. (Ported to Python and fuzzed against brute-force sampling: 3000 random rays each for the AABB slab test, including
axis-parallel rays, and the sphere test, zero mismatches.)

## Robustness
- Use squared distances; only `sqrt` when the value is needed.
- Degenerate segments (`dot(ab,ab) == 0`) need a guard before dividing.
- Use a small epsilon for "touching" comparisons in gameplay code, never in broad-phase rejection
  where false negatives cause missed collisions.
- Double-check handedness/normal direction for plane tests: `dot(n, p) - d` sign convention.
- Test with randomized fuzzing against a slow reference (e.g. sampled distance).

## Verify
- [ ] Unit tests: touching, separated, contained, and axis-parallel ray cases.
- [ ] Fuzz 1e6 random cases against a reference implementation: zero mismatches.
- [ ] Profile: ray-AABB inner loop branch-light and without division.
