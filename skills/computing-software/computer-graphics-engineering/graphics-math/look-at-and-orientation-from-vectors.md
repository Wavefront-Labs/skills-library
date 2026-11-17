---
id: computing-software.computer-graphics-engineering.graphics-math.look-at-and-orientation-from-vectors
name: look-at-and-orientation-from-vectors
category: computing-software
field: computer-graphics-engineering
product: graphics-math
tags: [computer-graphics-engineering, graphics-math, quaternions, rotations, look-at, lookat-matrix, from-to-rotation, orthonormal-basis, up-vector-singularity, frisvad-basis, billboards, rotation-between-vectors]
level: practitioner
status: verified
description: "Build orientations from directions: look-at view and object matrices, the up-vector singularity, shortest-arc from-to quaternions."
sources: ["Akenine-Moller et al., Real-Time Rendering (4th ed.), ch. 4.2.4, 4.3.2", "https://jcgt.org/published/0006/01/01/paper.pdf", "https://glm.g-truc.net/0.9.9/api/a00668.html", "https://www.euclideanspace.com/maths/algebra/vectors/angleBetween/"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Look-at and orientation from vectors

**Goal:** cameras, turrets, billboards and tangent frames that point where intended without
flipping or NaNs at the poles (see RTR4's transforms chapter).

## 1. Look-at view matrix (right-handed, camera looks down −Z)
```cpp
Mat4 lookAtRH(Vec3 eye, Vec3 target, Vec3 up) {
    Vec3 f = normalize(target - eye);
    Vec3 s = normalize(cross(f, up));      // right; fails when f ∥ up
    Vec3 u = cross(s, f);                  // true up
    return Mat4{ s.x,  u.x, -f.x, 0,
                 s.y,  u.y, -f.y, 0,
                 s.z,  u.z, -f.z, 0,
                -dot(s, eye), -dot(u, eye), dot(f, eye), 1 };   // column-major storage
}
```
This is the **view** matrix (world → camera). To orient an **object** toward a target, use the
inverse: columns = (s, u, −f) and translation = position. Left-handed APIs/libraries (DirectXMath
`XMMatrixLookAtLH`) use +Z forward — don't mix conventions.

## 2. The up-vector singularity
When looking straight up/down, `cross(f, up)` → 0 → NaN. Fixes:
- If `|dot(f, up)| > 0.999`, use a fallback up (e.g. the previous frame's right vector, or
  world Z).
- Better for free-flying cameras: maintain orientation as a quaternion and apply incremental
  rotations rather than recomputing from a fixed world up.

## 3. Shortest-arc rotation between two directions
```cpp
Quat fromTo(Vec3 a, Vec3 b) {               // a, b normalised
    float d = dot(a, b);
    if (d < -0.999999f) {                   // opposite: rotate 180° about any perpendicular axis
        Vec3 axis = cross(Vec3(1,0,0), a); if (length2(axis) < 1e-6f) axis = cross(Vec3(0,1,0), a);
        return Quat::axisAngle(normalize(axis), PI);
    }
    Vec3 c = cross(a, b);
    return normalize(Quat(c.x, c.y, c.z, 1.0f + d));   // half-angle trick, no trig
}
```
Use for aligning a model's forward to a direction; combine with a twist about that axis for
full control.

## 4. Orthonormal basis from one vector (normals, sampling frames)
Frisvad / Duff et al. branchless method (JCGT 2017):
```cpp
void basis(Vec3 n, Vec3& t, Vec3& b) {
    float s = copysignf(1.0f, n.z), a = -1.0f / (s + n.z), c = n.x * n.y * a;
    t = Vec3(1.0f + s * n.x * n.x * a, s * c, -s * n.x);
    b = Vec3(c, s + n.y * n.y * a, -n.y);
}
```
Continuous except at one point, no NaN at the poles — standard in path tracers.

## Gotchas
- Non-normalised inputs scale the matrix → skewed lighting.
- Billboards using look-at per particle can roll unexpectedly; derive from camera right/up.
- Interpolating look-at results frame to frame can flip at the singularity; slerp quaternions.

## Verify
(Computed here: the look-at matrix maps eye to the origin and the target to (0,0,-distance) with determinant +1; `fromTo` mapped a to b for 1000 random pairs and for opposite vectors; the Duff et al. basis was orthonormal with determinant +1 over 20000 random normals and finite at n = (0,0,+-1).)
- [ ] Unit tests: looking along ±X, ±Y, ±Z, including straight up/down, produce finite orthonormal matrices.
- [ ] `fromTo(a, b) * a ≈ b` for random and opposite vectors.
- [ ] Determinant +1 (no reflection) for all generated bases.
