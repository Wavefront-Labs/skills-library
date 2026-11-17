---
id: computing-software.robotics-software.ros2-core.ament-package-types
name: ament-package-types
category: computing-software
field: robotics-software
product: ros2-core
tags: [ament-package, ament-cmake, ament-python, package-xml, ros2-pkg-create]
level: practitioner
status: docs-checked
description: "Create ament_cmake and ament_python packages with ros2 pkg create and keep package.xml correct."
sources:
  - https://github.com/ros2/ros2_documentation/blob/rolling/source/ROS-Framework/client-libraries/Working-with-Client-Libraries/Creating-Your-First-ROS2-Package.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Creating packages
```bash
ros2 pkg create --build-type ament_cmake --license Apache-2.0 --node-name my_node my_package
ros2 pkg create --build-type ament_python --license Apache-2.0 --node-name my_node my_package
```
- `ros2 pkg create` takes `--build-type` (`ament_cmake` or `ament_python`); `--node-name` generates a simple executable and `--license` declares the package license.
- `package.xml` holds the package meta information (maintainer, description, license).
- An ament_python package has `setup.py`, `setup.cfg` (required when the package has executables so `ros2 run` can find them) and a `resource/<package_name>` marker file.
- Interfaces can only be defined in CMake packages; Python libraries and nodes can live in a CMake package using ament_cmake_python.

## Gotchas
- Run `rosdep` in the workspace root to check for missing dependencies before building.

## Checked
2026-11-02. Confirmed in Creating-Your-First-ROS2-Package and Single-Package-Define-And-Use-Interface (ros2_documentation, rolling): ros2 pkg create options, ament_python file layout, setup.cfg purpose, interfaces only in CMake packages. Removed dependency tag list, ament_package(), data_files, naming rule and the rosdep flags (not in the docs read).
Method: documentation only; no commands were run.

## Self-check
The package builds with `colcon build` and its executable runs with `ros2 run`.
