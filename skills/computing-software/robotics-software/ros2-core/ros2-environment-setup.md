---
id: computing-software.robotics-software.ros2-core.ros2-environment-setup
name: ros2-environment-setup
category: computing-software
field: robotics-software
product: ros2-core
tags: [ros-env-setup, source, ros-domain-id, setup-bash]
level: intro
status: docs-checked
description: "Source the ROS 2 underlay and overlay, set ROS_DOMAIN_ID, and avoid environment mix-ups across workspaces."
sources:
  - https://github.com/ros2/ros2_documentation
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Environment setup
**Goal:** a shell that finds the right ROS 2 install and workspace.

```bash
source /opt/ros/jazzy/setup.bash      # underlay (binary install)
source ~/ros2_ws/install/setup.bash   # overlay (your workspace), after a build
export ROS_DOMAIN_ID=42               # isolate this robot/team on the network
printenv | grep -i ROS                # inspect what is set
```
- Add the underlay `source` line to `~/.bashrc` to avoid sourcing it in every shell; source overlays explicitly.
- All nodes use domain ID 0 by default; choose an integer between 0 and 101 inclusive that nobody else on your network uses.
- Source the underlay first, then the overlay.

## Gotchas
- Confirm `printenv | grep -i ROS` shows the expected `ROS_DISTRO` and `ROS_VERSION`.

## Self-check
`ros2 pkg list | grep <your_pkg>` finds your package; `ros2 run demo_nodes_cpp talker` in one shell is heard by `listener` in another with the same domain id.

## Checked
2026-11-03. Confirmed in ros2_documentation (Configuring-ROS2-Environment, About-Domain-ID): `source /opt/ros/<distro>/setup.bash`, `~/.bashrc` line, `printenv | grep -i ROS`, `ROS_DISTRO`/`ROS_VERSION`, `ROS_DOMAIN_ID` default 0 and safe range 0-101. Removed: mixed-distro and stale `install/` claims, new-shell-after-build advice.
Method: documentation only; no commands were run.
