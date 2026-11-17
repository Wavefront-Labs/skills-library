---
id: computing-software.robotics-software.robot-perception-slam.lidar-odometry-3d
name: lidar-odometry-3d
category: computing-software
field: robotics-software
product: robot-perception-slam
tags: [lidar-odometry, kiss-icp, 3d-lidar-slam, scan-matching, deskew, point-cloud-map]
level: advanced
status: docs-checked
description: "Choose 3D LiDAR odometry/SLAM (KISS-ICP, LIO-SAM style) and wire frames, deskewing and downsampling."
sources:
  - https://github.com/PRBonn/kiss-icp/blob/main/ros/README.md
  - https://github.com/PRBonn/kiss-icp/blob/main/ros/config/config.yaml
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# 3D lidar odometry with KISS-ICP
```bash
git clone https://github.com/PRBonn/kiss-icp && colcon build && source ./install/setup.bash   # from the workspace per the README
ros2 launch kiss_icp odometry.launch.py topic:=/lidar/points base_frame:=lidar_cloud visualize:=false
ros2 bag play <path>      # in a second shell
```
- The only required launch argument is `topic`, the `PointCloud2` topic to process. Optional: `bagfile:=<path>` to launch with a bag; `visualize:=false` disables the default RViz2 window.
- ROS-related parameters can be given at launch or in the yaml: `base_frame`, `lidar_odom_frame`, `publish_odom_tf`, `invert_odom_tf`, `position_covariance`, `orientation_covariance`. Values set in the yaml file override the launch arguments.
- The algorithm parameters live in a yaml file (default is the one in the package share directory, pass your own with the `config_file` launch argument). Node name `kiss_icp_node`. Example sections: `data` (`deskew` True, `max_range` 100.0, `min_range`), `mapping` (`voxel_size` optional, default `max_range / 100.0`; `max_points_per_voxel` 20), `adaptive_threshold` and `registration`.
- The config file in the repository is described as an example of advanced options, not tuned for a specific dataset.

## Gotchas
- Set `base_frame` to the frame the lidar cloud is in or has a transform to, or the output frames are wrong.
- Parameters in the yaml silently win over the same names on the command line.

## Self-check
Drive a loop; the odometry path in RViz returns close to the start.

## Checked
2026-11-03. Confirmed in the KISS-ICP ROS README (build, launch command, arguments, ROS parameters, override rule) and `ros/config/config.yaml` (node name, sections, defaults). Removed: LIO-SAM and FAST-LIO comparisons, voxel size recommendations, octomap use, the evo evaluation steps and the extrinsic and per-point timestamp claims.
Method: documentation only; no commands were run.
