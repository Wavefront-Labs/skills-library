---
id: engineering-technology.aerospace-engineering.matlab-simulink.attitude-propagation-integration
name: attitude-propagation-integration
category: engineering-technology
field: aerospace-engineering
product: matlab-simulink
tags: [attitude-integration, quaternion-kinematics, attitude-propagation, numerical-integration, euler-angles]
level: practitioner
status: docs-checked
description: "Integrate rigid-body attitude with quaternions, keep the norm, avoid Euler-angle singularities, and choose a step size that bounds attitude drift."
sources:
  - "https://www.mathworks.com/help/aeroblks/6dofquaternion.html"
  - "https://www.mathworks.com/help/aeroblks/6dofecefquaternion.html"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Attitude propagation

**Goal:** propagate attitude through a six-DOF or spacecraft simulation without drift or singularity.

## Equations
- Quaternion kinematics: `qdot = 0.5 * Omega(w) * q`, where `w` is the body rate and `Omega` is the skew matrix built from it. State the convention first: scalar-first or scalar-last, body-to-inertial or inertial-to-body.
- Euler-angle rates have a singularity at pitch of plus or minus 90 degrees; use them only for display.

## Procedure
1. State `q` and body rates `w` (from the moment equation `I*wdot + w x I*w = M`).
2. Integrate `q` with the same fixed-step method as the rest of the model , or use a variable-step solver with tight tolerances.
3. Renormalise `q` after every step (`q = q/norm(q)`), or use a block that does it: the Aerospace Blockset 6DOF (Quaternion) block applies a correction gain that drives the quaternion norm back to 1.0 (its "Gain for quaternion normalization" parameter was removed in R2025a). Aerospace Blockset quaternions are scalar-first.
4. Convert to Euler angles only for output; use `atan2` forms.
5. For high-rate spinning bodies, shorten the step or use an exponential-map update from the angle increment `w*dt`.

## Gotchas
- Mixing quaternion conventions between blocks flips rotation direction.
- Normalising by division hides a bug if the norm drifts quickly; log `norm(q) - 1`.
- Integrating each Euler angle separately is wrong for large rotations.

## Verify
- [ ] Constant-rate spin about one axis for 360 degrees returns to the initial quaternion (up to sign) within tolerance; `norm(q) - 1` stays within your tolerance.

## Checked
2026-11-01. Confirmed on the two MathWorks 6DOF Quaternion block pages: normalisation correction
and removed parameter (R2025a), scalar-first convention. The kinematics equation and the
Euler-angle singularity are standard mathematics. Removed: RK4 recommendation, the 1e-9
figure and the textbook source.
Method: documentation only; no commands were run.
