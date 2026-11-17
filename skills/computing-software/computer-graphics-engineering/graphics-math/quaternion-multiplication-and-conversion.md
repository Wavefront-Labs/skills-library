---
id: computing-software.computer-graphics-engineering.graphics-math.quaternion-multiplication-and-conversion
name: quaternion-multiplication-and-conversion
category: computing-software
field: computer-graphics-engineering
product: graphics-math
tags: [computer-graphics-engineering, graphics-math, rotations, quaternion-multiplication, quaternion, quaternion-to-matrix, euler-angles, hamilton-convention]
level: practitioner
status: verified
description: "Use quaternions correctly: Hamilton product order, rotating vectors, matrix and Euler conversions, w-first vs w-last storage, double cover, and normalisation."
sources: ["https://www.3dgep.com/understanding-quaternions/", "https://arxiv.org/abs/1711.02508", "https://www.euclideanspace.com/maths/geometry/rotations/conversions/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Quaternion multiplication and conversion

## Product (Hamilton)
```
q1 q2 = (w1 w2 - v1.v2,  w1 v2 + w2 v1 + v1 x v2)
```
Non-commutative. With `v' = q v q*`, `q1 q2` applies **q2 first, then q1** (same order as matrices
with column vectors).

## Rotate a vector efficiently
```cpp
vec3 rotate(quat q, vec3 v) {                 // q unit
    vec3 t = 2.0f * cross(q.xyz, v);
    return v + q.w * t + cross(q.xyz, t);
}
```
about 15-18 multiplies, cheaper than building the matrix for a single vector.

## Quaternion -> matrix (column vectors, unit q)
```
[1-2(y²+z²)  2(xy-wz)    2(xz+wy)  ]
[2(xy+wz)    1-2(x²+z²)  2(yz-wx)  ]
[2(xz-wy)    2(yz+wx)    1-2(x²+y²)]
```
## Matrix -> quaternion
Use Shepperd's method: pick the largest of `trace, m00, m11, m22` to avoid dividing by a tiny
number. Normalise the result. Input must be a pure rotation (orthonormalise first).

## Conventions that bite
- Storage: Eigen/GLM constructors take (w, x, y, z) but store (x, y, z, w); Unity, three.js, ROS
  messages, scipy `as_quat()` use (x, y, z, w) (scipy >= 1.14 `scalar_first=True` switches to w-first). Document it at every API boundary.
- JPL convention (some aerospace/VIO papers) multiplies in the opposite order: check before copying
  formulas.
- **Double cover**: q and -q are the same rotation. Before interpolating or comparing, flip one if
  `dot(q1, q2) < 0`.

## Euler angles
Always state the order (intrinsic ZYX yaw-pitch-roll, etc.). Use a library (`scipy.spatial.transform.Rotation.from_euler("ZYX", ...)`)
rather than hand-written formulas; gimbal lock at pitch +-90 degrees makes the inverse ambiguous (scipy warns and sets the third angle to zero). Uppercase axes (`"ZYX"`) are intrinsic, lowercase extrinsic.

## Normalisation
After many multiplications, renormalise (`q /= |q|`); a non-unit q scales vectors.

## Verify
Random unit quaternions: q -> matrix -> q round-trip equals q up to sign; rotation of vectors by q
matches the matrix.
