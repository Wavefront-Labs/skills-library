---
id: engineering-technology.aerospace-engineering.matlab-simulink.frame-conversions-quaternions
name: frame-conversions-quaternions
category: engineering-technology
field: aerospace-engineering
product: matlab-simulink
tags: [matlab, simulink, aerospace-blockset, coordinate-conversion, quaternions, dcm, euler-angles, angle2dcm, attitude-representation]
level: practitioner
status: docs-checked
description: "Convert between Euler angles, direction cosine matrices and quaternions with Aerospace Toolbox functions, with scalar-first convention and singularity handling."
sources:
  - "https://www.mathworks.com/help/aerotbx/ug/angle2dcm.html"
  - "https://www.mathworks.com/help/aerotbx/ug/angle2quat.html"
  - "https://www.mathworks.com/help/aerotbx/ug/quat2dcm.html"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Frame conversions and quaternions

**Goal:** error-free attitude handling.

## Functions
- `dcm = angle2dcm(yaw, pitch, roll, 'ZYX')` (angles in radians) gives the DCM as a right-hand passive rotation from frame A to frame B; `'ZYX'` (yaw-pitch-roll) is the default sequence.
- `[yaw, pitch, roll] = dcm2angle(dcm, 'ZYX')`.
- `q = angle2quat(yaw, pitch, roll, 'ZYX')` (radians) and `quat2dcm(q)`; `quat2dcm` also normalizes its input. Aerospace Toolbox quaternions are scalar-first `[q0 q1 q2 q3]`. Related functions on the quat2dcm page: `dcm2quat`, `quat2angle`, `quatrotate`.

## Practice
1. Document the convention: frame names, rotation sequence, passive vs active (the toolbox DCM is a passive rotation from frame A to frame B).
2. Normalise quaternions after each integration step.
3. Use quaternion integration `qdot = 0.5 * q (x) [0, omega]` in body rates for propagation.
4. Convert to Euler angles only for display; Euler angles are singular at pitch +/-90 degrees.

## Gotchas
- Scalar-first vs scalar-last mix-ups with other libraries.
- Degrees vs radians.
- Product order: reversing quaternion multiplication order gives the inverse rotation sense.

## Verify
- [ ] `quat2dcm(angle2quat(y,p,r,'ZYX'))` equals `angle2dcm(y,p,r,'ZYX')` to machine precision.
- [ ] A 90-degree yaw maps the body x axis to the expected inertial direction.

## Checked
2026-11-01. Confirmed on the MathWorks angle2dcm, angle2quat and quat2dcm pages: syntax with optional rotation sequence, radians, default 'ZYX', scalar-first quaternions, passive rotation from frame A to frame B, quat2dcm normalization, dcm2angle as the inverse. Removed: quatmultiply, quatnormalize and quatinv (not on the pages read) and the textbook source. Kinematic equations are standard derivations.
Method: documentation only; no commands were run.
