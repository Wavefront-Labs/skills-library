---
id: computing-software.robotics-software.ros2-core.rosdep-dependencies
name: rosdep-dependencies
category: computing-software
field: robotics-software
product: ros2-core
tags: [rosdep, rosdep-install, rosdep-update, rosdep-keys, package-xml-deps]
level: practitioner
status: docs-checked
description: "Resolve system and ROS dependencies with rosdep init, update and install."
sources:
  - https://github.com/ros2/ros2_documentation
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# rosdep
```bash
sudo rosdep init                # once per machine
rosdep update
rosdep install --from-paths src --ignore-src -r -y --rosdistro jazzy
```
- `rosdep install` consults a local cached index from rosdistro (populated by `rosdep update`, cached in `~/.ros/rosdep/sources.cache`) to map `package.xml` keys to ROS packages, Python modules or binaries to install.
- `rosdep init` populates `20-default.list` with the main rosdistro URLs.

## Gotchas
- Do not edit the generated cache by hand; rerun `rosdep update`.

## Self-check
After install, `colcon build` needs no manual apt installs.

## Checked
2026-11-03. Confirmed in ros2_documentation (installation pages and Using-Custom-Rosdistro): `sudo rosdep init`, `rosdep update`, `rosdep install --from-paths src --ignore-src ... -y --rosdistro <distro>`, `-r -y` form, index/cache behaviour. Removed: `rosdep resolve`, custom-key YAML, CI advice, `-r` semantics and pip claims (not in the pages read).
Method: documentation only; no commands were run.
