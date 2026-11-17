---
id: computing-software.robotics-software.ros2-core.topic-cli
name: topic-cli
category: computing-software
field: robotics-software
product: ros2-core
tags: [topic-cli, ros2-topic, topic-echo, topic-hz, topic-pub]
level: intro
status: docs-checked
description: "Inspect and drive topics with ros2 topic list, info, echo, hz, bw and pub."
sources:
  - https://github.com/ros2/ros2cli/tree/rolling/ros2topic
  - https://github.com/ros2/ros2_documentation
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# ros2 topic CLI
**Goal:** debug data flow without writing code.

```bash
ros2 topic list -t                      # names with types
ros2 topic info /scan -v                # publishers, subscribers, QoS of each
ros2 topic echo /scan --once            # one message
ros2 topic hz /scan ; ros2 topic bw /scan
ros2 topic pub -r 1 /cmd_vel geometry_msgs/msg/Twist "{linear: {x: 0.1}}"
ros2 topic echo /scan --qos-reliability best_effort   # match a sensor-data publisher
```
- If a subscriber shows nothing, check the endpoint QoS with `ros2 topic info -v` and set QoS flags such as `--qos-reliability` on `echo`.
- `pub` has `-r`/`--rate` (default 1.0) and `-1`/`--once`.

## Gotchas
- `topic bw` measures the receiving rate on its own subscription, which QoS and platform load can affect.
- Run with the same `ROS_DOMAIN_ID` as the robot.

## Self-check
`ros2 topic hz` reports the expected rate for a known publisher.

## Checked
2026-11-03. Confirmed in ros2_documentation (Understanding-ROS2-Topics: `list -t`, `info --verbose`, `bw`, `--qos-reliability`) and the ros2cli source (`echo --once` and QoS arguments, `pub -r/--rate` and `-1/--once`, `hz`). Removed: default-reliable subscriber claim and discovery-wait advice. Note: `-v` for `topic info` is shown in the QoS-overrides tutorial.
Method: documentation only; no commands were run.
