---
id: computing-software.robotics-software.ros2-core.colcon-build
name: colcon-build
category: computing-software
field: robotics-software
product: ros2-core
tags: [colcon-build, colcon, workspace, symlink-install, packages-select, packages-up-to, ros2-colcon-packages]
level: practitioner
status: docs-checked
description: "Build and test a ROS 2 workspace with colcon, selecting packages and using symlink install."
sources:
  - https://github.com/ros2/ros2_documentation/blob/rolling/source/ROS-Framework/client-libraries/Working-with-Client-Libraries/Colcon-Tutorial.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# colcon workflow
```bash
cd ~/ros2_ws && colcon build --symlink-install
colcon build --packages-select my_pkg
source install/setup.bash
```
- Layout: `src/` sources, then `build/`, `install/`, `log/` created by colcon; never commit them.
- `--symlink-install` lets Python and launch/config edits take effect without rebuild.
- `--event-handlers console_direct+` prints output directly to the console.
- Run `colcon build` in the root of the workspace.

## Gotchas
- On Windows `--symlink-install` needs permission to create symbolic links, so it is not used by default.
- The workspace on top of an existing ROS 2 installation is an overlay; the installation is the underlay.

## Checked
2026-11-02. Confirmed in Colcon-Tutorial (ros2_documentation, rolling): src/build/install/log layout, --symlink-install, build from the workspace root, underlay and overlay, Windows symlink note, console_direct+ in the page set. Removed --packages-up-to, CMAKE_BUILD_TYPE, colcon test commands, log/latest_build, the clean-switch gotcha and the pkg prefix check (not in the docs read).
Method: documentation only; no commands were run.

## Self-check
After `source install/setup.bash`, the ROS 2 commands find your package (for example `ros2 run my_pkg <executable>`).
