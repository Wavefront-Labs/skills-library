---
id: computing-software.robotics-software.robot-perception-slam.slam-toolbox-mapping
name: slam-toolbox-mapping
category: computing-software
field: robotics-software
product: robot-perception-slam
tags: [slam-toolbox, online-async, online-sync, mapper-params, save-map, serialize-map, slam-2d]
level: practitioner
status: docs-checked
description: "Build 2D maps with slam_toolbox online async or sync mode, tune parameters and save or serialize maps."
sources:
  - https://github.com/SteveMacenski/slam_toolbox/blob/ros2/README.md
  - https://github.com/SteveMacenski/slam_toolbox/blob/ros2/config/mapper_params_online_async.yaml
  - https://github.com/SteveMacenski/slam_toolbox/blob/ros2/launch/online_async_launch.py
  - https://github.com/SteveMacenski/slam_toolbox/blob/ros2/srv/SaveMap.srv
  - https://github.com/SteveMacenski/slam_toolbox/blob/ros2/srv/SerializePoseGraph.srv
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# slam_toolbox mapping
```bash
sudo apt install ros-$ROS_DISTRO-slam-toolbox
ros2 launch slam_toolbox online_async_launch.py slam_params_file:=/path/mapper_params_online_async.yaml use_sim_time:=false
ros2 service call /slam_toolbox/save_map slam_toolbox/srv/SaveMap "{name: {data: 'lab'}}"          # map image
ros2 service call /slam_toolbox/serialize_map slam_toolbox/srv/SerializePoseGraph "{filename: 'lab'}"   # pose graph
```
- Launch files in the package: `online_async_launch.py`, `online_sync_launch.py`, `offline_launch.py`, `localization_launch.py`, `lifelong_launch.py`; example parameter files are in `config/` (`mapper_params_online_async.yaml`, `mapper_params_online_sync.yaml` and others). The online launch files take `slam_params_file` and `use_sim_time`.
- The node subscribes to a laser scan and odometry and publishes the `map` to `odom` transform and the map.
- Services: `/slam_toolbox/save_map` (`slam_toolbox/SaveMap`, request field `std_msgs/String name`) saves the map image, usable for display or AMCL localization; `/slam_toolbox/serialize_map` (`SerializePoseGraph`, request `string filename`) saves the pose graph for continued mapping, slam_toolbox localization and offline work; `/slam_toolbox/deserialize_map` loads a saved pose graph.
- Main parameters: `odom_frame`, `map_frame`, `base_frame`, `scan_topic` (an absolute name such as `/scan`), `mode` (`mapping` or `localization`), `resolution` (example 0.05), `max_laser_range` (example 20.0), `minimum_travel_distance` and `minimum_travel_heading` (examples 0.5), `do_loop_closing` (example true).
- `scan_queue_size` should always be 1 in async mode. `throttle_scans` is the number of scans to throttle in synchronous mode.

## Gotchas
- `scan_topic` must be an absolute name.
- Save both files if you want to continue later: the map image alone cannot be loaded back as a pose graph.

## Self-check
The map grows in RViz as the robot moves and `ros2 run tf2_tools view_frames` shows `map` to `odom` to `base_link`.

## Checked
2026-11-03. Confirmed in the slam_toolbox README (node behaviour, services, parameters, install), the example parameter file, `online_async_launch.py` (launch arguments), and the `.srv` definitions (request fields). Removed: the descriptions of async versus sync scan handling beyond what the README states, driving-speed advice and the claim about `max_laser_range` letting noise in.
Method: documentation only; no commands were run.
