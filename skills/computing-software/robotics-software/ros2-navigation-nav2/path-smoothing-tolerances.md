---
id: computing-software.robotics-software.ros2-navigation-nav2.path-smoothing-tolerances
name: path-smoothing-tolerances
category: computing-software
field: robotics-software
product: ros2-navigation-nav2
tags: [path-smoother, smoother-server, simple-smoother, savitzky-golay, planner-tolerance, goal-tolerance]
level: advanced
status: docs-checked
description: "Smooth planned paths with the smoother server and set planner and goal tolerances."
sources:
  - https://docs.nav2.org/
  - https://github.com/ros-navigation/docs.nav2.org
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Smoothing and tolerances
- `smoother_server` plugins: `nav2_smoother::SimpleSmoother`, `nav2_smoother::SavitzkyGolaySmoother` (the smoother pages document these two).
- Behavior-tree node `SmoothPath` runs a smoother after `ComputePathToPose`.
- Planner `tolerance` is how close to an occupied goal the planner may end; controller goal tolerances live in `general_goal_checker` (`xy_goal_tolerance`, `yaw_goal_tolerance`).
- Smoothing never checks dynamics of the robot; keep curvature feasible for car-like bases.
- Smoothers can push a path into obstacles; they re-check costmap collisions (`do_refinement`).

## Gotchas
- Smoothing a Smac Hybrid path with a simple smoother can break turning radius.
- Tight goal tolerance with a noisy localization oscillates.

## Self-check
Path in RViz is smoother with the smoother on and still collision-free.

## Checked
2026-11-03: parameter, plugin, API and command names compared with the Nav2 documentation sources (docs.nav2.org repository): core-server configuration pages (AMCL, BT Navigator, behavior, planner, smoother, docking, map saver, waypoint follower, costmap), the Simple Commander API page, the docking tutorial and the Jazzy and Lyrical migration guides. Removed or corrected: `nav2_smoother::CostmapSmoother` (not in the docs).

Method: documentation only; no commands were run.
