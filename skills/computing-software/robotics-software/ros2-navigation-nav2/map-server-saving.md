---
id: computing-software.robotics-software.ros2-navigation-nav2.map-server-saving
name: map-server-saving
category: computing-software
field: robotics-software
product: ros2-navigation-nav2
tags: [map-server, map-saver-cli, map-yaml, occupancy-grid, pgm, nav2-lifecycle]
level: practitioner
status: docs-checked
description: "Serve and save maps with nav2_map_server: map YAML fields, map_saver_cli and occupancy thresholds."
sources:
  - https://docs.nav2.org/
  - https://github.com/ros-navigation/docs.nav2.org
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Map server
Map YAML:
```yaml
image: map.pgm
mode: trinary
resolution: 0.05
origin: [-10.0, -10.0, 0.0]
negate: 0
occupied_thresh: 0.65
free_thresh: 0.25
```
```bash
ros2 run nav2_map_server map_saver_cli -f ~/maps/lab           # saves lab.yaml + lab.pgm from /map
ros2 run nav2_map_server map_server --ros-args -p yaml_filename:=lab.yaml
ros2 lifecycle set /map_server configure ; ros2 lifecycle set /map_server activate
```
- `map_server` is a lifecycle node publishing `/map` (transient local). The map saver has a `save_map_timeout` parameter for a slow `/map`.
- Resolution (metres per cell) and origin (pose of the lower-left pixel) must match what SLAM produced.

## Gotchas
- `/map` is transient local; subscribers with volatile QoS never see it.
- Editing the PGM changes planning; keep a backup.

## Self-check
The published map's width/height match the image.

## Checked
2026-11-03: parameter, plugin, API and command names compared with the Nav2 documentation sources (docs.nav2.org repository): core-server configuration pages (AMCL, BT Navigator, behavior, planner, smoother, docking, map saver, waypoint follower, costmap), the Simple Commander API page, the docking tutorial and the Jazzy and Lyrical migration guides. Removed or corrected: the `--ros-args -p save_map_timeout:=5.0` command form and the `ros2 topic echo` self-check.

Method: documentation only; no commands were run.
