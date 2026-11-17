---
id: computing-software.robotics-software.ros2-core.action-cli
name: action-cli
category: computing-software
field: robotics-software
product: ros2-core
tags: [action-cli, ros2-action, send-goal, action-info, action-list]
level: intro
status: docs-checked
description: "Use ros2 action list, info, send_goal and type to inspect and test actions."
sources:
  - https://github.com/ros2/ros2_documentation/blob/rolling/source/ROS-Framework/interfaces/actions/Working-with-actions/Understanding-ROS2-Actions/Understanding-ROS2-Actions.rst
  - https://github.com/ros2/ros2_documentation/blob/rolling/source/ROS-Framework/interfaces/actions/Working-with-actions/Action-Introspection.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# ros2 action CLI
```bash
ros2 action list -t
ros2 action type /fib
ros2 action info /fib                   # clients and servers
ros2 action info /fib --verbose
ros2 action echo /fib example_interfaces/action/Fibonacci --flow-style
```
- An action is implemented by five services and topics: the goal, cancel and result services, and the feedback and status topics.
- `ros2 action list -t` shows each action name followed by its type in brackets.

## Gotchas
- `ros2 action type` prints the type of a named action.

## Checked
2026-11-02. Confirmed in Understanding-ROS2-Actions and Action-Introspection (ros2_documentation, rolling): ros2 action list -t, type, info, info --verbose, echo with --flow-style, the five services and topics behind an action. Removed send_goal usage and cancel behaviour, goal/result/feedback layout and the error text (not in the docs read).
Method: documentation only; no commands were run.

## Self-check
`ros2 action list -t` shows `/fib` with its type, and `ros2 action info /fib` reports one server.
