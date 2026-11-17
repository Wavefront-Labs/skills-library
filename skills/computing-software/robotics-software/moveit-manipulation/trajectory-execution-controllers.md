---
id: computing-software.robotics-software.moveit-manipulation.trajectory-execution-controllers
name: trajectory-execution-controllers
category: computing-software
field: robotics-software
product: moveit-manipulation
tags: [trajectory-execution, moveit-simple-controller-manager, follow-joint-trajectory, ros2-controllers-yaml, allowed-execution-duration, execute-trajectory, moveit-execution]
level: practitioner
status: docs-checked
description: "Connect MoveIt to controllers via FollowJointTrajectory and tune trajectory execution monitoring."
sources:
  - https://moveit.picknik.ai/main/index.html
  - https://github.com/moveit/moveit2
  - https://github.com/moveit/moveit2_tutorials
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Trajectory execution
`moveit_controllers.yaml`:
```yaml
moveit_controller_manager: moveit_simple_controller_manager/MoveItSimpleControllerManager
moveit_simple_controller_manager:
  controller_names: [panda_arm_controller]
  panda_arm_controller:
    type: FollowJointTrajectory
    action_ns: follow_joint_trajectory
    default: true
    joints: [panda_joint1, panda_joint2]
```
- The action server lives in `ros2_control`'s `joint_trajectory_controller` at `/panda_arm_controller/follow_joint_trajectory`.
- Execution monitoring: `allowed_execution_duration_scaling`, `allowed_goal_duration_margin`, `allowed_start_tolerance` (under `trajectory_execution`).
- Controller joints and names must match `ros2_controllers.yaml`; the controller must be active before planning.

## Gotchas
- Controller-name mismatches between `moveit_controllers.yaml` and `ros2_controllers.yaml` break execution.
- Start-state tolerance failures: arm moved or controller state differs from planning start.

## Self-check
`plan` then `execute` moves the simulated arm and the action finishes with success.

## Checked
2026-11-03: parameter, plugin, API and command names compared with the MoveIt 2 sources (moveit2 repository headers, servo_parameters.yaml, servo_node.cpp, datatypes.hpp, moveit_py bindings; moveit2_tutorials pages for controller configuration, OMPL, Pilz, setup assistant and Bullet). Removed or corrected: the `ros2 control list_controllers` command and quoted error strings.

Method: documentation only; no commands were run.
