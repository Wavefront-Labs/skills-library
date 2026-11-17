---
id: computing-software.robotics-software.ros2-navigation-nav2.docking-keepout-routes
name: docking-keepout-routes
category: computing-software
field: robotics-software
product: ros2-navigation-nav2
tags: [nav2-docking, opennav-docking, docking-server, dock-database, charging-dock, route-server]
level: advanced
status: docs-checked
description: "Use Nav2 docking (Jazzy and later) with a dock database, and know when to use route or keepout features."
sources:
  - https://docs.nav2.org/
  - https://github.com/ros-navigation/docs.nav2.org
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Docking and related features
- Docking server (`opennav_docking`; the Jazzy migration guide documents it): actions `DockRobot` / `UndockRobot`; docks listed in the `docks` parameter or a `dock_database` file, each as `{type: <dock plugin name>, frame: map, pose: [x, y, theta]}`; a dock plugin (e.g. `SimpleChargingDock`, `SimpleNonChargingDock`) does detection and charge detection.
- Python: `nav.dockRobot(dock_pose, dock_type)` or `nav.dockRobot(dock_id)`, and `nav.undockRobot(dock_type="")`.
- Keepout zones: costmap filter with a mask (see costmap-filters). Speed limits by region: SpeedFilter.
- Route server (graph-based planning) is newer; check docs for your distro.
- Always verify the docking action with the robot raised off the floor or in simulation first.

## Gotchas
- Dock pose in the wrong frame or off by the dock offset parameters causes misses.
- The simple dock plugins need `JointState`, `BatteryState` and detected dock pose (`PoseStamped`) topics.

## Self-check
Dock/undock succeed in simulation before using on hardware.

## Checked
2026-11-03: parameter, plugin, API and command names compared with the Nav2 documentation sources (docs.nav2.org repository): core-server configuration pages (AMCL, BT Navigator, behavior, planner, smoother, docking, map saver, waypoint follower, costmap), the Simple Commander API page, the docking tutorial and the Jazzy and Lyrical migration guides. Removed or corrected: the nonexistent `dockRobotByPose` (real API is `dockRobot`) and the invented `simple_charging_dock` type name.

Method: documentation only; no commands were run.
