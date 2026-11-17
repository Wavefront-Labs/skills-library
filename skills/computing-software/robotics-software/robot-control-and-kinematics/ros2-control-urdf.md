---
id: computing-software.robotics-software.robot-control-and-kinematics.ros2-control-urdf
name: ros2-control-urdf
category: computing-software
field: robotics-software
product: robot-control-and-kinematics
tags: [ros2-control-urdf, ros2-control-tag, command-interface, state-interface, hardware-plugin, mock-components]
level: practitioner
status: docs-checked
description: "Declare hardware, joints, and command/state interfaces in the URDF ros2_control tag."
sources:
  - https://github.com/ros-controls/ros2_control/blob/master/hardware_interface/doc/hardware_interface_types_userdoc.rst
  - https://github.com/ros-controls/ros2_control/blob/master/hardware_interface/doc/mock_components_userdoc.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# ros2_control URDF tag
```xml
<ros2_control name="arm" type="system">
  <hardware><plugin>mock_components/GenericSystem</plugin></hardware>
  <joint name="joint1">
    <command_interface name="position"><param name="min">-3.14</param><param name="max">3.14</param></command_interface>
    <state_interface name="position"><param name="initial_value">0.0</param></state_interface>
    <state_interface name="velocity"/>
  </joint>
</ros2_control>
```
- `type` is `system`, `actuator` or `sensor`. The plugin is your hardware class or `mock_components/GenericSystem` for mock hardware.
- Interface names include `position`, `velocity`, `effort` and `acceleration`; command interfaces take `min`/`max` params and state interfaces take `initial_value`.
- All joints in the `<ros2_control>` tag must be present in the URDF received by the controller manager.

## Gotchas
- Joint names must match the URDF joints.

## Self-check
`ros2 control list_hardware_interfaces` lists the joint's command and state interfaces, shown `[unclaimed]` before a controller starts.

## Checked
2026-11-03. Confirmed in the ros2_control repo docs (hardware_interface_types_userdoc: `<ros2_control name type="system">`, `command_interface` with `min` param, joints must be in the URDF; mock_components_userdoc: plugin name, `initial_value`, interface names; ros2controlcli userdoc: `list_hardware_interfaces` output with `[unclaimed]`). Removed: `fake_components` rename, Gazebo plugin, xacro advice, `robot_description` source claim, NaN default claim (not in pages read).
Method: documentation only; no commands were run.
