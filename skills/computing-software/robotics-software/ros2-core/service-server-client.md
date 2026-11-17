---
id: computing-software.robotics-software.ros2-core.service-server-client
name: service-server-client
category: computing-software
field: robotics-software
product: ros2-core
tags: [service-server, create-service, create-client, call-async, srv, ros2-services]
level: practitioner
status: docs-checked
description: "Implement a ROS 2 service server and asynchronous client without blocking the executor."
sources:
  - https://github.com/ros2/ros2_documentation
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Service server and client
**Goal:** request/response RPC that does not deadlock.

```python
from example_interfaces.srv import AddTwoInts
self.create_service(AddTwoInts, 'add', lambda req, res: (setattr(res, 'sum', req.a + req.b), res)[1])
cli = self.create_client(AddTwoInts, 'add')
cli.wait_for_service(timeout_sec=2.0)
fut = cli.call_async(AddTwoInts.Request(a=1, b=2))
fut.add_done_callback(lambda f: self.get_logger().info(str(f.result().sum)))
```
- Prefer `call_async`: the Python synchronous `call()` can block and deadlock (for example when called from a timer callback, or when nothing spins in another thread), so the docs do not recommend it.
- Servers should be short; long work belongs in an action.

## Gotchas
- Calling a synchronous `call()` from a callback on a single-threaded executor deadlocks.
- Check the `wait_for_service` result before calling.

## Self-check
`ros2 service call /add example_interfaces/srv/AddTwoInts "{a: 1, b: 2}"` returns sum 3.

## Checked
2026-11-03. Confirmed in ros2_documentation (Writing-A-Simple-Py-Service-And-Client, Custom-ROS2-Interfaces, Sync-Vs-Async): `example_interfaces.srv.AddTwoInts`, `create_service`, `create_client`, `wait_for_service(timeout_sec=...)`, `call_async`, deadlock from `call()`. Removed: the `spin_until_future_complete` rule and the hanging-future claim. The inline lambda is illustrative.
Method: documentation only; no commands were run.
