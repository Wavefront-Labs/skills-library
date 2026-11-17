---
id: computing-software.robotics-software.moveit-manipulation.collision-objects-scene
name: collision-objects-scene
category: computing-software
field: robotics-software
product: moveit-manipulation
tags: [planning-scene, collision-objects, planning-scene-interface, attach-object, octomap, apply-planning-scene, moveit-planning-scene]
level: practitioner
status: docs-checked
description: "Add, move, attach and remove collision objects with PlanningSceneInterface."
sources:
  - https://moveit.picknik.ai/main/index.html
  - https://github.com/moveit/moveit2
  - https://github.com/moveit/moveit2_tutorials
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Planning scene
```cpp
moveit::planning_interface::PlanningSceneInterface psi;
moveit_msgs::msg::CollisionObject o;
o.header.frame_id = mg.getPlanningFrame(); o.id = "box1";
shape_msgs::msg::SolidPrimitive p; p.type = p.BOX; p.dimensions = {0.1, 0.1, 0.1};
geometry_msgs::msg::Pose pose; pose.position.x = 0.4; pose.orientation.w = 1.0;
o.primitives.push_back(p); o.primitive_poses.push_back(pose); o.operation = o.ADD;
psi.applyCollisionObjects({o});
mg.attachObject("box1", "panda_hand");        // object moves with the gripper
mg.detachObject("box1"); psi.removeCollisionObjects({"box1"});
```
- Meshes via `shape_msgs/Mesh`. Sensor data: OctoMap through the `occupancy_map_monitor` plugin with a point cloud or depth image updater.
- Scene is shared through `/planning_scene` and `/monitored_planning_scene`; RViz Planning Scene display edits it.
- Attached objects are included in collision checks as part of the robot.

## Gotchas
- Wrong `frame_id` places the object elsewhere.
- Objects are applied asynchronously; wait briefly or use `applyCollisionObjects` before planning.

## Self-check
Planning around the box avoids it, and after removal planning takes the shorter path.

## Checked
2026-11-03: parameter, plugin, API and command names compared with the MoveIt 2 sources (moveit2 repository headers, servo_parameters.yaml, servo_node.cpp, datatypes.hpp, moveit_py bindings; moveit2_tutorials pages for controller configuration, OMPL, Pilz, setup assistant and Bullet). Removed or corrected: nothing needed removal.

Method: documentation only; no commands were run.
