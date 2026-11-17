---
id: computing-software.robotics-software.moveit-manipulation.ompl-planning
name: ompl-planning
category: computing-software
field: robotics-software
product: moveit-manipulation
tags: [ompl-pipeline, ompl, rrtconnect, planning-adapters, planning-time, planner-config, moveit-planning-pipelines]
level: practitioner
status: docs-checked
description: "Configure the OMPL planning pipeline: planner configs per group, RRTConnect, request adapters, planning time."
sources:
  - https://moveit.picknik.ai/main/index.html
  - https://github.com/moveit/moveit2
  - https://github.com/moveit/moveit2_tutorials
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# OMPL pipeline
`ompl_planning.yaml` (excerpt):
```yaml
planning_plugins: ["ompl_interface/OMPLPlanner"]     # newer; older used planning_plugin: ompl_interface/OMPLPlanner
request_adapters: [default_planning_request_adapters/ResolveConstraintFrames, default_planning_request_adapters/ValidateWorkspaceBounds, default_planning_request_adapters/CheckStartStateBounds, default_planning_request_adapters/CheckStartStateCollision]
response_adapters: [default_planning_response_adapters/AddTimeOptimalParameterization, default_planning_response_adapters/ValidateSolution, default_planning_response_adapters/DisplayMotionPath]
panda_arm:
  default_planner_config: RRTConnectkConfigDefault
  planner_configs: [RRTConnectkConfigDefault, RRTstarkConfigDefault]
```
(Adapter names and the plural keys changed across releases; version unconfirmed, compare with your generated file.)
- RRTConnect is the usual first choice; RRT* optimizes but needs a time budget.
- Set time and attempts per request: `setPlanningTime(5.0)`, `setNumPlanningAttempts(10)`.
- Planner IDs: `RRTConnectkConfigDefault` etc.

## Gotchas
- OMPL plans are random and jerky; use shortcutting/smoothing adapters and time parameterization.
- Planning fails without a valid start state; check joint limits.

## Self-check
The same goal planned five times succeeds each time within the budget.

## Checked
2026-11-03: parameter, plugin, API and command names compared with the MoveIt 2 sources (moveit2 repository headers, servo_parameters.yaml, servo_node.cpp, datatypes.hpp, moveit_py bindings; moveit2_tutorials pages for controller configuration, OMPL, Pilz, setup assistant and Bullet). Removed or corrected: nothing needed removal.

Method: documentation only; no commands were run.
