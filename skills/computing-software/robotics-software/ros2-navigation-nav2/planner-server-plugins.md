---
id: computing-software.robotics-software.ros2-navigation-nav2.planner-server-plugins
name: planner-server-plugins
category: computing-software
field: robotics-software
product: ros2-navigation-nav2
tags: [planner-server, navfn, smac-planner, smac-hybrid, theta-star, planner-plugins, nav2-planning]
level: practitioner
status: docs-checked
description: "Select and configure Nav2 global planner plugins (NavFn, Smac 2D/Hybrid/Lattice, Theta*)."
sources:
  - https://docs.nav2.org/
  - https://github.com/ros-navigation/docs.nav2.org
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Planner server
```yaml
planner_server:
  ros__parameters:
    expected_planner_frequency: 20.0
    planner_plugins: ["GridBased"]
    GridBased:
      plugin: "nav2_navfn_planner::NavfnPlanner"     # or nav2_smac_planner::SmacPlanner2D, SmacPlannerHybrid, SmacPlannerLattice, nav2_theta_star_planner::ThetaStarPlanner
      tolerance: 0.5
      use_astar: false
      allow_unknown: true
```
- NavFn/Theta*/Smac2D: holonomic or circular robots; SmacHybrid (Dubin/Reeds-Shepp) and Lattice: car-like or non-circular, kinematically feasible paths.
- Hybrid needs `minimum_turning_radius`; Lattice needs a lattice file generated for the robot.
- Choose planners per behavior-tree node with `planner_id`.
- Plan is requested via `ComputePathToPose` action.

## Gotchas
- Plugin strings use the `pkg::Class` form (for example `nav2_navfn_planner::NavfnPlanner`); the `pkg/Class` form is not used on the planner pages.
- `allow_unknown` false with a partly unknown map fails to plan.

## Self-check
A ComputePathToPose request returns a non-empty path.

## Checked
2026-11-03: parameter, plugin, API and command names compared with the Nav2 documentation sources (docs.nav2.org repository): core-server configuration pages (AMCL, BT Navigator, behavior, planner, smoother, docking, map saver, waypoint follower, costmap), the Simple Commander API page, the docking tutorial and the Jazzy and Lyrical migration guides. Removed or corrected: the `pkg/Class` plugin form (docs use `pkg::Class`) and the action CLI line.

Method: documentation only; no commands were run.
