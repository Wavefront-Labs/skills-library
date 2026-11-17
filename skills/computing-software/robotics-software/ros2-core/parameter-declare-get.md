---
id: computing-software.robotics-software.ros2-core.parameter-declare-get
name: parameter-declare-get
category: computing-software
field: robotics-software
product: ros2-core
tags: [parameter-declare, declare-parameter, get-parameter, parameter-descriptor, ros2-param, ros2-parameters]
level: practitioner
status: docs-checked
description: "Declare typed node parameters with defaults and descriptors, and read or set them with ros2 param."
sources:
  - https://github.com/ros2/ros2_documentation/blob/rolling/source/ROS-Framework/client-libraries/Working-with-Client-Libraries/Using-Parameters-In-A-Class-Python.rst
  - https://github.com/ros2/ros2_documentation/blob/rolling/source/ROS-Framework/parameters/Working-with-parameters/Using-ros2-param.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Declaring and using parameters
**Goal:** configurable nodes without recompiling.

```python
self.declare_parameter('speed', 0.5)               # type inferred from default
speed = self.get_parameter('speed').value
```
```bash
ros2 param list /tick ; ros2 param get /tick speed
ros2 param set /tick speed 1.0
ros2 param dump /tick
ros2 param load /tick tick.yaml
```
- Parameters must be declared unless the node is created with `allow_undeclared_parameters` set to true.
- Use `ParameterDescriptor` for a description and constraints such as read-only or a range.
- Read-only parameters can be set at node startup but not afterwards.
- Values passed to `ros2 param set` use YAML syntax.

## Gotchas
- A parameter that was not declared cannot be got or set unless undeclared parameters are allowed.

## Checked
2026-11-02. Confirmed in Using-Parameters-In-A-Class-Python and Using-ros2-param (ros2_documentation, rolling): declare_parameter with default, ParameterDescriptor with description, read-only and range constraints, allow_undeclared_parameters, ros2 param list/get/set/dump/load, YAML syntax for set values, read-only at startup only. Removed the C++ one-liner, the type-fixed and int-for-double claims, FloatingPointRange and the launch-override gotcha (not in the docs read).
Method: documentation only; no commands were run.

## Self-check
`ros2 param set` changes behaviour and `ros2 param get` returns the new value.
