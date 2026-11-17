---
id: computing-software.robotics-software.ros2-core.custom-interfaces
name: custom-interfaces
category: computing-software
field: robotics-software
product: ros2-core
tags: [custom-interface, msg-file, srv-file, rosidl, rosidl-generate-interfaces, ros2-interfaces]
level: practitioner
status: docs-checked
description: "Define custom .msg, .srv and .action files in a dedicated interface package and generate code with rosidl."
sources:
  - https://github.com/ros2/ros2_documentation/blob/rolling/source/ROS-Framework/client-libraries/Working-with-Client-Libraries/Custom-ROS2-Interfaces.rst
  - https://github.com/ros2/ros2_documentation/blob/rolling/source/ROS-Framework/client-libraries/Working-with-Client-Libraries/Single-Package-Define-And-Use-Interface.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Custom interfaces
**Goal:** a reusable `my_interfaces` package.

```
my_interfaces/msg/Status.msg        # string name \n float32 battery
my_interfaces/srv/Reset.srv         # request --- response
my_interfaces/action/Go.action      # goal --- result --- feedback
```
CMakeLists.txt:
```cmake
find_package(rosidl_default_generators REQUIRED)
rosidl_generate_interfaces(${PROJECT_NAME} "msg/Status.msg" "srv/Reset.srv" "action/Go.action")
ament_export_dependencies(rosidl_default_runtime)
```
package.xml: `<buildtool_depend>rosidl_default_generators</buildtool_depend>`, `<exec_depend>rosidl_default_runtime</exec_depend>`, `<member_of_group>rosidl_interface_packages</member_of_group>`.
- The first argument of `rosidl_generate_interfaces` must start with the package name, for example `${PROJECT_NAME}`.
- `rosidl_default_generators` is a build tool dependency; `rosidl_default_runtime` is needed at run time to use the interfaces.
- The package is declared a `<member_of_group>` of `rosidl_interface_packages`.

## Gotchas
- Interfaces can only be defined in ament_cmake packages, but you can use them from C++ or Python nodes in any package type.

## Checked
2026-11-02. Confirmed in Custom-ROS2-Interfaces and Single-Package-Define-And-Use-Interface (ros2_documentation, rolling): rosidl_generate_interfaces, rosidl_default_generators/runtime, member_of_group, ament_cmake-only rule, ros2 interface show. Removed naming-case rule, separate-package advice and the bag-breaking claim (not in the docs read). The example file names are illustrative.
Method: documentation only; no commands were run.

## Self-check
`ros2 interface show my_interfaces/msg/Status` prints the fields after building and sourcing.
