---
id: computing-software.robotics-software.ros2-core.rclpy-node
name: rclpy-node
category: computing-software
field: robotics-software
product: ros2-core
tags: [rclpy-node, rclpy, python, setup-py, entry-points]
level: practitioner
status: docs-checked
description: "Write a ROS 2 node in Python with rclpy: Node subclass, timers, spin, entry points in setup.py."
sources:
  - https://github.com/ros2/ros2_documentation/blob/rolling/source/ROS-Framework/client-libraries/Working-with-Client-Libraries/Writing-A-Simple-Py-Publisher-And-Subscriber.rst
  - https://github.com/ros2/ros2_documentation/blob/rolling/source/ROS-Framework/client-libraries/Working-with-Client-Libraries/Creating-Your-First-ROS2-Package.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# rclpy node
**Goal:** a minimal Python node in an ament_python package.

```python
import rclpy
from rclpy.node import Node

class Tick(Node):
    def __init__(self):
        super().__init__('tick')
        self.create_timer(1.0, lambda: self.get_logger().info('tick'))

def main():
    rclpy.init()
    node = Tick()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()
```
`setup.py` declares the executable under `entry_points` with a `console_scripts` list. Declare the `rclpy` dependency in package.xml.

## Gotchas
- `setup.cfg` is required when a package has executables so that `ros2 run` can find them.

## Checked
2026-11-02. Confirmed in the Python publisher/subscriber tutorial and Creating-Your-First-ROS2-Package (ros2_documentation, rolling): rclpy.init/spin/Node/create_timer pattern, console_scripts entry point, setup.cfg requirement, rclpy dependency in package.xml. Removed try_shutdown, the "No executable found" message and the double-shutdown claim; the shutdown call is the plain rclpy.shutdown().
Method: documentation only; no commands were run.

## Self-check
`ros2 run my_pkg tick` logs each second and exits cleanly on Ctrl+C.
