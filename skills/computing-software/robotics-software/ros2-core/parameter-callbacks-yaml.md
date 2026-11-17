---
id: computing-software.robotics-software.ros2-core.parameter-callbacks-yaml
name: parameter-callbacks-yaml
category: computing-software
field: robotics-software
product: ros2-core
tags: [parameter-callback, add-on-set-parameters-callback, params-file, wildcard, dynamic-reconfigure]
level: advanced
status: docs-checked
description: "Validate dynamic parameter changes with set-parameters callbacks and load YAML parameter files."
sources:
  - https://github.com/ros2/ros2_documentation/blob/rolling/source/Migration-and-Upgrades/Migrating-from-ROS1/Migrating-Parameters.rst
  - https://github.com/ros2/ros2_documentation/blob/rolling/source/ROS-Framework/parameters/Working-with-parameters/Understanding-ROS2-Parameters/Understanding-ROS2-Parameters.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Parameter callbacks and YAML files
```python
from rcl_interfaces.msg import SetParametersResult
self.add_on_set_parameters_callback(lambda ps: SetParametersResult(
    successful=all(p.value >= 0 for p in ps if p.name == 'speed')))
```
YAML file:
```yaml
/**:                       # wildcard: any node name / namespace
  ros__parameters:
    speed: 0.8
my_node:
  ros__parameters:
    frame_id: base_link
```
Load: `ros2 run pkg exe --ros-args --params-file params.yaml`; launch files pass parameters with the `parameters=` argument of `Node`.
- `add_on_set_parameters_callback` validates parameter changes; `add_post_set_parameters_callback` runs after they are applied.
- When migrating from ROS 1 `dynamic_reconfigure`, use the `set_parameters_atomically` service to validate and apply several parameters as one operation.
- When a parameter file is used at node startup, all parameters are updated, including the read-only ones.

## Gotchas
- Parameter values sit under a `ros__parameters` key (two underscores).

## Checked
2026-11-02. Confirmed in Migrating-Parameters and Understanding-ROS2-Parameters (ros2_documentation, rolling): add_on_set_parameters_callback and add_post_set_parameters_callback, set_parameters_atomically as the dynamic_reconfigure replacement, --params-file, ros__parameters key, parameter files update read-only parameters at startup. Removed the node-name matching rule, the reject-before-apply and reason-text claims, and the recursion gotcha (not in the docs read); the `/**` wildcard and ros__parameters layout are confirmed in Node-arguments.
Method: documentation only; no commands were run.

## Self-check
Setting an invalid value via `ros2 param set` is rejected with the reason text.
