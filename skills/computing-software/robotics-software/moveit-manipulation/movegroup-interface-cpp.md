---
id: computing-software.robotics-software.moveit-manipulation.movegroup-interface-cpp
name: movegroup-interface-cpp
category: computing-software
field: robotics-software
product: moveit-manipulation
tags: [move-group-interface, movegroupinterface, setposetarget, plan-execute, named-target, scaling-factor, moveit-move-group]
level: practitioner
status: docs-checked
description: "Plan and execute with moveit::planning_interface::MoveGroupInterface in C++: goals, named targets, scaling factors."
sources:
  - https://moveit.picknik.ai/main/index.html
  - https://github.com/moveit/moveit2
  - https://github.com/moveit/moveit2_tutorials
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# MoveGroupInterface (C++)
```cpp
#include <moveit/move_group_interface/move_group_interface.hpp>   // the .h header is a deprecated forwarding header
auto node = std::make_shared<rclcpp::Node>("mgi", rclcpp::NodeOptions().automatically_declare_parameters_from_overrides(true));
moveit::planning_interface::MoveGroupInterface mg(node, "panda_arm");
mg.setMaxVelocityScalingFactor(0.2); mg.setMaxAccelerationScalingFactor(0.2);
mg.setNamedTarget("ready");                        // from SRDF group_state
// or: mg.setPoseTarget(pose_stamped); mg.setJointValueTarget(joint_vector);
moveit::planning_interface::MoveGroupInterface::Plan plan;
if (mg.plan(plan) == moveit::core::MoveItErrorCode::SUCCESS) mg.execute(plan);
```
- The node must spin in another thread (executor) for state updates; the node needs the same params as `move_group`, or run with robot description available.
- `getCurrentPose()`, `getCurrentJointValues()`, `setStartStateToCurrentState()`.
- Cartesian path: `computeCartesianPath(waypoints, 0.01, trajectory)` (`eef_step` in metres) returns the fraction achieved. The overload taking `jump_threshold` is deprecated ("Drop jump_threshold").

## Gotchas
- `plan()` without a spinning executor times out waiting for current state.
- Cartesian fraction below 1.0 means a partial path; check it before executing.

## Self-check
Robot reaches the named target in simulation; `getCurrentPose()` matches the goal within tolerance.

## Checked
2026-11-03: parameter, plugin, API and command names compared with the MoveIt 2 sources (moveit2 repository headers, servo_parameters.yaml, servo_node.cpp, datatypes.hpp, moveit_py bindings; moveit2_tutorials pages for controller configuration, OMPL, Pilz, setup assistant and Bullet). Removed or corrected: the deprecated `jump_threshold` form of `computeCartesianPath` and the `.h` include.

Method: documentation only; no commands were run.
