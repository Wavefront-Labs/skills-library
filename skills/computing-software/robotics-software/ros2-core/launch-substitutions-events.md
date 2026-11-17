---
id: computing-software.robotics-software.ros2-core.launch-substitutions-events
name: launch-substitutions-events
category: computing-software
field: robotics-software
product: ros2-core
tags: [launch-substitutions, declare-launch-argument, launch-configuration, event-handler, on-exit, opaque-function]
level: advanced
status: docs-checked
description: "Use launch arguments, substitutions, conditions, event handlers and OpaqueFunction."
sources:
  - https://github.com/ros2/ros2_documentation/blob/rolling/source/Developer-Tools/Launch/Using-Substitutions.rst
  - https://github.com/ros2/ros2_documentation/blob/rolling/source/Developer-Tools/Launch/Using-Event-Handlers.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Substitutions, conditions and events
```python
from launch.actions import DeclareLaunchArgument, RegisterEventHandler
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch.conditions import IfCondition
from launch_ros.substitutions import FindPackageShare
sim = LaunchConfiguration('sim')
DeclareLaunchArgument('sim', default_value='false')
Node(..., condition=IfCondition(sim))
PathJoinSubstitution([FindPackageShare('my_pkg'), 'config', 'p.yaml'])
```
- `LaunchConfiguration` reads the value of a launch argument anywhere in the launch description; `DeclareLaunchArgument` defines it.
- `RegisterEventHandler` takes event handlers such as `OnProcessStart`, `OnProcessIO`, `OnExecutionComplete`, `OnProcessExit` and `OnShutdown`; see Using-Event-Handlers for the full example.

## Gotchas
- Conditions are evaluated inside `IfCondition` with substitutions such as `PythonExpression` or `EqualsSubstitution`.

## Checked
2026-11-02. Confirmed in Using-Substitutions and Using-Event-Handlers (ros2_documentation, rolling) and the DeclareLaunchArgument default_value usage in the URDF launch example: FindPackageShare, PathJoinSubstitution, LaunchConfiguration, IfCondition, PythonExpression, EqualsSubstitution, RegisterEventHandler and the five event handlers. Removed OpaqueFunction, --show-args, lazy-resolution and bool claims, and the OnProcessExit snippet (not in the docs read).
Method: documentation only; no commands were run.

## Self-check
`ros2 launch pkg file sim:=true` starts the conditional node; without it, not.
