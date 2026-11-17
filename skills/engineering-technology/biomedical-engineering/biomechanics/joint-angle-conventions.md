---
id: engineering-technology.biomedical-engineering.biomechanics.joint-angle-conventions
name: joint-angle-conventions
category: engineering-technology
field: biomedical-engineering
product: biomechanics
tags: [joint-angle-conventions, joint-kinematics, rigid-body-kinematics, euler-angles, cardan-angles, gimbal-lock, quaternion, rotation-matrix]
level: practitioner
status: gated
description: "Compute joint angles from rotation matrices with a stated Cardan or Euler sequence, handle gimbal lock and left-right sign conventions, and compare studies fairly."
sources: ["Wu et al., ISB recommendation on definitions of joint coordinate system of various joints (J Biomech 2002 and 2005)", "Craig, Introduction to Robotics: Mechanics and Control (rotation representations)", "Winter, Biomechanics and Motor Control of Human Movement"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Joint angle conventions

**Goal:** a reproducible set of joint angles from segment orientation data, with the sequence stated.

## Key facts
- 3D rotations do not commute, so the **rotation sequence changes the numbers**. Cardan sequences use three different axes (X-Y-Z, Z-X-Y); Euler sequences repeat one (Z-X-Z).
- **ISB lower limb** (Wu et al. 2002 covers ankle, hip and spine; the knee follows Grood and Suntay 1983; the Z-X-Y axis assignment below is from memory of the recommendation (gated: unconfirmed, source is paywalled or blocked)): hip and knee use Z-X-Y, with flexion-extension about Z (mediolateral), ab-adduction about the floating X axis and axial rotation about Y (long axis). The knee ab-adduction range is small, so the sequence order matters little there, but for the shoulder, sequence choice changes results considerably.
- **Gimbal lock:** when the middle angle reaches plus or minus 90 degrees, the first and third axes align and the decomposition is not unique. Keep the sequence so the middle rotation is the one with the smallest range (ab-adduction for hip and knee).

## Procedure
1. Express each segment's orientation as a rotation matrix R (global to segment).
2. Relative rotation R_rel = R_prox^T R_dist.
3. Extract angles with the chosen sequence (for R = Rz(alpha) Rx(beta) Ry(gamma): alpha = atan2(-R12, R22), beta = asin(R32), gamma = atan2(-R31, R33) with 1-based row-column indices; checked numerically: angles 0.3, 0.4, -0.5 rad round-trip exactly).
4. Subtract neutral standing offsets if the study protocol does so.
5. Mirror left-side signs (abduction and axial rotation reverse) so left and right are comparable.
6. For interpolation, averaging or filtering of orientations use quaternions or rotation vectors and convert at the end; do not filter Euler angles that wrap by 360 degrees without unwrapping.

## Gotchas
- Different software uses different default sequences and axis labels; read the manual.
- Angles about an anatomical axis are not the same as angles about a global axis.
- Projection angles (planar 2D) differ from 3D joint angles when motion is out of plane.

## Verify
- [ ] Apply a known rotation (30 degrees about one axis) and recover it.
- [ ] Reconstruct R from the angles and compare with the original.
- [ ] Cross-check results against a published dataset with the same convention.
