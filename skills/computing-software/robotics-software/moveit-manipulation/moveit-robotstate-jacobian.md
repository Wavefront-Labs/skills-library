---
id: computing-software.robotics-software.moveit-manipulation.moveit-robotstate-jacobian
name: moveit-robotstate-jacobian
category: computing-software
field: robotics-software
product: moveit-manipulation
tags: [robot-state, robotstate, jacobian-moveit, forward-kinematics-moveit, joint-model-group, setfromik]
level: advanced
status: docs-checked
description: "Use RobotModel and RobotState in C++ for forward kinematics, IK and the Jacobian."
sources:
  - https://moveit.picknik.ai/main/index.html
  - https://github.com/moveit/moveit2
  - https://github.com/moveit/moveit2_tutorials
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# RobotModel and RobotState
```cpp
moveit::core::RobotModelPtr model = robot_model_loader::RobotModelLoader(node, "robot_description").getModel();
moveit::core::RobotState st(model);
const auto* jmg = model->getJointModelGroup("panda_arm");
st.setToRandomPositions(jmg);
const Eigen::Isometry3d& T = st.getGlobalLinkTransform("panda_link8");     // FK
bool ok = st.setFromIK(jmg, T, 0.1);                                       // IK, 0.1 s timeout
Eigen::MatrixXd J; st.getJacobian(jmg, st.getLinkModel("panda_link8"), Eigen::Vector3d::Zero(), J);
```
- `getJacobian` returns a 6xN matrix (linear rows, then angular); use for singularity checks (`svd` min singular value).
- State is only a model snapshot; to read the live robot use `PlanningSceneMonitor`/`getCurrentState`.
- Eigen types: `Isometry3d` for poses.

## Gotchas
- `setFromIK` uses the group's configured solver; fails if none is loaded.
- State must be `update()`d after setting joints before reading link transforms (`st.update()`).

## Self-check
FK of an IK solution reproduces the target pose within the solver tolerance.

## Checked
2026-11-03: parameter, plugin, API and command names compared with the MoveIt 2 sources (moveit2 repository headers, servo_parameters.yaml, servo_node.cpp, datatypes.hpp, moveit_py bindings; moveit2_tutorials pages for controller configuration, OMPL, Pilz, setup assistant and Bullet). Removed or corrected: nothing needed removal.

Method: documentation only; no commands were run.
