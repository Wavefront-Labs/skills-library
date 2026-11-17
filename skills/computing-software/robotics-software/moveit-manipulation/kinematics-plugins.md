---
id: computing-software.robotics-software.moveit-manipulation.kinematics-plugins
name: kinematics-plugins
category: computing-software
field: robotics-software
product: moveit-manipulation
tags: [kinematics-plugin, kdl-kinematics, kinematics-yaml, pick-ik, bio-ik, ikfast, moveit-kinematics]
level: practitioner
status: docs-checked
description: "Choose and configure MoveIt IK solvers (KDL, pick_ik, BioIK, IKFast, LMA) in kinematics.yaml."
sources:
  - https://moveit.picknik.ai/main/index.html
  - https://github.com/moveit/moveit2
  - https://github.com/moveit/moveit2_tutorials
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Kinematics plugins
```yaml
panda_arm:
  kinematics_solver: kdl_kinematics_plugin/KDLKinematicsPlugin     # or pick_ik/PickIkPlugin, bio_ik/BioIKKinematicsPlugin, lma_kinematics_plugin/LMAKinematicsPlugin
  kinematics_solver_search_resolution: 0.005
  kinematics_solver_timeout: 0.05
```
- KDL: default numeric solver, can fail on redundant or near-singular arms. IKFast: analytic, very fast for 6-DOF, generated per robot (OpenRAVE tooling, plugin package built from it). pick_ik / BioIK: global-ish optimization IK with weights, good for redundant arms.
- Limits: tolerance and attempts affect plan success rate.
- Direct IK in the API: `RobotState::setFromIK(group, pose, timeout)`.
- Inverse kinematics theory (Jacobian, redundancy) is covered in robot-control-and-kinematics skills.

## Gotchas
- KDL with `kinematics_solver_timeout` too low reports spurious failures.
- Chain with fewer than 6 DOF cannot reach arbitrary 6D poses; use position-only IK.

## Self-check
Pose goals that fail with KDL succeed (or fail faster) with the alternative; compare success rates over 100 random poses.

## Checked
2026-11-03: parameter, plugin, API and command names compared with the MoveIt 2 sources (moveit2 repository headers, servo_parameters.yaml, servo_node.cpp, datatypes.hpp, moveit_py bindings; moveit2_tutorials pages for controller configuration, OMPL, Pilz, setup assistant and Bullet). Removed or corrected: nothing needed removal.

Method: documentation only; no commands were run.
