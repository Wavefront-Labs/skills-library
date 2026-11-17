---
id: computing-software.robotics-software.ros2-core.qos-profiles
name: qos-profiles
category: computing-software
field: robotics-software
product: ros2-core
tags: [qos-profiles, reliability, durability, history-depth, sensor-data-qos, transient-local, ros2-qos]
level: practitioner
status: docs-checked
description: "Pick QoS reliability, durability, history, deadline and lifespan; use sensor-data and transient-local profiles."
sources:
  - https://github.com/ros2/ros2_documentation/blob/rolling/source/ROS-Framework/interfaces/topics/About-Quality-of-Service-Settings.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# QoS profiles
**Goal:** choose policies per data type.

| Policy | Values |
|---|---|
| Reliability | reliable, best_effort |
| Durability | volatile, transient_local |
| History | keep_last(depth), keep_all |
| Deadline / Lifespan | durations; "default" means unspecified |
| Liveliness | automatic or manual by topic, with a lease duration |

- Defaults for publishers and subscriptions: keep last with a queue size of 10, reliable, volatile, system default liveliness. Services are reliable too. The sensor data profile uses best effort reliability and a smaller queue size. The system default profile uses the RMW implementation's values.
- Latched-like behaviour (maps, robot description): `transient_local` durability with any depth; the publisher and the subscriber must both use Transient Local for late subscribers to get old messages.

## Gotchas
- On lossy wireless networks a best effort policy is more suitable than reliable.

## Checked
2026-11-02. Confirmed in About-Quality-of-Service-Settings (ros2_documentation, rolling): policy list, defaults (keep last 10, reliable, volatile), services reliable, sensor data profile best effort with smaller queue, transient local agreement for late subscribers. Removed the rclpy code block, the named profile constants, depth 1, the Wi-Fi image claim and the keep_all memory claim (not in the docs read).
Method: documentation only; no commands were run.

## Self-check
A late subscriber with transient_local receives the last `/map` message immediately.
