---
id: computing-software.robotics-software.moveit-manipulation.moveit-setup-assistant
name: moveit-setup-assistant
category: computing-software
field: robotics-software
product: moveit-manipulation
tags: [setup-assistant, srdf, planning-groups, moveit-config-package, self-collisions, named-poses, moveit-setup]
level: practitioner
status: docs-checked
description: "Generate a MoveIt 2 config package with the Setup Assistant: planning groups, self-collisions, named poses and controllers."
sources:
  - https://moveit.picknik.ai/main/index.html
  - https://github.com/moveit/moveit2
  - https://github.com/moveit/moveit2_tutorials
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# MoveIt Setup Assistant
**Goal:** a `<robot>_moveit_config` package from a URDF.

```bash
sudo apt install ros-$ROS_DISTRO-moveit
ros2 launch moveit_setup_assistant setup_assistant.launch.py
```
Steps in the GUI: load the URDF/xacro; generate the self-collision matrix; add virtual joints (`world` to base); define planning groups (chain or joints with base/tip links); add named robot poses (e.g. `home`); add end effectors; configure controllers; set author info; generate the package.
Generated `config/` holds the SRDF, `kinematics.yaml`, `joint_limits.yaml`, `moveit_controllers.yaml`, `ros2_controllers.yaml`, planner configs; `launch/` has `demo.launch.py`, `move_group.launch.py`, `moveit_rviz.launch.py`.
- Test: `ros2 launch <robot>_moveit_config demo.launch.py`.
- Re-run the assistant after URDF changes (SRDF depends on link/joint names).

## Gotchas
- Self-collision sampling density/choices affect which links are disabled; review the result.
- Hand-edits to generated files are lost on regenerate unless the assistant is told to keep them.

## Self-check
Demo launch shows the interactive marker in RViz and planning succeeds between named poses.

## Checked
2026-11-03: parameter, plugin, API and command names compared with the MoveIt 2 sources (moveit2 repository headers, servo_parameters.yaml, servo_node.cpp, datatypes.hpp, moveit_py bindings; moveit2_tutorials pages for controller configuration, OMPL, Pilz, setup assistant and Bullet). Removed or corrected: the literal generated file list names.

Method: documentation only; no commands were run.
