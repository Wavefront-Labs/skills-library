---
id: computing-software.robotics-software.moveit-manipulation.pilz-chomp-stomp
name: pilz-chomp-stomp
category: computing-software
field: robotics-software
product: moveit-manipulation
tags: [pilz-planner, pilz-industrial-motion-planner, ptp, lin, circ, chomp, stomp]
level: advanced
status: docs-checked
description: "Use the Pilz industrial planner for PTP, LIN and CIRC motions, and know when to pick CHOMP or STOMP."
sources:
  - https://moveit.picknik.ai/main/index.html
  - https://github.com/moveit/moveit2
  - https://github.com/moveit/moveit2_tutorials
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Pilz, CHOMP and STOMP
- Multiple pipelines can be loaded (`planning_pipelines` list); choose per request with `setPlanningPipelineId("pilz_industrial_motion_planner")` and `setPlannerId("LIN")`.
- Pilz planners (deterministic, industrial): `PTP` (joint-space), `LIN` (straight Cartesian line), `CIRC` (arc via center/interim point). Also sequence requests (`MotionSequenceRequest`) with blending radii.
- Limits come from a Cartesian limits file (`cartesian_limits`: `max_trans_vel`, `max_trans_acc`, `max_trans_dec`, `max_rot_vel`) plus joint limits including acceleration.
- CHOMP and STOMP optimize a trajectory for smoothness and obstacle cost; often used as post-processing of an OMPL path; require a good initial guess and parameter tuning.
- Repeatable paths for production: Pilz; free-space obstacle avoidance: OMPL.

## Gotchas
- Acceleration limits must be set through node parameters (the URDF has none); an unset `max_deceleration` becomes `-max_acceleration`.
- LIN fails when the line crosses a singularity or leaves joint limits.

## Self-check
A LIN move produces a straight end-effector path in RViz and fails cleanly when blocked.

## Checked
2026-11-03: parameter, plugin, API and command names compared with the MoveIt 2 sources (moveit2 repository headers, servo_parameters.yaml, servo_node.cpp, datatypes.hpp, moveit_py bindings; moveit2_tutorials pages for controller configuration, OMPL, Pilz, setup assistant and Bullet). Removed or corrected: the `pilz_cartesian_limits.yaml` name as a fixed requirement and the deceleration-required gotcha (unset deceleration defaults to -max_acceleration).

Method: documentation only; no commands were run.
