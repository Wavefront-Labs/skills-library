---
id: computing-software.robotics-software.ros2-navigation-nav2.velocity-limits-collision-monitor
name: velocity-limits-collision-monitor
category: computing-software
field: robotics-software
product: ros2-navigation-nav2
tags: [collision-monitor, velocity-smoother, max-accel, polygon-slowdown, collision-monitor-polygons, cmd-vel]
level: advanced
status: docs-checked
description: "Limit and filter cmd_vel with velocity_smoother and the collision monitor."
sources:
  - https://github.com/ros-navigation/docs.nav2.org/tree/rolling/docs/configuration_and_development/configuration_guide/core_servers
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Velocity smoothing and collision monitor
- `velocity_smoother`: `max_velocity [vx, vy, wz]`, `min_velocity`, `max_accel`, `max_decel`, `feedback: "OPEN_LOOP"` (default, uses the last commanded velocity) or `"CLOSED_LOOP"`.
- `collision_monitor`: polygons with action types `stop`, `slowdown`, `limit` or `approach` around the robot, fed by data sources; input and output topics are `cmd_vel_in_topic` (default `cmd_vel_smoothed`) and `cmd_vel_out_topic` (default `cmd_vel`).
```yaml
collision_monitor:
  ros__parameters:
    cmd_vel_in_topic: cmd_vel_smoothed
    cmd_vel_out_topic: cmd_vel
    polygons: ["PolygonStop"]
    PolygonStop: {type: polygon, points: "[[0.3, 0.3], [0.3, -0.3], [-0.3, -0.3], [-0.3, 0.3]]", action_type: stop, min_points: 4, visualize: true, polygon_pub_topic: polygon_stop}
    observation_sources: ["scan"]
    scan: {type: scan, topic: /scan}
```
- Remap chain so only the final stage publishes to the base's `cmd_vel`.

## Gotchas
- Two nodes publishing the same `cmd_vel` fight; check the remapping chain.
- Nav2's collision monitor does not provide hard real-time safety certification.

## Self-check
Placing an obstacle in the stop polygon halts the robot without planner involvement.

## Checked
2026-11-03. Confirmed in the Nav2 docs source (configuring_velocity_smoother, configuring_collision_monitor_node): `max_velocity`, `min_velocity`, `max_accel`, `max_decel`, `feedback` default `OPEN_LOOP`, `cmd_vel_in_topic`/`cmd_vel_out_topic` defaults, polygon `type`, `points`, `action_type` values, `min_points`, `visualize`, `polygon_pub_topic`, `observation_sources`, source types `scan`/`pointcloud`/`range`. Fixed: `points` must be a nested list `"[[x, y], ...]"`, not a flat list. Removed: smoother topic names, "Galactic+" and "certified" wording.
Method: documentation only; no commands were run.
