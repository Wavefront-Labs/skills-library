---
id: computing-software.computer-graphics-engineering.graphics-math.axis-angle-and-rodrigues-rotation
name: axis-angle-and-rodrigues-rotation
category: computing-software
field: computer-graphics-engineering
product: graphics-math
tags: [computer-graphics-engineering, graphics-math, rotations, axis-angle, rodrigues, rotation-vector, exponential-map, so3]
level: sme
status: verified
description: "Work with axis-angle rotations: Rodrigues' formula, rotation vectors and the exponential/log map, conversions to quaternions and matrices, and small-angle stability."
sources: ["https://www.realtimerendering.com/", "https://docs.opencv.org/4.x/d9/d0c/group__calib3d.html#ga61585db663d9da06b68e70cfbf6a1eac", "https://www.cs.cmu.edu/~spiff/moedit99/expmap.pdf", "https://arxiv.org/abs/1812.01537"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Axis-angle and Rodrigues

## 1. Rodrigues' formula
Rotate v about unit axis k by angle theta:
`v' = v cos(theta) + (k x v) sin(theta) + k (k . v)(1 - cos(theta))`
Matrix form: `R = I + sin(theta) K + (1 - cos(theta)) K^2`, K = skew matrix of k.

## 2. Rotation vector (exponential map)
`r = theta * k` (3 numbers, no constraint): what OpenCV `rvec` and most optimisers use.
```python
R, _ = cv2.Rodrigues(rvec)        # rvec (3,) -> 3x3
rvec, _ = cv2.Rodrigues(R)        # 3x3 -> rvec
# scipy: Rotation.from_rotvec(r).as_matrix(), Rotation.from_matrix(R).as_rotvec()
```
- Log map (matrix -> axis-angle): `theta = acos((trace(R) - 1) / 2)`, `k = (R32-R23, R13-R31, R21-R12) / (2 sin theta)`.
- `acos` loses small angles entirely (acos of a value rounded to 1.0 returns 0 for theta=1e-9, while `2*atan2(|q.xyz|, q.w)` returns 1e-9); `cv2.Rodrigues` also returned a zero rvec for a 1e-8 rad rotation matrix while scipy `as_rotvec` kept it, so use scipy when tiny angles matter.
- Near theta = 0: use series `sin(theta)/theta ~ 1 - theta^2/6` to avoid 0/0.
- Near theta = pi: sin is ~0; take the axis from the largest diagonal of `(R + I)/2` instead.

## 3. Conversions
- To quaternion: `q = (cos(theta/2), k sin(theta/2))`.
- From quaternion: `theta = 2 atan2(|q.xyz|, q.w)`, `k = q.xyz / |q.xyz|` (atan2 is better conditioned than acos).

## 4. Uses
- Optimisation (bundle adjustment, pose refinement, IK): parameterise updates as `R_new = exp(delta) * R` with a
  3-vector delta - minimal and singularity-free locally (Lie algebra so(3)).
- Angular velocity integration: `R(t+dt) = exp(omega * dt) * R(t)`.
- Gizmos and "rotate around this axis by N degrees" UI.

## Gotchas
- Axis must be unit length; normalise or the formula scales vectors.
- Rotation vectors are not unique beyond |r| > pi (r and r - 2pi k are the same rotation); wrap when
  interpolating or comparing.
- Adding rotation vectors is not composing rotations (only valid for small angles).

## Verify
- [ ] Round-trip tests at theta = 0, 1e-8, pi/2, pi - 1e-6, pi: rotvec -> matrix -> rotvec within 1e-6 (axis
  sign may flip at pi).
