---
id: computing-software.robotics-software.ros2-core.lifecycle-states
name: lifecycle-states
category: computing-software
field: robotics-software
product: ros2-core
tags: [lifecycle-states, lifecycle-node, on-configure, on-activate, primary-states, transitions, ros2-lifecycle]
level: advanced
status: docs-checked
description: "Implement a lifecycle node with configure, activate, deactivate and cleanup transitions."
sources:
  - https://design.ros2.org/articles/node_lifecycle.html
  - https://github.com/ros2/demos/tree/rolling/lifecycle
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Lifecycle node states
**Goal:** deterministic start-up and teardown.

- Primary states: unconfigured, inactive, active, finalized. Transitions: configure, activate, deactivate, cleanup, shutdown. A callback that succeeds moves the node to its target state; a failure code or any other result sends it to ErrorProcessing (configure failure returns to unconfigured).
- C++: derive from `rclcpp_lifecycle::LifecycleNode`, override `on_configure`, `on_activate`, `on_deactivate`, `on_cleanup`, `on_shutdown`.
- Create publishers/subscribers/timers in `on_configure`; the lifecycle demo only publishes while the node is active (its `on_activate` activates the publisher and timer, `on_deactivate` stops them).
- `on_error` runs in ErrorProcessing; if it succeeds the node returns to unconfigured, otherwise it goes to finalized.
- Finalized is terminal; shutdown can be entered from any primary state except finalized.

## Gotchas
- Do lengthy preparation in configure, not `on_activate` (the design says activation should avoid long-running work).
- A publisher that is not activated publishes nothing.

## Self-check
Node starts unconfigured; after `configure` and `activate` it publishes; after `deactivate` it stops.

## Checked
2026-11-03. Confirmed in the ROS 2 managed-nodes design article and the ros2/demos lifecycle README: primary states, transitions, callback names, configure failure to unconfigured, ErrorProcessing/onError, shutdown rule, `rclcpp_lifecycle::LifecycleNode`, publish only when active. Removed: `rclpy.lifecycle.Node` claim and SUCCESS/FAILURE/ERROR return-name list (not in pages read), real-time allocation claim (replaced by the design wording).
Method: documentation only; no commands were run.
