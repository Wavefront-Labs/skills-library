---
id: computing-software.robotics-software.robot-simulation-gazebo.ros-gz-launch-sim
name: ros-gz-launch-sim
category: computing-software
field: robotics-software
product: robot-simulation-gazebo
tags: [ros-gz-sim, gz-sim-launch, ros-gz-sim-create, launch-integration]
level: practitioner
status: docs-checked
description: "Launch Gazebo from ROS 2 with ros_gz_sim, spawn models with create and export model paths in package.xml."
sources:
  - https://raw.githubusercontent.com/gazebosim/ros_gz/ros2/ros_gz_sim/README.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# ros_gz_sim launch integration
`ros_gz_sim` provides launch files and ROS-enabled executables for Gazebo Sim.

## Run Gazebo
```bash
ros2 launch ros_gz_sim gz_sim.launch.py gz_args:="shapes.sdf"
```
`gz_args` carries the arguments passed to Gazebo (world file and any flags).
From a Python launch file include `gz_sim.launch.py` with `IncludeLaunchDescription` and
pass `launch_arguments={'gz_args': ...}`.

## Spawn entities
The `create` executable spawns SDF or URDF entities from a file on disk or Gazebo Fuel, or
from a ROS parameter:
```bash
ros2 run ros_gz_sim create -world default -file 'https://fuel.gazebosim.org/1.0/openrobotics/models/Gazebo'
ros2 run ros_gz_sim create --helpshort   # all options
```

## Export model and plugin paths from package.xml
Inside `<export>`, `<gazebo_ros>` attributes extend Gazebo search paths:
- `gazebo_model_path` and `gazebo_media_path` are appended to `GZ_SIM_RESOURCE_PATH`.
- `plugin_path` is appended to `GZ_SIM_SYSTEM_PLUGIN_PATH`.
- `${prefix}` expands to the package share path.
```xml
<export>
  <gazebo_ros gazebo_model_path="${prefix}/../"/>
</export>
```
Install the directory from CMake, for example `install(DIRECTORY models DESTINATION share/${PROJECT_NAME})`.
With `${prefix}/../` a world can reference `package://my_awesome_pkg/models/cool_robot`;
with `${prefix}/models` the reference is `package://cool_robot`, which may clash with
other models.

## SetEntityState
Pose, twist and acceleration fields are applied only when `set_pose`, `set_twist` or
`set_acceleration` is true; all false leaves the entity unchanged.

## Self-check
`ros2 launch ros_gz_sim gz_sim.launch.py gz_args:="shapes.sdf"` opens the world.

## Checked
Method: docs-checked 2026-11-09 against the ros_gz_sim README.md (ros2 branch, read in full). Removed as unconfirmed: the `-topic robot_description -name` create arguments, launch ordering and `/world/<name>/create` wait, `-r -v2` flags, `use_sim_time` and tf-lookup claims, robot_state_publisher wiring, and the landing-page source gazebosim.org/docs.
