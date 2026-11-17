---
id: computing-software.robotics-software.robot-perception-slam.robot-localization-ekf
name: robot-localization-ekf
category: computing-software
field: robotics-software
product: robot-perception-slam
tags: [robot-localization, ekf-node, ukf-node, two-d-mode, odom0-config, navsat-transform, sensor-fusion]
level: advanced
status: docs-checked
description: "Fuse odometry, IMU and GPS with robot_localization EKF: sensor config matrices, frames and 2D mode."
sources:
  - https://github.com/cra-ros-pkg/robot_localization/blob/rolling-devel/params/ekf.yaml
  - https://github.com/cra-ros-pkg/robot_localization/blob/rolling-devel/doc/state_estimation_nodes.rst
  - https://github.com/cra-ros-pkg/robot_localization/blob/rolling-devel/doc/preparing_sensor_data.rst
  - https://github.com/cra-ros-pkg/robot_localization/blob/rolling-devel/doc/integrating_gps.rst
  - https://github.com/cra-ros-pkg/robot_localization/blob/rolling-devel/doc/navsat_transform_node.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# robot_localization EKF
```yaml
ekf_filter_node:
  ros__parameters:
    frequency: 30.0          # default 30
    two_d_mode: true
    publish_tf: true
    map_frame: map
    odom_frame: odom
    base_link_frame: base_link
    world_frame: odom        # odom for continuous data
    odom0: /wheel/odometry
    odom0_config: [false, false, false,    # x, y, z
                   false, false, false,    # roll, pitch, yaw
                   true,  true,  false,    # vx, vy, vz
                   false, false, true,     # vroll, vpitch, vyaw
                   false, false, false]    # ax, ay, az
    imu0: /imu/data
    imu0_config: [false, false, false,  false, false, true,  false, false, false,  false, false, true,  true, false, false]
```
- The config vector order is x, y, z, roll, pitch, yaw, vx, vy, vz, vroll, vpitch, vyaw, ax, ay, az. A `true` entry fuses that variable; use `false` rather than inflated covariance to ignore one.
- `world_frame`: set it to `odom_frame` when fusing continuous data (wheel odometry, visual odometry, IMU); this is the default. When fusing global data that can jump (GPS, landmark updates), set it to `map_frame` and make sure something else (it can be another `robot_localization` node that does not fuse the global data) produces `odom` to `base_link`. Without a `map_frame`, remove it and keep `world_frame` equal to `odom_frame`.
- Frame defaults: `map`, `odom`, `base_link`. `publish_tf` is true by default in the example config.
- Sensor inputs are named `odom0`, `imu0`, `pose0`, `twist0` with matching `_config` vectors.
- Input quality: follow REP 103 and give covariances that make sense (see the IMU skill). With two sources of orientation, fuse both only if both have accurate covariances.
- GPS: run `navsat_transform_node`, which needs the robot's pose estimate (an `Odometry` message), an earth-referenced heading (IMU) and a `sensor_msgs/NavSatFix`. Its IMU should read yaw 0 when facing east; `yaw_offset` fixes an IMU that reads 0 facing north (pi/2).

## Gotchas
- With `world_frame: map`, something else must generate `odom` to `base_link`, or the tree is incomplete.
- A zero variance on a fused variable gets a small epsilon added; give real variances.

## Self-check
The filtered odometry output is smooth and the `odom` to `base_link` transform follows the robot in RViz.

## Checked
2026-11-03. Confirmed in robot_localization `params/ekf.yaml` (parameters, defaults, config vector order, world_frame comments), `state_estimation_nodes.rst`, `preparing_sensor_data.rst` (covariance and orientation sources), `integrating_gps.rst` and `navsat_transform_node.rst` (inputs, east heading, `yaw_offset`). Removed: the advice to avoid fusing the same quantity twice (replaced by the orientation caution), datasheet covariance advice, the claim that the IMU must be aligned with `base_link`, and driver `publish_tf` advice.
Method: documentation only; no commands were run.
