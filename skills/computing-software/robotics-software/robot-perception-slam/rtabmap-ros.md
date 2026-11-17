---
id: computing-software.robotics-software.robot-perception-slam.rtabmap-ros
name: rtabmap-ros
category: computing-software
field: robotics-software
product: robot-perception-slam
tags: [rtabmap, rtabmap-launch, rgbd-slam, loop-closure, rtabmap-db, localization-mode, slam-3d-visual]
level: advanced
status: docs-checked
description: "Run RTAB-Map with RGB-D or stereo cameras: topics, frames, database, mapping vs localization."
sources:
  - https://github.com/introlab/rtabmap_ros/blob/ros2/README.md
  - https://github.com/introlab/rtabmap_ros/blob/ros2/rtabmap_launch/launch/rtabmap.launch.py
  - https://github.com/introlab/rtabmap_ros/blob/ros2/rtabmap_sync/README.md
  - https://github.com/introlab/rtabmap_ros/blob/ros2/AGENTS.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# RTAB-Map with ROS 2
```bash
sudo apt install ros-$ROS_DISTRO-rtabmap-ros
ros2 launch rtabmap_launch rtabmap.launch.py rgb_topic:=/camera/color/image_raw depth_topic:=/camera/depth/image_raw camera_info_topic:=/camera/color/camera_info frame_id:=base_link approx_sync:=false args:="--delete_db_on_start"
ros2 launch rtabmap_launch rtabmap.launch.py localization:=true database_path:=~/.ros/rtabmap.db   # reuse the map
```
- `rtabmap.launch.py` arguments (defaults): `rgb_topic` (`/camera/rgb/image_rect_color`), `depth_topic` (`/camera/depth_registered/image_raw`), `camera_info_topic` (`/camera/rgb/camera_info`), `frame_id` (`base_link`), `map_frame_id` (`map`), `database_path` (`~/.ros/rtabmap.db`), `localization` (`false`), `approx_sync` (`false`), `approx_sync_max_interval` (`0.0`), `visual_odometry` (`true`), `icp_odometry` (`false`), `odom_topic` (`odom`), `use_sim_time` (`false`), `rtabmap_viz` (`true`), `rviz` (`false`).
- `args` passes RTAB-Map parameters or flags such as `--delete_db_on_start` to the node. Parameters use the `Group/Name` form, for example `Rtabmap/DetectionRate` and `Reg/Strategy`; their definitions are in rtabmap's `Parameters.h`, not in `rtabmap_ros`.
- `database_path` is where the map is saved and loaded. `localization:=true` launches in localization mode.
- With `visual_odometry:=true` the launch starts RTAB-Map's own visual odometry node; set it to `false` and provide your own odometry (`odom_topic` or TF with `odom_frame_id`) when you have wheel or lidar odometry.
- Sync: the `rtabmap_sync` README says to prefer exact synchronisation wherever the sensor allows it, and warns that approximate sync pairs whatever it has; `approx_sync_max_interval` limits how far apart a set may be (0 disables the limit). `rgbd_sync` defaults to approximate.

## Gotchas
- The default topic names do not match most camera drivers; always pass your own `rgb_topic`, `depth_topic` and `camera_info_topic`.
- Without `--delete_db_on_start`, a new session adds to the existing database at `database_path`.

## Self-check
The map builds in RTAB-Map's viewer or RViz and a return to a known place gives a loop closure.

## Checked
2026-11-03. Confirmed in the rtabmap_ros README (apt package), `rtabmap.launch.py` (argument names and defaults, `args` description), `rtabmap_sync/README.md` (sync advice) and AGENTS.md (parameter naming). Removed: the SQLite claim, `/rtabmap/cloud_map` output topics, the `--Kp/DetectorStrategy` flag, loop closure viewer steps and any claim about the map output formats.
Method: documentation only; no commands were run.
