---
id: computing-software.robotics-software.ros2-navigation-nav2.nav2-goals-commander
name: nav2-goals-commander
category: computing-software
field: robotics-software
product: ros2-navigation-nav2
tags: [nav2-simple-commander, navigate-to-pose, basic-navigator, initial-pose, follow-waypoints, nav2-msgs]
level: practitioner
status: docs-checked
description: "Send initial pose and navigation goals from code with NavigateToPose and nav2_simple_commander."
sources:
  - https://docs.nav2.org/
  - https://github.com/ros-navigation/docs.nav2.org
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Sending goals
```python
from nav2_simple_commander.robot_navigator import BasicNavigator
from geometry_msgs.msg import PoseStamped
nav = BasicNavigator()
init = PoseStamped(); init.header.frame_id = 'map'; init.pose.orientation.w = 1.0
nav.setInitialPose(init)
nav.waitUntilNav2Active()
goal = PoseStamped(); goal.header.frame_id = 'map'
goal.pose.position.x = 2.0; goal.pose.orientation.w = 1.0
nav.goToPose(goal)
while not nav.isTaskComplete(): fb = nav.getFeedback()
print(nav.getResult())        # TaskResult.SUCCEEDED / CANCELED / FAILED
```
- Underlying actions: NavigateToPose (`goToPose`), NavigateThroughPoses (`goThroughPoses`) and waypoint following (`followWaypoints`). The calls are non-blocking.

## Gotchas
- Initial pose must be set (or AMCL given `set_initial_pose`) before goals; otherwise tf `map` is missing.

## Self-check
Robot reaches a goal in simulation and `getResult()` reports SUCCEEDED.

## Checked
2026-11-03: parameter, plugin, API and command names compared with the Nav2 documentation sources (docs.nav2.org repository): core-server configuration pages (AMCL, BT Navigator, behavior, planner, smoother, docking, map saver, waypoint follower, costmap), the Simple Commander API page, the docking tutorial and the Jazzy and Lyrical migration guides. Removed or corrected: the `/navigate_to_pose` CLI line, the stamp line and the `w=0` rejection claim.

Method: documentation only; no commands were run.
