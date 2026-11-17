---
id: computing-software.robotics-software.ros2-navigation-nav2.controller-server-plugins
name: controller-server-plugins
category: computing-software
field: robotics-software
product: ros2-navigation-nav2
tags: [controller-server, dwb, regulated-pure-pursuit, mppi-controller, goal-checker, progress-checker, nav2-control]
level: practitioner
status: docs-checked
description: "Configure the controller server with DWB, Regulated Pure Pursuit or MPPI plus goal and progress checkers."
sources:
  - https://docs.nav2.org/
  - https://github.com/ros-navigation/docs.nav2.org
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Controller server
```yaml
controller_server:
  ros__parameters:
    controller_frequency: 20.0
    controller_plugins: ["FollowPath"]
    progress_checker_plugins: ["progress_checker"]
    goal_checker_plugins: ["general_goal_checker"]
    FollowPath:
      plugin: "nav2_regulated_pure_pursuit_controller::RegulatedPurePursuitController"   # or dwb_core::DWBLocalPlanner, nav2_mppi_controller::MPPIController
      desired_linear_vel: 0.5
      lookahead_dist: 0.6
    general_goal_checker: {plugin: "nav2_controller::SimpleGoalChecker", xy_goal_tolerance: 0.25, yaw_goal_tolerance: 0.25}
    progress_checker: {plugin: "nav2_controller::SimpleProgressChecker", required_movement_radius: 0.5, movement_time_allowance: 10.0}
```
- RPP: path tracking, good for differential and car-like robots at steady speed. DWB: sampling, many critics to tune. MPPI: predictive, supports omni/diff/Ackermann motion models, heavier CPU.
- Output goes to `cmd_vel` (via `velocity_smoother` if used, then `collision_monitor`).

## Gotchas
- Controller frequency too low causes jerky motion; too high wastes CPU.
- Progress checker aborts when the robot is stuck; raise `movement_time_allowance` for slow robots.

## Self-check
Robot follows a straight path at the desired speed and stops within goal tolerance.

## Checked
2026-11-03: parameter, plugin, API and command names compared with the Nav2 documentation sources (docs.nav2.org repository): core-server configuration pages (AMCL, BT Navigator, behavior, planner, smoother, docking, map saver, waypoint follower, costmap), the Simple Commander API page, the docking tutorial and the Jazzy and Lyrical migration guides. Removed or corrected: nothing needed removal.

Method: documentation only; no commands were run.
