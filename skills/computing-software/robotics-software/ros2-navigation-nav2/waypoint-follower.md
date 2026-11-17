---
id: computing-software.robotics-software.ros2-navigation-nav2.waypoint-follower
name: waypoint-follower
category: computing-software
field: robotics-software
product: ros2-navigation-nav2
tags: [waypoint-follower, follow-waypoints, task-executor, wait-at-waypoint, nav-through-poses, sequential-goals, nav2-advanced]
level: practitioner
status: docs-checked
description: "Run waypoint missions with FollowWaypoints and task executors at each waypoint."
sources:
  - https://docs.nav2.org/
  - https://github.com/ros-navigation/docs.nav2.org
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Waypoint following
```yaml
waypoint_follower:
  ros__parameters:
    stop_on_failure: false
    loop_rate: 20
    waypoint_task_executor_plugin: "wait_at_waypoint"
    wait_at_waypoint: {plugin: "nav2_waypoint_follower::WaitAtWaypoint", enabled: true, waypoint_pause_duration: 200}
```
```python
nav.followWaypoints([pose1, pose2, pose3])       # BasicNavigator
while not nav.isTaskComplete(): fb = nav.getFeedback()
```
- Other task executors: `PhotoAtWaypoint`, `InputAtWaypoint`.
- `NavigateThroughPoses` plans one continuous path through poses instead of stopping at each.

## Gotchas
- `stop_on_failure: true` aborts the mission at the first failed waypoint.
- Waypoints on lethal or inflated cells are rejected by the planner.

## Self-check
Three waypoints complete in order.

## Checked
2026-11-03: parameter, plugin, API and command names compared with the Nav2 documentation sources (docs.nav2.org repository): core-server configuration pages (AMCL, BT Navigator, behavior, planner, smoother, docking, map saver, waypoint follower, costmap), the Simple Commander API page, the docking tutorial and the Jazzy and Lyrical migration guides. Removed or corrected: `fb.current_waypoint` and `missed_waypoints` (not in the docs).

Method: documentation only; no commands were run.
