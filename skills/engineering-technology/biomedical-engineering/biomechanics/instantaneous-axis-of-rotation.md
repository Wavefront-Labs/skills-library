---
id: engineering-technology.biomedical-engineering.biomechanics.instantaneous-axis-of-rotation
name: instantaneous-axis-of-rotation
category: engineering-technology
field: biomedical-engineering
product: biomechanics
tags: [instantaneous-axis, helical-axis, screw-axis, instantaneous-centre, joint-kinematics]
level: advanced
status: draft
description: "Compute the helical (screw) axis and instantaneous centre of rotation of a joint from segment pose data, and judge when the estimate is reliable."
sources: ["Winter, Biomechanics and Motor Control of Human Movement (kinematics chapter)", "Woltring et al., finite helical axis literature (journal literature; confirm citations)", "https://www.isbweb.org"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Helical axis and instantaneous centre

**Goal:** describe joint motion between two segments as rotation about an axis plus translation along it, and know the estimate's limits.

## Method
1. Obtain the rotation matrix R and translation of segment B relative to A for two consecutive frames; the relative displacement is R_rel and the translation t_rel.
2. The **finite helical axis** direction n comes from the axial vector of R_rel (the eigenvector for eigenvalue 1); the rotation angle theta comes from the trace: cos(theta) = (trace(R_rel) - 1) / 2; translation along the axis is the dot product of t_rel with n.
3. A point on the axis follows from solving the displacement equation; the **instantaneous helical axis** is the limit as the time step shrinks.
4. In planar motion the axis reduces to an **instantaneous centre of rotation**; its path (the centrode) characterises, for example, the knee in the sagittal plane.

## Reliability
- When the rotation angle between frames is small, the axis location is very sensitive to noise (error grows roughly inversely with rotation angle). Use larger frame intervals, a minimum angle threshold, or smoothed and fitted data; do not interpret axes from tiny rotations.
- Soft tissue artefact corrupts the axis (see soft-tissue-artefact).
- Functional joint-centre and axis methods use this idea to locate hip centres and knee axes from calibration motions.

## Verify
- [ ] Frame interval and angle threshold chosen and reported.
- [ ] Test with a mechanical hinge of known axis to confirm the algorithm.
- [ ] Noise sensitivity examined by adding simulated marker noise.

> Practice guidance, not regulatory or clinical advice. Confirm current standard editions and rules for your jurisdiction, and defer to qualified regulatory, clinical and engineering judgement.
