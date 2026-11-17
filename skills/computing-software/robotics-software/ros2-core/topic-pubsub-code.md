---
id: computing-software.robotics-software.ros2-core.topic-pubsub-code
name: topic-pubsub-code
category: computing-software
field: robotics-software
product: ros2-core
tags: [topic-pubsub, publisher, subscriber, create-publisher, create-subscription, ros2-topics]
level: practitioner
status: docs-checked
description: "Create publishers and subscribers in rclcpp and rclpy with typed messages and queue depth."
sources:
  - https://github.com/ros2/ros2_documentation/blob/rolling/source/ROS-Framework/client-libraries/Working-with-Client-Libraries/Writing-A-Simple-Py-Publisher-And-Subscriber.rst
  - https://github.com/ros2/ros2_documentation/blob/rolling/source/ROS-Framework/interfaces/topics/About-Quality-of-Service-Settings.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Publisher and subscriber
**Goal:** typed, decoupled one-to-many data flow.

```python
from std_msgs.msg import String
pub = self.create_publisher(String, 'chatter', 10)           # 10 = queue size
self.create_subscription(String, 'chatter', self.on_msg, 10)
msg = String(); msg.data = 'hi'
pub.publish(msg)
```
- The last argument is the queue size, a required QoS setting that limits queued messages if a subscriber is not receiving them fast enough.
- By default publishers and subscriptions use "keep last" history with a queue size of 10, "reliable" reliability and "volatile" durability. The sensor data profile uses best effort and a smaller queue.
- Publishers and subscriptions with incompatible QoS profiles do not connect.

## Gotchas
- Mismatched QoS means no connection and no messages (the QoS page has the compatibility rules); compare the profiles with `ros2 topic info /chatter -v`.

## Self-check
`ros2 topic info /chatter -v` shows 1 publisher and 1 subscriber with compatible QoS.

## Checked
2026-11-03. Confirmed in the Python publisher/subscriber tutorial (`create_publisher(String, 'topic', 10)`, queue size) and the QoS page (default profile, sensor data profile, incompatible profiles prevent delivery). Removed: the C++ subscription lambda example, the namespace and remap advice, the callback-thread claim and the shared-pointer mutation warning.
Method: documentation only; no commands were run.
