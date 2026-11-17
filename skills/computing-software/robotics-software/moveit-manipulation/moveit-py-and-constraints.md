---
id: computing-software.robotics-software.moveit-manipulation.moveit-py-and-constraints
name: moveit-py-and-constraints
category: computing-software
field: robotics-software
product: moveit-manipulation
tags: [moveit-py, moveit-py, path-constraints, orientation-constraint, goal-constraints, jump-threshold]
level: advanced
status: docs-checked
description: "Use the moveit_py Python API and add path or goal constraints to planning requests."
sources:
  - https://moveit.picknik.ai/main/index.html
  - https://github.com/moveit/moveit2
  - https://github.com/moveit/moveit2_tutorials
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# moveit_py and constraints
- `moveit_py` (Humble onwards; API still evolving, check docs):
```python
from moveit.planning import MoveItPy
moveit = MoveItPy(node_name="moveit_py")
arm = moveit.get_planning_component("panda_arm")
arm.set_start_state_to_current_state()
arm.set_goal_state(configuration_name="ready")
result = arm.plan()
if result: moveit.execute(result.trajectory, controllers=[])
```
- Constraints in C++: `moveit_msgs::msg::Constraints` with `OrientationConstraint` (link, absolute tolerances, weight) set via `setPathConstraints()`; clear with `clearPathConstraints()`.
- Goals can be constraint sets (position + orientation tolerance) instead of exact poses.
- Constrained planning needs more planning time and works best with a constraint-aware state space (`ompl` projection / constrained planning configs).

## Gotchas
- Start state that violates the path constraint makes planning fail; start from a satisfying state.
- Python APIs: moveit_py is not the same as ROS 1 moveit_commander.

## Self-check
A plan with an orientation path constraint keeps the tool upright along the trajectory.

## Checked
2026-11-03: parameter, plugin, API and command names compared with the MoveIt 2 sources (moveit2 repository headers, servo_parameters.yaml, servo_node.cpp, datatypes.hpp, moveit_py bindings; moveit2_tutorials pages for controller configuration, OMPL, Pilz, setup assistant and Bullet). Removed or corrected: nothing needed removal.

Method: documentation only; no commands were run.
