---
id: computing-software.robotics-software.robot-control-and-kinematics.forward-kinematics-dh
name: forward-kinematics-dh
category: computing-software
field: robotics-software
product: robot-control-and-kinematics
tags: [forward-kinematics, denavit-hartenberg, homogeneous-transform, rotation-matrix, urdf-joint-origin, tf2-kdl, kinematics-fk-ik]
level: practitioner
status: draft
description: "Compute forward kinematics with homogeneous transforms and Denavit-Hartenberg parameters."
sources:
  - https://control.ros.org/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Forward kinematics
**Goal:** end-effector pose from joint angles.

- Rotation about z: `Rz(t) = [[c,-s,0],[s,c,0],[0,0,1]]`; homogeneous `T = [[R,p],[0,1]]`; chain `T_0n = T_01 T_12 ... T_(n-1)n`.
- Standard DH link transform: `A_i = Rot_z(theta_i) Trans_z(d_i) Trans_x(a_i) Rot_x(alpha_i)`.
```python
import numpy as np
def A(theta, d, a, alpha):
    ct, st, ca, sa = np.cos(theta), np.sin(theta), np.cos(alpha), np.sin(alpha)
    return np.array([[ct, -st*ca,  st*sa, a*ct],
                     [st,  ct*ca, -ct*sa, a*st],
                     [0,      sa,     ca,    d],
                     [0,       0,      0,    1]])
T = np.linalg.multi_dot([A(q1,0.3,0,np.pi/2), A(q2,0,0.4,0), A(q3,0,0.3,0)])
```
- URDF is not DH: each joint has an `<origin xyz rpy>` and an `<axis>`; `robot_state_publisher` (KDL) does the FK for tf. Convert DH to URDF per link.
- Use quaternions in messages; rotation matrices for math.

## Gotchas
- Standard vs modified (Craig) DH conventions differ; do not mix tables.
- Check that R is orthonormal (`R @ R.T = I`, `det = 1`) after chaining.

## Self-check
Two-link planar arm at q = (0,0) gives x = l1 + l2, y = 0, and tf `lookup_transform` agrees.
