---
id: computing-software.robotics-software.moveit-manipulation.allowed-collision-matrix
name: allowed-collision-matrix
category: computing-software
field: robotics-software
product: moveit-manipulation
tags: [allowed-collision-matrix, acm, disable-collisions, touch-links, collision-checking-fcl, padding]
level: advanced
status: docs-checked
description: "Manage the allowed collision matrix, touch links and collision padding for grasping and contact."
sources:
  - https://moveit.picknik.ai/main/index.html
  - https://github.com/moveit/moveit2
  - https://github.com/moveit/moveit2_tutorials
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Allowed collision matrix
- The Setup Assistant generates the self-collision matrix into the SRDF as disabled link pairs.
- At runtime change the ACM in a planning scene diff (the `allowed_collision_matrix` field of the PlanningScene message) to allow gripper-object contact while grasping.
- `attachObject(id, link, touch_links)` on MoveGroupInterface allows collisions between the object and listed links (fingers).
- Collision checkers: FCL default; Bullet is an optional alternative (Bullet collision checker tutorial). Look up padding settings in your release's planning scene API.

## Gotchas
- Allowing too many pairs hides real collisions; limit to the fingers and the held object.
- Mesh collision shapes with many triangles slow planning; use convex decompositions or primitives.

## Self-check
The planning scene reports no contacts for the grasp pose after the ACM change.

## Checked
2026-11-03: parameter, plugin, API and command names compared with the MoveIt 2 sources (moveit2 repository headers, servo_parameters.yaml, servo_node.cpp, datatypes.hpp, moveit_py bindings; moveit2_tutorials pages for controller configuration, OMPL, Pilz, setup assistant and Bullet). Removed or corrected: SRDF reason enum, `/check_state_validity` and `setCollisionPadding` (not found in the sources).

Method: documentation only; no commands were run.
