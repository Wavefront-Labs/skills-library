---
id: computing-software.robotics-software.ros2-navigation-nav2.costmap-layers
name: costmap-layers
category: computing-software
field: robotics-software
product: ros2-navigation-nav2
tags: [costmap-layers, static-layer, obstacle-layer, voxel-layer, plugins, observation-sources, nav2-costmaps]
level: practitioner
status: docs-checked
description: "Configure global and local costmap layers: static, obstacle, voxel and sensor observation sources."
sources:
  - https://docs.nav2.org/
  - https://github.com/ros-navigation/docs.nav2.org
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Costmap layers
Config (excerpt of `nav2_params.yaml`):
```yaml
local_costmap:
  local_costmap:
    ros__parameters:
      update_frequency: 5.0
      rolling_window: true
      width: 3
      height: 3
      resolution: 0.05
      plugins: ["voxel_layer", "inflation_layer"]
      voxel_layer:
        plugin: "nav2_costmap_2d::VoxelLayer"
        observation_sources: scan
        scan: {topic: /scan, data_type: LaserScan, marking: true, clearing: true, max_obstacle_height: 2.0}
      inflation_layer: {plugin: "nav2_costmap_2d::InflationLayer"}
global_costmap: # static_layer + obstacle_layer + inflation_layer, global_frame: map
```
- Global costmap uses the static map; local is a rolling window in `odom`.
- Plugin order matters: inflation last.
- Sensor `topic` QoS must match the driver (best effort sensors need a matching setting in the observation source in newer releases; check docs).

## Gotchas
- Wrong `observation_sources` sub-block name silently disables a sensor.
- Too-large local window or tiny resolution loads the CPU.

## Self-check
RViz shows obstacle cells from live scans in the local costmap and clearing when they leave.

## Checked
2026-11-03: parameter, plugin, API and command names compared with the Nav2 documentation sources (docs.nav2.org repository): core-server configuration pages (AMCL, BT Navigator, behavior, planner, smoother, docking, map saver, waypoint follower, costmap), the Simple Commander API page, the docking tutorial and the Jazzy and Lyrical migration guides. Removed or corrected: nothing needed removal.

Method: documentation only; no commands were run.
