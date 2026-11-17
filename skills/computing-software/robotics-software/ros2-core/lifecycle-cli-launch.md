---
id: computing-software.robotics-software.ros2-core.lifecycle-cli-launch
name: lifecycle-cli-launch
category: computing-software
field: robotics-software
product: ros2-core
tags: [lifecycle-cli, ros2-lifecycle, lifecycle-set, lifecycle-get, lifecycle-nodes, lifecycle-manager]
level: practitioner
status: docs-checked
description: "Drive lifecycle nodes with ros2 lifecycle and launch-time transitions."
sources:
  - https://github.com/ros2/demos/tree/rolling/lifecycle
  - https://github.com/ros2/ros2cli/tree/rolling/ros2lifecycle
  - https://github.com/ros-navigation/docs.nav2.org/blob/rolling/docs/configuration_and_development/configuration_guide/core_servers/configuring_lifecycle_manager.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Driving lifecycle nodes
```bash
ros2 lifecycle nodes
ros2 lifecycle get /my_node
ros2 lifecycle list /my_node            # available transitions
ros2 lifecycle set /my_node configure
ros2 lifecycle set /my_node activate
```
- Nav2 uses a lifecycle manager with `autostart` and `node_names` parameters to bring up a list of nodes in order.
- The design makes each supervisory transition a service, and publishes state changes on a latched `lifecycle_state` topic.

## Gotchas
- Order matters; activate dependencies first and tear down in reverse.

## Self-check
`ros2 lifecycle get` reports `active` after both transitions.

## Checked
2026-11-03. Confirmed in the ros2/demos lifecycle README (`ros2 lifecycle get/set/list`), the ros2cli `nodes` verb, the managed-nodes design article (services per transition, `lifecycle_state` topic) and the Nav2 lifecycle manager page (`autostart`, `node_names`). Removed: launch event API line, `change_state` service name, `[3]` state id, non-lifecycle-node claim (not in pages read).
Method: documentation only; no commands were run.
