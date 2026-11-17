---
id: computing-software.robotics-software.robot-simulation-gazebo.ros-gz-bridge
name: ros-gz-bridge
category: computing-software
field: robotics-software
product: robot-simulation-gazebo
tags: [ros-gz-bridge, parameter-bridge, bridge-yaml, gz-msgs, clock-bridge, image-bridge, gz-ros-integration]
level: practitioner
status: docs-checked
description: "Bridge ROS 2 and Gazebo topics and services with ros_gz_bridge using arguments, YAML or launch files."
sources:
  - https://raw.githubusercontent.com/gazebosim/ros_gz/ros2/ros_gz_bridge/README.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# ros_gz_bridge
Bridges messages between ROS and Gazebo Transport. The README lists the supported ROS to
`gz.msgs` type pairs (for example `std_msgs/msg/String` to `gz.msgs.StringMsg`,
`sensor_msgs/msg/Image` to `gz.msgs.Image`, `sensor_msgs/msg/LaserScan` to
`gz.msgs.LaserScan`, `geometry_msgs/msg/Twist` to `gz.msgs.Twist`, `rosgraph_msgs/msg/Clock`
to `gz.msgs.Clock`) and four service pairs (ControlWorld, DeleteEntity, SpawnEntity,
SetEntityPose). Run `ros2 run ros_gz_bridge parameter_bridge -h` for the argument syntax.

## Command line
```bash
ros2 run ros_gz_bridge parameter_bridge /chatter@std_msgs/msg/String@gz.msgs.StringMsg
ros2 run ros_gz_bridge parameter_bridge /clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock
```
The README's examples use `@` (bidirectional) and `[` (Gazebo to ROS) in the topic spec.
Services: `/world/shapes/control@ros_gz_interfaces/srv/ControlWorld`, then
`ros2 service call /world/<world_name>/control ros_gz_interfaces/srv/ControlWorld "{world_control: {pause: false}}"`.

## Clock
If Gazebo detects another publisher on `/clock` at startup it creates only the fully
qualified `/world/<worldname>/clock`. Use a unidirectional `/clock` bridge as above so
Gazebo is the sole clock source. Alternatively `override_timestamps_with_wall_time:=true`
stamps outgoing headers with wall time (default false).

## YAML config
A YAML array of maps, loaded with
`ros2 run ros_gz_bridge parameter_bridge --ros-args -p config_file:=<file>`.
Keys: `topic_name` (applies to both sides) or `ros_topic_name` and `gz_topic_name`,
`ros_type_name`, `gz_type_name`, `subscriber_queue`, `publisher_queue` (default 10 if
`qos_profile` is empty), `lazy` (default false), `direction` (`BIDIRECTIONAL` default,
`GZ_TO_ROS`, `ROS_TO_GZ`), `qos_profile` (for example `SENSOR_DATA`), `frame_id`.

## Launch files
- XML: `<ros_gz_bridge bridge_name=...>` with `<topic .../>` and `<service .../>` children
  (attributes mirror the YAML keys; services use `gz_req_type_name` and
  `gz_rep_type_name`). Unlike YAML it supports substitutions such as `$(var world_name)`,
  and `config_file="..."` can be combined with the tags.
- Python: `Node(package="ros_gz_bridge", executable="parameter_bridge", parameters=[...])`
  with `bridge_names` and `bridges.<name>.<setting>` parameters.

## Other parameters
- `override_frame_id` (GZ to ROS): replace `header.frame_id`, for example to point camera
  `Image` and `CameraInfo` at a z-forward optical frame (REP-0103).
- `expand_gz_topic_names` (default false): apply the ROS namespace to Gazebo topics.
- `subscription_heartbeat` (default 1000 ms): how often lazy bridges check for subscribers.
- A `static_bridge` executable hard-codes a `/chatter` String bridge as an example.

## Self-check
`gz topic -t /chatter -m gz.msgs.StringMsg -p 'data:"Hello"'` appears in
`ros2 topic echo /chatter` with the first bridge command running.

## Checked
Method: docs-checked 2026-11-09 against the ros_gz_bridge README.md (ros2 branch, read in full). Removed as unconfirmed: the `ros_gz_image image_bridge` image_transport claim, `use_sim_time` advice, "many topics in one bridge is lighter" and the unsupported-pair error behaviour, the claim that CameraInfo and tf pose topics all need bridging, and the landing-page source gazebosim.org/docs.
