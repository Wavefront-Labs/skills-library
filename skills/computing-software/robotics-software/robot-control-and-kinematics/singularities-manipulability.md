---
id: computing-software.robotics-software.robot-control-and-kinematics.singularities-manipulability
name: singularities-manipulability
category: computing-software
field: robotics-software
product: robot-control-and-kinematics
tags: [singularities, manipulability, jacobian-rank, wrist-singularity, condition-number, workspace]
level: advanced
status: draft
description: "Detect singularities and measure manipulability with Jacobian rank, condition number and Yoshikawa's measure."
sources:
  - https://control.ros.org/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Singularities
- A configuration is singular when J loses rank: some Cartesian direction cannot be produced, and tiny task velocities need huge joint velocities.
- Yoshikawa manipulability `w = sqrt(det(J J^T))`; singular values from `numpy.linalg.svd(J)`; condition number `s_max/s_min`.
```python
s = np.linalg.svd(J, compute_uv=False)
w = np.prod(s); cond = s[0]/s[-1]
if s[-1] < 1e-3: slow_down_or_damp()
```
- Typical 6R arm singularities: boundary (arm fully stretched), elbow, and wrist (two wrist axes aligned).
- Mitigate: damped least squares, plan paths away, use null-space motion, limit task speed near `s_min`.
- MoveIt Servo slows and stops near singularities using thresholds (see moveit-servo).

## Gotchas
- Position-only and full 6D Jacobians have different singularities.
- Numerical rank depends on the threshold; scale rows (m vs rad) first.

## Self-check
Fully extended planar 2R arm gives `det(J) = 0`; a bent pose has non-zero manipulability.
