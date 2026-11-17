---
id: computing-software.robotics-software.ros2-core.intra-process-comms
name: intra-process-comms
category: computing-software
field: robotics-software
product: ros2-core
tags: [intra-process, zero-copy, unique-ptr, loaned-messages, use-intra-process-comms]
level: advanced
status: docs-checked
description: "Enable intra-process communication and zero-copy publishing with unique_ptr messages in rclcpp."
sources:
  - https://github.com/ros2/ros2_documentation/blob/rolling/source/ROS-Framework/nodes/Working-with-nodes/intra-process/Intra-Process-Communication.rst
  - https://github.com/ros2/ros2_documentation/blob/rolling/source/ROS-Framework/nodes/Working-with-nodes/Composition.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Intra-process communication
- Enable per node: `rclcpp::NodeOptions().use_intra_process_comms(true)` (or the composable-node `extra_arguments`).
- Publish a `std::unique_ptr` message so ownership moves instead of copying.
- A `UniquePtr` subscriber callback receives the same message address as was published (zero-copy). A `ConstSharedPtr` callback stays zero-copy with several subscribers as long as a `std::unique_ptr` was published; a `shared_ptr` callback is zero-copy only while it is the sole subscriber.
- Intra-process communication helps when several nodes run in the same process.
- Loaned messages and zero-copy data sharing are a separate mechanism; see the Configure ZeroCopy loaned messages page for RMW support and environment variables.

## Gotchas
- Never touch a message after `std::move` publishing.

## Checked
2026-11-02. Confirmed in Intra-Process-Communication and Composition (ros2_documentation, rolling): use_intra_process_comms(true), unique_ptr ownership transfer, UniquePtr/ConstSharedPtr/shared_ptr callback copy behaviour, composable-node extra argument use_intra_process_comms. Removed the QoS requirement list, borrow_loaned_message and the ros2 topic echo visibility claim (not in the docs read).
Method: documentation only; no commands were run.

## Self-check
A latency comparison of a large image topic shows lower copy cost with intra-process on.
