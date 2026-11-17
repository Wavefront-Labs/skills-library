---
id: computing-software.robotics-software.ros2-core.launch-python
name: launch-python
category: computing-software
field: robotics-software
product: ros2-core
tags: [launch-python, launch-description, node-action, generate-launch-description, remappings, ros2-launch]
level: practitioner
status: docs-checked
description: "Write Python launch files with LaunchDescription, Node actions, parameters, remappings and namespaces."
sources:
  - https://github.com/ros2/ros2_documentation/blob/rolling/source/Developer-Tools/Launch/Creating-Launch-Files.rst
  - https://github.com/ros2/ros2_documentation/blob/rolling/source/Developer-Tools/Launch/Launch-file-different-formats.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Python launch files
```python
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(package='demo_nodes_cpp', executable='talker', name='talker', namespace='robot1',
             parameters=[{'use_sim_time': False}],
             remappings=[('chatter', 'out')], output='screen'),
    ])
```
Run: `ros2 launch <package_name> <launch_file_name>` or `ros2 launch <path_to_launch_file>`; launch arguments are passed as `name:=value`.
- Include other launch files with `IncludeLaunchDescription`.
- Group actions with `GroupAction`.

## Gotchas
- Launch arguments are strings.

## Checked
2026-11-02. Confirmed in Creating-Launch-Files and Launch-file-different-formats (ros2_documentation, rolling): Node action arguments (package, executable, name, namespace, parameters, remappings, output), ros2 launch forms, name:=value arguments, IncludeLaunchDescription, GroupAction. Removed install steps, PythonLaunchDescriptionSource, PushRosNamespace and the unique-name rule (not in the docs read).
Method: documentation only; no commands were run.

## Self-check
`ros2 launch` starts all nodes; `ros2 node list` shows the namespaced names.
