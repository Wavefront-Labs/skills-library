---
id: computing-software.robotics-software.ros2-core.interface-cli-types
name: interface-cli-types
category: computing-software
field: robotics-software
product: ros2-core
tags: [interface-cli, ros2-interface, interface-show, interface-proto, builtin-types]
level: intro
status: docs-checked
description: "Explore standard interface packages and field types with ros2 interface list, show and proto."
sources:
  - https://github.com/ros2/ros2cli/tree/rolling/ros2interface
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# ros2 interface CLI
```bash
ros2 interface list | grep geometry_msgs
ros2 interface show geometry_msgs/msg/PoseStamped
ros2 interface proto sensor_msgs/msg/Imu          # YAML skeleton for pub/call
ros2 interface package std_msgs
```
- Use standard types before inventing new ones; check `ros2 interface list` first.
- `ros2 interface proto` prints a YAML prototype of a message (`--no-quotes` drops the outer quotes).

## Gotchas
- Types without a `header` field cannot carry a timestamp or frame id; prefer purpose-built types.

## Self-check
`ros2 interface proto` output can be pasted into `ros2 topic pub` unchanged.

## Checked
2026-11-03. Confirmed in the ros2cli source (`ros2interface` verbs `proto` with `--no-quotes`, and `package`) and ros2_documentation (`ros2 interface show` in the topics tutorial). Removed: list of standard packages, field-type list, header/tf and loaned-message claims (not in the pages read).
Method: documentation only; no commands were run.
