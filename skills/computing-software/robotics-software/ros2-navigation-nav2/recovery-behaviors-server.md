---
id: computing-software.robotics-software.ros2-navigation-nav2.recovery-behaviors-server
name: recovery-behaviors-server
category: computing-software
field: robotics-software
product: ros2-navigation-nav2
tags: [behavior-server, spin, backup, drive-on-heading, wait, assisted-teleop]
level: advanced
status: docs-checked
description: "Configure behavior_server recoveries (spin, backup, drive_on_heading, wait, assisted_teleop) and invoke them from the BT."
sources:
  - https://docs.nav2.org/
  - https://github.com/ros-navigation/docs.nav2.org
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Behavior server
```yaml
behavior_server:
  ros__parameters:
    behavior_plugins: ["spin", "backup", "drive_on_heading", "wait"]
    spin: {plugin: "nav2_behaviors::Spin"}
    backup: {plugin: "nav2_behaviors::BackUp"}
    drive_on_heading: {plugin: "nav2_behaviors::DriveOnHeading"}
    wait: {plugin: "nav2_behaviors::Wait"}
    local_frame: odom
    global_frame: map
    robot_base_frame: base_link
    spin:
      max_rotational_vel: 1.0
      rotational_acc_lim: 3.2
```
- Behavior server exposes one action server per behavior, called by BT nodes (`<Spin spin_dist="1.57"/>`, `<BackUp backup_dist="0.3" backup_speed="0.15"/>`).
- Per-behavior parameters are namespaced under the plugin name (`spin.max_rotational_vel`, `backup.simulate_ahead_time`); the older node-level names are no longer read in the current docs (Lyrical migration guide), so check your distro's page.
- Recoveries check the local costmap for collision and abort if blocked.
- Test directly with the Simple Commander: `nav.spin(spin_dist=1.57)`, `nav.backup(backup_dist=0.15, backup_speed=0.025)`.

## Gotchas
- Backing up a robot with no rear sensors is unsafe; consider disabling.
- Plugin names in the list must exactly match the sub-block names.

## Self-check
`nav.spin(spin_dist=1.57)` rotates the robot about 90 degrees and returns success.

## Checked
2026-11-03: parameter, plugin, API and command names compared with the Nav2 documentation sources (docs.nav2.org repository): core-server configuration pages (AMCL, BT Navigator, behavior, planner, smoother, docking, map saver, waypoint follower, costmap), the Simple Commander API page, the docking tutorial and the Jazzy and Lyrical migration guides. Removed or corrected: `nav2_behaviors/X` plugin strings (docs use `::`), node-level spin parameters (now namespaced), the `/spin` CLI line.

Method: documentation only; no commands were run.
