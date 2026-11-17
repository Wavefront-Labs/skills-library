---
id: computing-software.robotics-software.robot-control-and-kinematics.cartesian-orientation-paths
name: cartesian-orientation-paths
category: computing-software
field: robotics-software
product: robot-control-and-kinematics
tags: [cartesian-trajectory, slerp, quaternion-interpolation, straight-line-path, orientation-error, screw-motion]
level: advanced
status: draft
description: "Interpolate Cartesian paths with position lines and quaternion slerp, and compute orientation error correctly."
sources:
  - https://control.ros.org/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Cartesian paths and orientation
- Position: linear `p(s) = p0 + s (p1 - p0)` with `s(t)` from a time-scaling profile.
- Orientation: quaternion spherical interpolation, `slerp(q0, q1, s)`; flip `q1` to `-q1` when `dot(q0, q1) < 0` to take the short arc.
```python
from scipy.spatial.transform import Rotation as R, Slerp
slerp = Slerp([0, 1], R.from_quat([q0, q1]))
q_s = slerp([s]).as_quat()[0]            # scipy quaternion order: x, y, z, w (same as ROS)
err = (R.from_quat(q_d) * R.from_quat(q).inv()).as_rotvec()    # orientation error as rotation vector (world frame)
```
- Convert Cartesian samples to joint samples by IK each step; check the joint jumps are small (branch flipping).
- MoveIt: `computeCartesianPath(waypoints, eef_step, jump_threshold, traj)` or Pilz LIN.
- Avoid Euler-angle interpolation (gimbal lock, uneven rotation).

## Gotchas
- Rotation-vector error depends on frame convention (world vs body); keep it consistent with the Jacobian frame.
- ROS quaternion order is x y z w; some libraries use w x y z.

## Self-check
Slerp at s = 0.5 between 0 and 90 degrees yaw gives 45 degrees.
