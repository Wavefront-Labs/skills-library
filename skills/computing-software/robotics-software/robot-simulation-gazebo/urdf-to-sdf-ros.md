---
id: computing-software.robotics-software.robot-simulation-gazebo.urdf-to-sdf-ros
name: urdf-to-sdf-ros
category: computing-software
field: robotics-software
product: robot-simulation-gazebo
tags: [urdf-sdf, gazebo-tags, ros-gz-xacro, robot-description, spawn-entity, ros-gz-sim-create]
level: advanced
status: draft
description: "Move a ROS robot into Gazebo: URDF/xacro to SDF, gazebo extension tags, spawn with ros_gz_sim create."
sources:
  - https://gazebosim.org/docs
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# URDF to Gazebo
```bash
ros2 run ros_gz_sim create -topic robot_description -name my_robot -z 0.1     # spawn from the parameter published by robot_state_publisher
ros2 run ros_gz_sim create -file model.sdf -name box
```
- Gazebo converts URDF at load, but needs: `<inertial>` on every link, `<collision>`, and joint `<limit>`. Use `<gazebo>` tags for materials, friction (`<surface>`), and plugins; `<gazebo reference="link">`.
- Gazebo plugins in URDF use `<gazebo><plugin filename="gz-sim-diff-drive-system" name="gz::sim::systems::DiffDrive">...</plugin></gazebo>`.
- ros2_control in sim: `<ros2_control>` hardware `gz_ros2_control/GazeboSimSystem` plus plugin `gz_ros2_control::GazeboSimROS2ControlPlugin` (package gz_ros2_control; Fortress used `ign_ros2_control`).
- `package://` mesh URIs work through ROS integration for spawn; check resource paths if meshes are missing.

## Gotchas
- Fixed joints with massless links get merged/dropped by the URDF-to-SDF converter ("lumping"); keep `preserveFixedJoint` where needed.
- Missing `use_sim_time:=true` in robot_state_publisher breaks tf.

## Self-check
Robot spawns, `robot_state_publisher` tf matches the Gazebo pose, wheels turn when commanded.
