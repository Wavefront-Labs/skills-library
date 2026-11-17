---
id: computing-software.robotics-software.ros2-core.tf2-lookup
name: tf2-lookup
category: computing-software
field: robotics-software
product: ros2-core
tags: [tf2-lookup, tf-buffer, transform-listener, lookup-transform, extrapolation-exception, tf2-geometry-msgs]
level: advanced
status: docs-checked
description: "Look up transforms with tf2_ros Buffer and TransformListener and handle time, timeouts and extrapolation."
sources:
  - https://github.com/ros2/ros2_documentation
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# tf2 lookup
```python
import rclpy.time
from tf2_ros import TransformException
from tf2_ros.buffer import Buffer
from tf2_ros.transform_listener import TransformListener
self.tf_buffer = Buffer(); self.tf_listener = TransformListener(self.tf_buffer, self)
try:
    t = self.tf_buffer.lookup_transform('map', 'base_link', rclpy.time.Time())   # Time() = latest
except TransformException as ex:
    self.get_logger().info(str(ex))
```
- Arguments are target frame, source frame, time; `Time()` returns the latest available transform.
- The listener buffers transforms for up to 10 seconds.
- A timeout (optional last argument of `lookupTransform` in the C++ tutorial) makes the call wait for the transform instead of failing at once.

## Gotchas
- Lookup right after starting the listener can fail because nothing is buffered yet; use a timer or a timeout.

## Self-check
`ros2 run tf2_ros tf2_echo map base_link` matches your node's lookup result.

## Checked
2026-11-03. Confirmed in the ros2_documentation tf2 tutorials (Writing-A-Tf2-Listener-Py, Learning-About-Tf2-And-Time-Cpp): imports, `lookup_transform(target, source, time)`, `Time()` = latest, 10 s buffer, timeout argument, `TransformException`. Removed: Python `timeout=` keyword with `Duration`, `Buffer.transform`/`tf2_geometry_msgs`, `can_transform`, the exception subclass list, `use_sim_time` and stamp advice (not in the pages read). `tf2_echo` confirmed in Debugging-Tf2-Problems.
Method: documentation only; no commands were run.
