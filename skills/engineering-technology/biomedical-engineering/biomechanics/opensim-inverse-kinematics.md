---
id: engineering-technology.biomedical-engineering.biomechanics.opensim-inverse-kinematics
name: opensim-inverse-kinematics
category: engineering-technology
field: biomedical-engineering
product: biomechanics
tags: [opensim-ik, inverse-kinematics, opensim, marker-tracking, musculoskeletal-modeling]
level: practitioner
status: verified
description: "Run OpenSim inverse kinematics: marker weights, tasks, model scaling prerequisites, filtering, residual checks and the marker-error guidelines used to accept results."
sources: ["OpenSim documentation, Checklist - Evaluating your Simulation (https://opensimconfluence.atlassian.net/wiki/spaces/OpenSim/pages/53114566)", "OpenSim documentation, How Inverse Kinematics Works (https://opensimconfluence.atlassian.net/wiki/spaces/OpenSim/pages/53090047)", "Delp et al., OpenSim: open-source software to create and analyze dynamic simulations of movement (IEEE Trans Biomed Eng, 2007)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# OpenSim inverse kinematics

**Goal:** find joint coordinates over time that best reproduce measured marker positions with the scaled model.

## Method
1. **Prerequisites:** a scaled model with marker set placed from a static trial (see opensim-model-scaling), marker trajectories filtered and in the model coordinate system.
2. **Setup:** IK Tool with a task set listing each marker and weight; markers that are well placed on bony landmarks get higher weight than skin-sliding markers. Coordinates can also be tasks (prescribed or locked).
3. **Solve:** at each frame the solver minimises the weighted sum of squared marker errors (plus coordinate task errors) subject to the model's joint constraints.
4. **Outputs:** motion file with coordinate values and an error report (marker error per marker).
5. **Check:** examine marker errors; the OpenSim checklist "Evaluating your Simulation" asks whether the maximum marker error is less than 4 cm and the RMS error less than about 2 cm. Large persistent errors often mean a misplaced model marker or poor scaling.
6. Low-pass filter the resulting coordinates before differentiation for velocities (see butterworth-data-filtering), consistently with force data.

## Traps
- Tuning weights until error is small, hiding a model problem.
- Locking coordinates without reporting.
- Using IK output with a mismatch of time ranges or units (degrees versus radians).

## Verify
- [ ] Marker error report within the agreed thresholds.
- [ ] Scaling and weight choices documented.
- [ ] Joint angle curves plausible against reference data.

> Practice guidance, not regulatory or clinical advice. Confirm current standard editions and rules for your jurisdiction, and defer to qualified regulatory, clinical and engineering judgement.
