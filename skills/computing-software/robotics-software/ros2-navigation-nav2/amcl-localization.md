---
id: computing-software.robotics-software.ros2-navigation-nav2.amcl-localization
name: amcl-localization
category: computing-software
field: robotics-software
product: ros2-navigation-nav2
tags: [nav2-amcl, amcl, particle-filter, initial-pose-estimate, laser-model, odom-frame, nav2-localization]
level: practitioner
status: docs-checked
description: "Configure AMCL: frames, motion model, scan topic, particle counts, and initial pose."
sources:
  - https://docs.nav2.org/
  - https://github.com/ros-navigation/docs.nav2.org
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# AMCL
```yaml
amcl:
  ros__parameters:
    base_frame_id: base_footprint
    odom_frame_id: odom
    global_frame_id: map
    scan_topic: scan
    robot_model_type: "nav2_amcl::DifferentialMotionModel"
    min_particles: 500
    max_particles: 2000
    set_initial_pose: true
    initial_pose: {x: 0.0, y: 0.0, z: 0.0, yaw: 0.0}
    tf_broadcast: true
```
- AMCL publishes the `map -> odom` transform; the `odom` to base-frame transform must come from your odometry. Needs a map from `map_server`.
- Set the pose in RViz (2D Pose Estimate), through the Simple Commander `setInitialPose`, or with `set_initial_pose`/`initial_pose` as above.
- AMCL is laser-scan based; the page documents `scan_topic` only.
- `always_reset_initial_pose`, `update_min_d`, `update_min_a` control update cadence.

## Gotchas
- Wrong `base_frame_id` (footprint vs link) yields a failed tf lookup.
- Featureless corridors cause drift; AMCL cannot recover without good scans.

## Self-check
Particle cloud collapses around the true pose after a short drive.

## Checked
2026-11-03: parameter, plugin, API and command names compared with the Nav2 documentation sources (docs.nav2.org repository): core-server configuration pages (AMCL, BT Navigator, behavior, planner, smoother, docking, map saver, waypoint follower, costmap), the Simple Commander API page, the docking tutorial and the Jazzy and Lyrical migration guides. Removed or corrected: the `/initialpose` topic and `pointcloud_to_laserscan` advice (not in the docs).

Method: documentation only; no commands were run.
