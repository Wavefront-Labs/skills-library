---
id: computing-software.robotics-software.robot-perception-slam.depth-to-scan-cloud
name: depth-to-scan-cloud
category: computing-software
field: robotics-software
product: robot-perception-slam
tags: [depth-image-proc, pointcloud-to-laserscan, depthimage-to-laserscan, registered-cloud, depth-camera, laserscan]
level: advanced
status: docs-checked
description: "Create point clouds from depth images and flatten clouds to LaserScan for 2D navigation."
sources:
  - https://github.com/ros-perception/image_pipeline/blob/rolling/depth_image_proc/doc/components.rst
  - https://github.com/ros-perception/pointcloud_to_laserscan/blob/rolling/README.md
  - https://github.com/ros-perception/depthimage_to_laserscan/blob/ros2/README.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Depth to cloud and scan
- `depth_image_proc` components: `PointCloudXyzNode` (subscribes `image_rect` and `camera_info`, publishes `points`) and `PointCloudXyzrgbNode` (subscribes `depth_registered/image_rect`, `rgb/image_rect_color` and `rgb/camera_info`, publishes `points`). Each is also available as a standalone node such as `point_cloud_xyz_node`.
- Depth image encoding: 16UC1 is interpreted as millimetres and 32FC1 as metres. `ConvertMetricNode` converts uint16 millimetre depth to float metres.
- `pointcloud_to_laserscan` (`PointCloudToLaserScanNode`): subscribes `cloud_in`, publishes `scan`. Parameters: `min_height`, `max_height`, `angle_min`, `angle_max`, `angle_increment` (default pi/180), `range_min`, `range_max`, `scan_time`, `use_inf`, `target_frame` (transform the cloud first; default none) and `transform_tolerance` (default 0.01 s, used only with `target_frame`). No input is processed unless `scan` has a subscriber.
- `depthimage_to_laserscan`: subscribes `depth` and `depth_camera_info`, publishes `scan`. Parameters: `scan_time`, `range_min` (default 0.45 m), `range_max` (default 10.0 m), `scan_height` (the row of the depth image used for the projection, default 1) and `output_frame`.

## Gotchas
- Choose `min_height`/`max_height` as a band that excludes the floor, or floor points enter the scan.
- With `target_frame` set, tf must be available for the cloud's stamp within `transform_tolerance`.

## Self-check
The scan from the depth camera lines up with a real lidar scan in RViz.

## Checked
2026-11-03. Confirmed in the depth_image_proc component docs (topics, encodings, standalone node names), the pointcloud_to_laserscan README and source (topics, parameters and defaults) and the depthimage_to_laserscan README and source (topics, parameters, defaults). Removed: the Nav2 costmap and slam_toolbox usage claims and the camera-driver specific height advice.
Method: documentation only; no commands were run.
