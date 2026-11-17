---
id: computing-software.robotics-software.moveit-manipulation.moveit-config-files
name: moveit-config-files
category: computing-software
field: robotics-software
product: moveit-manipulation
tags: [moveit-config-files, joint-limits-yaml, kinematics-yaml, moveit-controllers-yaml, moveit-config-builder, acceleration-limits]
level: advanced
status: docs-checked
description: "Edit key MoveIt config files and load them with MoveItConfigsBuilder in launch."
sources:
  - https://moveit.picknik.ai/main/index.html
  - https://github.com/moveit/moveit2
  - https://github.com/moveit/moveit2_tutorials
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# MoveIt config files
- `joint_limits.yaml`: per joint `has_velocity_limits`, `max_velocity`, `has_acceleration_limits`, `max_acceleration`; MoveIt needs acceleration limits for time parameterization (URDF has none).
- `moveit_controllers.yaml`: `moveit_simple_controller_manager` maps controller names to action namespaces/type (`FollowJointTrajectory`) and joints.
- Launch loading:
```python
from moveit_configs_utils import MoveItConfigsBuilder
cfg = MoveItConfigsBuilder("my_robot", package_name="my_robot_moveit_config").to_moveit_configs()
Node(package="moveit_ros_move_group", executable="move_group", parameters=[cfg.to_dict()])
```
- Pass `use_sim_time` and the same `robot_description` as the controllers use.
- Parameter file merging: `to_dict()` includes robot_description, robot_description_semantic, kinematics, planning pipelines, trajectory execution.

## Gotchas
- Missing acceleration limits cause "No acceleration limit" errors during planning.
- Two different URDF copies (controllers vs MoveIt) drift apart.

## Self-check
`move_group` starts and loads the SRDF without errors.

## Checked
2026-11-03: parameter, plugin, API and command names compared with the MoveIt 2 sources (moveit2 repository headers, servo_parameters.yaml, servo_node.cpp, datatypes.hpp, moveit_py bindings; moveit2_tutorials pages for controller configuration, OMPL, Pilz, setup assistant and Bullet). Removed or corrected: the `ros2 param get` self-check.

Method: documentation only; no commands were run.
