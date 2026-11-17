---
id: computing-software.robotics-software.robot-control-and-kinematics.inverse-kinematics-jacobian
name: inverse-kinematics-jacobian
category: computing-software
field: robotics-software
product: robot-control-and-kinematics
tags: [inverse-kinematics, jacobian, damped-least-squares, pseudo-inverse, redundancy, differential-ik]
level: advanced
status: draft
description: "Solve IK numerically with the Jacobian: pseudo-inverse, damped least squares and redundancy resolution."
sources:
  - https://control.ros.org/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Differential and inverse kinematics
- Velocity relation `v = J(q) qdot` (6xN: linear rows, angular rows). Task error `e = x_d - x` (position difference plus orientation error from a rotation-vector or quaternion difference).
- Damped least squares (stable near singularities): `dq = J^T (J J^T + lambda^2 I)^-1 e`.
```python
def ik_step(J, e, lam=0.05, step=0.5):
    return step * J.T @ np.linalg.solve(J @ J.T + lam**2 * np.eye(J.shape[0]), e)
# loop: q += ik_step(J(q), pose_error(q_target, fk(q))) until norm(e) < 1e-4
```
- Redundant arms (N > task dim): add nullspace motion `(I - J^+ J) z`, e.g. toward joint-range centre or away from joint limits.
- Clamp to joint limits each iteration; seed from the current state for continuity.
- Analytic solutions exist for 6R arms with a spherical wrist (decoupling position and orientation); libraries (IKFast, KDL, pick_ik, TRAC-IK) give production solvers.

## Gotchas
- Pure pseudo-inverse blows up at singularities; always damp.
- Multiple solutions (elbow up/down); the iterative solver finds the one nearest the seed.

## Self-check
Pose from FK of random q recovered by IK to within 1e-4 and FK of the result matches the target.
