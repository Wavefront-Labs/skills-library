---
id: computing-software.robotics-software.ros2-core.qos-compatibility
name: qos-compatibility
category: computing-software
field: robotics-software
product: ros2-core
tags: [qos-compatibility, incompatible-qos, qos-events, qos-override, ros2-topic-info-verbose]
level: advanced
status: docs-checked
description: "Diagnose QoS incompatibility between publishers and subscribers with topic info -v and QoS events."
sources:
  - https://github.com/ros2/ros2_documentation/blob/rolling/source/ROS-Framework/interfaces/topics/About-Quality-of-Service-Settings.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# QoS compatibility
Rule: a subscriber's request must be no stricter than the publisher's offer.

| Publisher offers | Subscriber requests | Connects? |
|---|---|---|
| reliable | reliable / best_effort | yes |
| best_effort | reliable | no |
| volatile | transient_local | no |
| transient_local | either | yes |

- Diagnose: publishers get an "offered incompatible QoS" event and subscriptions a "requested incompatible QoS" event; handle them with QoS event callbacks.
- Override at node startup: a node that opts in declares read-only parameters named `qos_overrides.<topic_name>.<entity_type>[_<id>].<policy_name>`, set from YAML or command-line arguments.
- Matching deadlines/liveliness must also be compatible.

## Gotchas
- When profiles are incompatible no connection is made and no messages pass between the publisher and the subscription.
- Every policy that affects compatibility must be compatible; a compatible reliability does not rescue an incompatible durability.

## Checked
2026-11-02. Confirmed in About-Quality-of-Service-Settings (ros2_documentation, rolling): request-versus-offer rule, reliability and durability compatibility tables, deadline and liveliness compatibility, incompatible-QoS events, qos_overrides parameter structure. Removed the `ros2 topic info -v` diagnostic, the `qos_overrides./topic.publisher.reliability` example and the RViz and bag claims (not in the docs read).
Method: documentation only; no commands were run.

## Self-check
After changing the subscriber to best_effort, `ros2 topic hz` shows data and no incompatibility warning.
