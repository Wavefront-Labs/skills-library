---
id: computing-software.robotics-software.ros2-navigation-nav2.nav2-bringup-launch
name: nav2-bringup-launch
category: computing-software
field: robotics-software
product: ros2-navigation-nav2
tags: [nav2-bringup, bringup-launch, params-file, lifecycle-manager, autostart, tb3-simulation, nav2-bringup]
level: practitioner
status: docs-checked
description: "Bring up the Nav2 stack with nav2_bringup, a params file, a map and the lifecycle managers."
sources:
  - https://docs.nav2.org/
  - https://github.com/ros-navigation/docs.nav2.org
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Nav2 bring-up
**Goal:** a running navigation stack you can configure.

```bash
sudo apt install ros-$ROS_DISTRO-navigation2 ros-$ROS_DISTRO-nav2-bringup
ros2 launch nav2_bringup tb3_simulation_launch.py headless:=False       # demo (TurtleBot 3 packages required)
ros2 launch nav2_bringup bringup_launch.py map:=map.yaml params_file:=nav2_params.yaml use_sim_time:=true
```
- Servers: planner_server, controller_server, smoother_server, behavior_server, bt_navigator, waypoint_follower, velocity_smoother; localization: map_server + amcl (or SLAM).
- Lifecycle managers (`lifecycle_manager_navigation` in the docs; the Lyrical migration guide merges the separate managers into one `lifecycle_manager_nav2`) bring the nodes up in order from their `node_names` list.
- Copy `nav2_bringup/params/nav2_params.yaml` and edit; one file configures all servers under their node names.
- Robot needs: `/tf` chain `map -> odom -> base_link`, `/odom`, a sensor topic, and a velocity command on `/cmd_vel`.

## Gotchas
- Mismatched `use_sim_time` across nodes causes tf extrapolation errors.
- Stack does nothing until lifecycle managers report active; check logs for failed transitions.

## Self-check
`ros2 lifecycle get /bt_navigator` reports `active` and the RViz Nav2 panel shows navigation active.

## Checked
2026-11-03: parameter, plugin, API and command names compared with the Nav2 documentation sources (docs.nav2.org repository): core-server configuration pages (AMCL, BT Navigator, behavior, planner, smoother, docking, map saver, waypoint follower, costmap), the Simple Commander API page, the docking tutorial and the Jazzy and Lyrical migration guides. Removed or corrected: the `lifecycle_manager_localization` name (Lyrical merges managers into `lifecycle_manager_nav2`).

Method: documentation only; no commands were run.
