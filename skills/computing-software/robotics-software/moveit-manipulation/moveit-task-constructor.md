---
id: computing-software.robotics-software.moveit-manipulation.moveit-task-constructor
name: moveit-task-constructor
category: computing-software
field: robotics-software
product: moveit-manipulation
tags: [task-constructor, mtc, pick-and-place, generate-grasp-pose, serial-container, compute-ik-stage]
level: advanced
status: docs-checked
description: "Compose pick-and-place pipelines with MoveIt Task Constructor stages and containers."
sources:
  - https://moveit.picknik.ai/main/index.html
  - https://github.com/moveit/moveit2
  - https://github.com/moveit/moveit2_tutorials
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# MoveIt Task Constructor (MTC)
Concept: a `Task` is a tree of stages: generators (e.g. `CurrentState`, `GenerateGraspPose`, `GeneratePlacePose`), propagators (`MoveTo`, `MoveRelative`, `ComputeIK` wraps a generator), and connectors (`Connect`) joined in `SerialContainer`s.
```cpp
moveit::task_constructor::Task task; task.stages()->setName("pick");
task.loadRobotModel(node);
task.add(std::make_unique<mtc::stages::CurrentState>("current"));
// planners: mtc::solvers::PipelinePlanner, JointInterpolationPlanner, CartesianPath
task.add(std::make_unique<mtc::stages::MoveTo>("open hand", interpolation_planner));
// ... Connect, SerialContainer{ approach (MoveRelative), GenerateGraspPose -> ComputeIK, allowCollisions, close hand, attach object, lift }
task.plan(); task.execute(*task.solutions().front());
```
- Needs the `moveit_task_constructor_core` package (separate from MoveIt; source build in some distros).
- RViz plugin shows solutions and failure reasons per stage.
- Properties propagate (`group`, `eef`, `ik_frame`, `target_pose`).

## Gotchas
- Ordering errors surface as "no solution"; use the RViz stage view to find the failing stage.
- Stage names must be unique.

## Self-check
Task planning returns at least one solution and execute completes the full pick in simulation.

## Checked
2026-11-03: parameter, plugin, API and command names compared with the MoveIt 2 sources (moveit2 repository headers, servo_parameters.yaml, servo_node.cpp, datatypes.hpp, moveit_py bindings; moveit2_tutorials pages for controller configuration, OMPL, Pilz, setup assistant and Bullet). Removed or corrected: nothing needed removal.

Method: documentation only; no commands were run.
