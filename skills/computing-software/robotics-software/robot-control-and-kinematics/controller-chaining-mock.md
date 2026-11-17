---
id: computing-software.robotics-software.robot-control-and-kinematics.controller-chaining-mock
name: controller-chaining-mock
category: computing-software
field: robotics-software
product: robot-control-and-kinematics
tags: [controller-chaining, chained-controllers, reference-interfaces, mock-hardware, fake-hardware, command-forwarding]
level: advanced
status: docs-checked
description: "Test with mock hardware and chain controllers through reference interfaces."
sources:
  - https://github.com/ros-controls/ros2_control/blob/master/controller_manager/doc/controller_chaining.rst
  - https://github.com/ros-controls/ros2_control/blob/master/hardware_interface/doc/mock_components_userdoc.rst
  - https://github.com/ros-controls/ros2_control/blob/master/ros2controlcli/doc/userdoc.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Mock hardware and chaining
- `mock_components/GenericSystem` mirrors commands to states (optional hardware params include `mock_sensor_commands`, `calculate_dynamics` and `disable_commands`, all default false); use it to test controllers, launch files and integrations without hardware.
- Controller chaining: a following controller exports reference interfaces (named like `<controller_name>/v_x`); a preceding controller claims them as its command interfaces instead of hardware. A controller exposing reference interfaces switches to chained mode only while another controller uses them.
- Chained controllers must be activated and deactivated together or in the proper order; the `spawner` option `--activate-as-group` activates a whole chain in one call.
- `ros2 control switch_controllers` takes `--activate`, `--deactivate` and `--strict`.

## Gotchas
- Mock states mirror commands (ideal behaviour), so they hide real tracking error.

## Self-check
Activating the chain moves the mock joints.

## Checked
2026-11-03. Confirmed in the ros2_control repo docs (controller_chaining, mock_components_userdoc, ros2controlcli userdoc). Fixed: `--strictness STRICT` does not exist on `switch_controllers`; the flag is `--strict`. Removed: ForwardCommandController parameter details, start-order claim, Gazebo and interface-claim gotchas, deactivation self-check (not in pages read).
Method: documentation only; no commands were run.
