---
id: computing-software.robotics-software.moveit-manipulation.moveit-servo
name: moveit-servo
category: computing-software
field: robotics-software
product: moveit-manipulation
tags: [moveit-servo, servo-node, delta-twist-cmds, jog, collision-checking-servo, command-type, moveit-servo-mtc]
level: advanced
status: docs-checked
description: "Run MoveIt Servo for real-time Cartesian or joint jogging with singularity and collision slowdown."
sources:
  - https://moveit.picknik.ai/main/index.html
  - https://github.com/moveit/moveit2
  - https://github.com/moveit/moveit2_tutorials
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# MoveIt Servo
**Goal:** teleoperate an arm with streamed commands.

- Launch `moveit_servo` (`servo_node_main` / composable `moveit_servo::ServoNode`) with a servo YAML and the MoveIt config parameters. Key params: `move_group_name`, `active_subgroup`, `command_in_type` (`unitless` or `speed_units`), `scale.linear`/`scale.rotational`/`scale.joint`, `publish_period`, `command_out_topic` (to a trajectory or position controller), `command_out_type`, `check_collisions`, `lower_singularity_threshold`, `hard_stop_singularity_threshold`.
- Input topics: `~/delta_twist_cmds` (TwistStamped), `~/delta_joint_cmds` (JointJog), `~/pose_target_cmds` (newer releases).
- Switch type (newer API): `ros2 service call /servo_node/switch_command_type moveit_msgs/srv/ServoCommandType "{command_type: 1}"` (0 joint jog, 1 twist, 2 pose).
- Output must match what the controller accepts (`JointTrajectory` to a joint_trajectory_controller, or `Float64MultiArray` to a forward controller).
- Parameter names changed between releases (Humble vs Jazzy); copy the example config from your branch.

## Gotchas
- Stale input stops motion after `incoming_command_timeout`; keep streaming.
- Servo bypasses the planner; collision checking is limited to its own check.

## Self-check
Publishing a twist at 20 Hz moves the end effector; stopping the stream stops the arm.

## Checked
2026-11-03: parameter, plugin, API and command names compared with the MoveIt 2 sources (moveit2 repository headers, servo_parameters.yaml, servo_node.cpp, datatypes.hpp, moveit_py bindings; moveit2_tutorials pages for controller configuration, OMPL, Pilz, setup assistant and Bullet). Removed or corrected: the `planning_frame` and `ee_frame_name` parameters (no longer in the servo parameter file).

Method: documentation only; no commands were run.
