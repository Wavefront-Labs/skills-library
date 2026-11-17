---
id: computing-software.robotics-software.ros2-core.service-cli
name: service-cli
category: computing-software
field: robotics-software
product: ros2-core
tags: [service-cli, ros2-service, service-call, service-type, service-list]
level: intro
status: docs-checked
description: "Discover and call services from the command line with ros2 service list, type, find and call."
sources:
  - https://github.com/ros2/ros2cli/tree/rolling/ros2service/ros2service/verb
  - https://github.com/ros2/ros2_documentation/blob/rolling/source/ROS-Framework/interfaces/About-Services.rst
  - https://github.com/ros2/ros2_documentation/blob/rolling/source/ROS-Framework/interfaces/About-Interfaces.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# ros2 service CLI
```bash
ros2 service list -t
ros2 service type /add
ros2 service find example_interfaces/srv/AddTwoInts
ros2 interface show example_interfaces/srv/AddTwoInts
ros2 service call /add example_interfaces/srv/AddTwoInts "{a: 1, b: 2}"
```
- The `ros2 service` verbs are `call`, `echo`, `find`, `info`, `list` and `type`. `list -t` (`--show-types`) prints the type next to each name; `find -c` only prints the count; `find --include-hidden-services` also considers hidden services; `call -r N` repeats the call at a rate; `call` takes the request values as a YAML string.
- By default services use reliable QoS with volatile durability.

## Gotchas
- `ros2 service call` against a missing service prints `waiting for service to become available...` and keeps waiting; press Ctrl+C to abort.
- Quote YAML so the shell does not split braces and spaces.

## Self-check
`ros2 service call` returns a response; `ros2 service list` shows the server's service.

## Checked
2026-11-03. Confirmed in the ros2cli `ros2service` verbs (names, `-t/--show-types`, `find` options, `call --rate` and YAML argument, the "waiting for service" message) and the ROS 2 QoS page (services are reliable with volatile durability). Removed: the claim that omitted request fields take defaults and the unconfirmed version remark on service introspection.
Method: documentation only; no commands were run.
