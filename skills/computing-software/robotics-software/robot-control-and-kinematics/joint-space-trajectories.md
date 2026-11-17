---
id: computing-software.robotics-software.robot-control-and-kinematics.joint-space-trajectories
name: joint-space-trajectories
category: computing-software
field: robotics-software
product: robot-control-and-kinematics
tags: [trajectory-polynomial, cubic-polynomial, quintic, trapezoidal-velocity, time-scaling, via-points, trajectory-generation]
level: practitioner
status: draft
description: "Generate joint trajectories with cubic or quintic polynomials and trapezoidal velocity profiles."
sources:
  - https://control.ros.org/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Joint-space trajectories
- Cubic from q0 to q1 over T with zero end velocities: `q(t) = q0 + (3s^2 - 2s^3)(q1 - q0)`, `s = t/T`. Quintic `q(t) = q0 + (10s^3 - 15s^4 + 6s^5)(q1 - q0)` also zeros end accelerations.
- Trapezoidal velocity: accelerate at `a` to `vmax`, cruise, decelerate; if `|dq| < vmax^2/a` it becomes triangular (peak `sqrt(a |dq|)`).
```python
def quintic(q0, q1, T, t):
    s = np.clip(t/T, 0, 1)
    return q0 + (10*s**3 - 15*s**4 + 6*s**5) * (q1 - q0)
```
- Synchronize joints: use the slowest joint's duration for all so they arrive together.
- Via points: use splines (cubic with continuous velocity) or pass waypoints to `joint_trajectory_controller` with velocities.
- Sampling should be at least the controller rate; check against joint velocity, acceleration (and jerk) limits.

## Gotchas
- Cubic gives jumps in acceleration (jerk spikes); use quintic or jerk-limited (Ruckig).
- Wrapping angles: for continuous joints choose the short way explicitly.

## Self-check
Evaluate at t = 0 and T: positions equal q0 and q1 and velocities equal zero.
