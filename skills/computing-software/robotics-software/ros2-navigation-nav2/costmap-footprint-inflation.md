---
id: computing-software.robotics-software.ros2-navigation-nav2.costmap-footprint-inflation
name: costmap-footprint-inflation
category: computing-software
field: robotics-software
product: ros2-navigation-nav2
tags: [costmap-inflation, robot-radius, footprint, inflation-radius, cost-scaling-factor, keepout-filter]
level: advanced
status: docs-checked
description: "Tune robot footprint, inflation radius and cost scaling, and use keepout and speed filter masks."
sources:
  - https://docs.nav2.org/
  - https://github.com/ros-navigation/docs.nav2.org
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Footprint and inflation
- Footprint: `robot_radius: 0.22` (circle) or `footprint: "[[0.3,0.2],[0.3,-0.2],[-0.3,-0.2],[-0.3,0.2]]"` (polygon, metres, base_link). Set the same in both costmaps.
- `inflation_layer.inflation_radius` should exceed the circumscribed radius plus a margin; `cost_scaling_factor` controls how fast cost decays (higher = steeper, planner hugs walls more closely).
- Cost values: inscribed and lethal cells are 253-254 (the Collision Monitor page describes the range as inscribed/lethal).
- Too large an inflation radius closes doorways; too small causes wall scraping.
- Costmap filters (`KeepoutFilter`, `SpeedFilter`, `BinaryFilter`) use a mask image + `CostmapFilterInfoServer` + map server for no-go zones and speed zones.

## Gotchas
- A footprint larger than the real robot wastes space; smaller risks collisions.
- Filter masks must align (same frame/resolution) with the map.

## Self-check
The robot passes a known-width doorway and RViz shows inflation ring not blocking it.

## Checked
2026-11-03: parameter, plugin, API and command names compared with the Nav2 documentation sources (docs.nav2.org repository): core-server configuration pages (AMCL, BT Navigator, behavior, planner, smoother, docking, map saver, waypoint follower, costmap), the Simple Commander API page, the docking tutorial and the Jazzy and Lyrical migration guides. Removed or corrected: the 0 and 255 cost-value claims.

Method: documentation only; no commands were run.
