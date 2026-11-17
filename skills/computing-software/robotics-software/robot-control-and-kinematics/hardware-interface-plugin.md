---
id: computing-software.robotics-software.robot-control-and-kinematics.hardware-interface-plugin
name: hardware-interface-plugin
category: computing-software
field: robotics-software
product: robot-control-and-kinematics
tags: [hardware-interface, system-interface, export-state-interfaces, read-write, pluginlib, lifecycle-hardware, control-hardware]
level: advanced
status: docs-checked
description: "Write a ros2_control SystemInterface hardware plugin with lifecycle callbacks and read/write loop."
sources:
  - https://raw.githubusercontent.com/ros-controls/ros2_control/master/hardware_interface/doc/writing_new_hardware_component.rst
  - https://raw.githubusercontent.com/ros-controls/ros2_control/master/ros2controlcli/doc/userdoc.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Hardware interface plugin
Hardware components are libraries loaded dynamically by the controller manager through
pluginlib. Pick the base class by hardware type: `ActuatorInterface`, `SensorInterface`
or `SystemInterface` (header `hardware_interface/<type>_interface.hpp`).

## Class outline
- Constructor without parameters.
- Lifecycle callbacks: `on_configure`, `on_cleanup`, `on_shutdown`, `on_activate`,
  `on_deactivate`, `on_error`.
- Overrides of the interface class: `on_init`, `read`, `write`, and optionally
  `prepare_command_mode_switch` and `perform_command_mode_switch` (actuator and system
  types, for hardware with several control modes).

## What each method does
- `on_init`: call the parent `on_init(info)` first (it processes standard values such as
  the name), initialise members and process parameters from `info`; return
  `CallbackReturn::SUCCESS`, or `CallbackReturn::ERROR` if parameters are missing or
  invalid.
- `on_configure`: set up communication so the hardware can be activated; `on_cleanup`
  does the opposite.
- `on_activate`: enable hardware "power"; `on_deactivate` does the opposite.
- `on_shutdown`: shut down gracefully. `on_error`: handle errors from all states.
- `read`: get states from the hardware and store them with `set_state(name, value)`.
- `write`: command the hardware from values read with `get_command(name)`.

## Interfaces
- Command and state interfaces are created and exported automatically by the framework
  (`on_export_command_interfaces()` and `on_export_state_interfaces()`) from the
  interfaces declared in the `ros2_control` XML tag. Descriptions are kept in maps such as
  `joint_command_interfaces_` and `joint_state_interfaces_` (also sensor, gpio and
  unlisted). Full names look like `<joint_name>/<interface_type>`.
- Interfaces not in the XML tag can be added by overriding
  `export_unlisted_command_interface_descriptions()` or
  `export_unlisted_state_interface_descriptions()`.
- If you override the export methods yourself, store the created interfaces (only shared
  pointers are returned and the resource manager will not give them back) and keep names
  unique.
- Sensor-type components export no command interfaces.

## Packaging
1. `ament_cmake` package with `include/<package>/` and `src/`; header guards, a unique
   namespace (the package name in snake_case).
2. End the .cpp with `PLUGINLIB_EXPORT_CLASS(<package>::<Class>, hardware_interface::<Type>Interface)`
   (include `pluginlib/class_list_macros.hpp`).
3. Write `<package>.xml` describing the library and class; the plugin name is usually
   `<package>/<Class>` and must match the macro.
4. In CMake add dependencies `hardware_interface`, `pluginlib`, `rclcpp`,
   `rclcpp_lifecycle`, build a shared library, and call
   `pluginlib_export_plugin_description_file(hardware_interface <package>.xml)`.
5. Add the same dependencies to `package.xml`; write a load test modelled on the generic
   system mock test.
6. Build with `colcon build <package>`, source the install setup file, then run
   `colcon test <package>`.

## Optional extras
- The framework creates a node per hardware component, reachable with `get_node()`, for
  publishers and timers without disturbing the control loop.
- Framework-managed status publishing: override `init_hardware_status_message`
  (non-real-time, pre-allocate the message structure) and
  `update_hardware_status_message` (real-time safe, fast and non-allocating) and set the
  `status_publish_rate` parameter in the URDF `hardware` tag; 0.0 disables it.

## Self-check
`ros2 control list_hardware_components` shows the component and its state (active after
the controller manager activates it).

## Checked
Method: docs-checked 2026-11-09 against the ros2_control "Writing a Hardware Component" guide and the ros2controlcli userdoc.rst (both read in full from raw GitHub, current master). Removed as unconfirmed: the manual `export_state_interfaces` override code (current docs say export is automatic), the "no allocation, locking or blocking IO in read/write" rule, enabling torque on activate, the NaN-initial-command gotcha, returning ERROR on comms loss, and the landing-page source control.ros.org.
