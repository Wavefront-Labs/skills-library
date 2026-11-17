---
id: computing-software.robotics-software.ros2-core.callback-groups
name: callback-groups
category: computing-software
field: robotics-software
product: ros2-core
tags: [callback-groups, mutually-exclusive, reentrant, callback-group, deadlock]
level: advanced
status: docs-checked
description: "Use MutuallyExclusive and Reentrant callback groups to avoid deadlocks and enable parallelism."
sources:
  - https://github.com/ros2/ros2_documentation/blob/rolling/source/ROS-Framework/nodes/Working-with-nodes/Using-callback-groups.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Callback groups
- Default: each node has one MutuallyExclusive group; callbacks in it never run concurrently.
- Reentrant: callbacks (even the same one) may run concurrently; you must make the code thread-safe.
```python
from rclpy.callback_groups import ReentrantCallbackGroup, MutuallyExclusiveCallbackGroup
cb = MutuallyExclusiveCallbackGroup()
self.create_timer(1.0, self.tick, callback_group=cb)
self.cli = self.create_client(Srv, 'x', callback_group=ReentrantCallbackGroup())
```
- Pattern: a timer that calls a service synchronously needs the client in a different group and a MultiThreadedExecutor.
- C++: `create_callback_group(rclcpp::CallbackGroupType::Reentrant)` and assign it through `rclcpp::SubscriptionOptions` (`options.callback_group`).

## Gotchas
- Groups only help under a multi-threaded executor.
- Shared state across reentrant callbacks needs a mutex.

## Checked
2026-11-02. Confirmed in Using-callback-groups (ros2_documentation, rolling): default group is Mutually Exclusive, Reentrant semantics, Python callback_group argument and group classes, C++ create_callback_group and SubscriptionOptions, deadlocks from synchronous calls, groups matter under a Multi-Threaded Executor. Removed PublisherOptions (not in the page).
Method: documentation only; no commands were run.

## Self-check
A callback holding a service wait completes instead of deadlocking.
