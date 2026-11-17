---
id: computing-software.robotics-software.robot-perception-slam.imu-odometry-covariance
name: imu-odometry-covariance
category: computing-software
field: robotics-software
product: robot-perception-slam
tags: [imu-odom-quality, imu-filter-madgwick, covariance, wheel-odometry, calibration-bias, gravity]
level: advanced
status: docs-checked
description: "Prepare IMU and wheel odometry for fusion: orientation filtering, covariances, bias and odometry calibration."
sources:
  - https://github.com/ros2/common_interfaces/blob/rolling/sensor_msgs/msg/Imu.msg
  - https://github.com/cra-ros-pkg/robot_localization/blob/rolling-devel/doc/preparing_sensor_data.rst
  - https://github.com/CCNYRoboticsLab/imu_tools/blob/rolling/imu_filter_madgwick/src/imu_filter_ros.cpp
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# IMU, odometry and covariance
- `sensor_msgs/Imu`: linear acceleration in m/s^2, angular velocity in rad/s, each with a covariance matrix (`orientation_covariance`, `angular_velocity_covariance`, `linear_acceleration_covariance`, row major about x, y, z). If there is no orientation estimate, set element 0 of `orientation_covariance` to -1; consumers check for that value.
- Follow REP 103 (units and axis conventions) for every sensor you give to `robot_localization`; check that the signs are right (turn the robot counter-clockwise and yaw must increase).
- Covariance values matter to `robot_localization`. Do not inflate covariances to make the filter ignore a variable; set that variable to `false` in the sensor's config vector instead.
- A variable you fuse should not have a variance of 0; the nodes add a small epsilon (1e-6) when they find 0, and the docs say setting a sensible value yourself is better.
- Velocity data should be in the frame given by `base_link_frame`, or a transform from its `frame_id` to `base_link_frame` must exist.
- `robot_localization` assumes an IMU in its neutral right-side-up position on a flat surface measures +9.81 m/s^2 on the Z axis (and +9.81 on Y if rolled +90 degrees).
- Two sources of orientation: fuse both only if both give accurate covariances; otherwise fuse one.
- `imu_filter_madgwick` (imu_tools) parameters: `use_mag` (default true), `publish_tf` (default true), `world_frame` (default `enu`; `ned` and `nwu` also accepted).

## Gotchas
- A driver that reports a zero covariance diagonal for a fused variable makes the filter over-trust that sensor.
- Wrong `frame_id` on velocity data is a common reason a sensor seems to have no effect.

## Self-check
`ros2 topic echo --once /imu/data` shows about 9.8 m/s^2 on the up axis at rest and a covariance that is not all zeros.

## Checked
2026-11-03. Confirmed in `Imu.msg` (units, covariance fields, -1 rule), robot_localization `preparing_sensor_data.rst` (REP 103, covariance, config vector advice, epsilon, frame rule, 9.81 on Z, two orientation sources) and the imu_filter_madgwick source (parameter names and defaults). Removed: gyro bias settling times, wheel odometry calibration and UMBmark claims, magnetometer-indoors advice, driver clock claims and the 360-degree self-check numbers.
Method: documentation only; no commands were run.
