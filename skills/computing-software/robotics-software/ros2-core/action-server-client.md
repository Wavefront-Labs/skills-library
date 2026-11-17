---
id: computing-software.robotics-software.ros2-core.action-server-client
name: action-server-client
category: computing-software
field: robotics-software
product: ros2-core
tags: [action-server, rclcpp-action, rclpy-action, goal-handle, feedback, cancel, ros2-actions]
level: advanced
status: docs-checked
description: "Write an action server and client with goals, feedback, results and cancellation."
sources:
  - https://github.com/ros2/ros2_documentation/blob/rolling/source/ROS-Framework/interfaces/actions/Working-with-actions/Writing-an-Action-Server-Client/Py.rst
  - https://github.com/ros2/ros2_documentation/blob/rolling/source/ROS-Framework/interfaces/actions/Working-with-actions/Writing-an-Action-Server-Client/Cpp.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Action server and client
**Goal:** long-running tasks with progress and cancel.

```python
from rclpy.action import ActionServer, ActionClient
from example_interfaces.action import Fibonacci
ActionServer(self, Fibonacci, 'fib', self.execute)         # execute(goal_handle) -> Result
# inside execute: goal_handle.publish_feedback(fb); goal_handle.succeed(); return the result
client = ActionClient(self, Fibonacci, 'fib')
send = client.send_goal_async(goal, feedback_callback=cb)   # then get_result_async on the accepted handle
```
- The server's execute callback runs once a goal is accepted; the goal handle's `publish_feedback()` sends feedback.
- The client's `send_goal_async()` returns a future to a goal handle; call `get_result_async()` on that handle for the result.
- The C++ version uses the `rclcpp_action` package.

## Gotchas
- If the goal handle state is not set in the execute callback, the goal is assumed aborted.

## Checked
2026-11-02. Confirmed in the Python and C++ action server/client tutorials (ros2_documentation, rolling): ActionClient, execute callback after acceptance, publish_feedback, send_goal_async, get_result_async, default aborted state, rclcpp_action. Removed the lifecycle chain, cancel-check calls, create_server naming, and the executor claims (not in the docs read).
Method: documentation only; no commands were run.

## Self-check
`ros2 action send_goal /fib example_interfaces/action/Fibonacci "{order: 5}" --feedback` prints feedback and a result.
