---
id: engineering-technology.aerospace-engineering.spacecraft-systems-design.attitude-kinematics-representations
name: attitude-kinematics-representations
category: engineering-technology
field: aerospace-engineering
product: spacecraft-systems-design
tags: [attitude-kinematics, quaternions, direction-cosine-matrix, euler-angles, mrp, adcs]
level: practitioner
status: draft
description: "Choose and convert spacecraft attitude representations (DCM, Euler angles, quaternions, MRPs), propagate kinematics and compute attitude error."
sources:
  - "Markley and Crassidis, Fundamentals of Spacecraft Attitude Determination and Control"
  - "Wertz and Larson, Space Mission Analysis and Design"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Attitude kinematics

**Goal:** a consistent representation of orientation and its time derivative.

## Representations
- **DCM** (3x3 rotation matrix): unambiguous; 9 numbers with 6 constraints; `dC/dt = -[w x] C` for the body-from-inertial matrix.
- **Euler angles** (for example 3-2-1): intuitive for display; singular at the middle angle of plus or minus 90 degrees (for 3-2-1).
- **Quaternion** (4 numbers, unit norm): no singularity, `qdot = 0.5 * Omega(w) * q`; double cover (`q` and `-q` are the same attitude).
- **Modified Rodrigues parameters (MRPs)**: three parameters, singular at 360 degrees, switchable to the shadow set to avoid it.

## Procedure
1. Fix conventions in writing: quaternion order (scalar first or last), the direction (body from inertial or inverse), and rotation sequence.
2. Propagate the quaternion; renormalise (see attitude-propagation-integration).
3. Error attitude: `q_err = q_cmd^-1 (x) q_est` (quaternion product convention-dependent); use the vector part (or twice) as the small-angle error for control.
4. Take care at the sign: choose the shortest rotation by flipping `q_err` if its scalar part is negative.
5. Convert DCM to quaternion with a robust algorithm (Shepperd's method) rather than a single formula.

## Gotchas
- Mixing conventions between star-tracker, estimator and control is the leading cause of attitude bugs.
- Direction of rotation ambiguity: passive vs active.
- Euler angles for large-angle control produce singular behaviour.

## Verify
- [ ] Rotating a test vector with the DCM and with the quaternion gives the same result, and the round trip conversion recovers the input.
