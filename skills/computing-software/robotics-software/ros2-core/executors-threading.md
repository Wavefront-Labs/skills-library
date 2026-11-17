---
id: computing-software.robotics-software.ros2-core.executors-threading
name: executors-threading
category: computing-software
field: robotics-software
product: ros2-core
tags: [executors, single-threaded-executor, multi-threaded-executor, spin-some, static-executor, ros2-executors]
level: advanced
status: docs-checked
description: "Choose SingleThreaded or MultiThreaded executors and understand callback ordering and blocking."
sources:
  - https://github.com/ros2/ros2_documentation/blob/rolling/source/ROS-Framework/client-libraries/About-Executors/About-Executors.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Executors
**Goal:** know which thread runs which callback.

- `rclcpp::spin(node)` / `rclpy.spin(node)` use the default single-threaded executor: callbacks run one at a time, so one slow callback delays all.
- Multi-thread: `rclcpp::executors::MultiThreadedExecutor exec; exec.add_node(n); exec.spin();`.
- Several nodes can share one executor (`add_node`), also in composed containers.
- Manual control: `spin_once`, `spin_some`, `spin_until_future_complete`.

## Gotchas
- Blocking calls (sleep, synchronous service call) in a callback stall everything on a single-threaded executor.
- Mutually exclusive callbacks in one group are still serialized under a multi-threaded executor.

## Checked
2026-11-02. Confirmed in About-Executors (ros2_documentation, rolling): spin uses the Single-Threaded Executor, the multi-threaded executor processes events in parallel threads, add_node for several nodes, container processes use a single-threaded executor. Removed the Python num_threads call and the events executor line (not in the docs read).
Method: documentation only; no commands were run.

## Self-check
A 2 s sleeping timer does not block a 10 Hz subscriber after moving them to separate callback groups with a multi-threaded executor.
