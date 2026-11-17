---
id: computing-software.robotics-software.robot-simulation-gazebo.sensors-lidar-camera-imu
name: sensors-lidar-camera-imu
category: computing-software
field: robotics-software
product: robot-simulation-gazebo
tags: [gz-sensors, gpu-lidar, rgbd-camera, imu-sensor, update-rate]
level: practitioner
status: docs-checked
description: "Configure SDF lidar, camera and IMU sensor elements: scan, range, image, clip, noise, reference frame."
sources:
  - https://raw.githubusercontent.com/gazebosim/sdformat/sdf14/sdf/1.11/sensor.sdf
  - https://raw.githubusercontent.com/gazebosim/sdformat/sdf14/sdf/1.11/lidar.sdf
  - https://raw.githubusercontent.com/gazebosim/sdformat/sdf14/sdf/1.11/camera.sdf
  - https://raw.githubusercontent.com/gazebosim/sdformat/sdf14/sdf/1.11/imu.sdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Gazebo sensors in SDF (SDF 1.11 spec)
Common `<sensor name type>` elements: `always_on` (default false), `update_rate` (default 0:
data every cycle), `visualize`, `topic`, `enable_metrics`, plus `pose` and `plugin`. Types
include `lidar`, `gpu_lidar`, `camera`, `depth_camera`, `rgbd_camera`, `thermal_camera`,
`segmentation_camera`, `boundingbox_camera`, `imu`, `navsat`, `contact`, `altimeter`,
`magnetometer`. `gpu_ray` and `ray` are legacy aliases of `gpu_lidar` and `lidar`.

## Lidar
```xml
<sensor name="lidar" type="gpu_lidar">
  <topic>scan</topic><update_rate>10</update_rate><always_on>true</always_on>
  <lidar>
    <scan><horizontal><samples>360</samples><min_angle>-3.14</min_angle><max_angle>3.14</max_angle></horizontal></scan>
    <range><min>0.1</min><max>12</max></range>
    <noise><type>gaussian</type><mean>0</mean><stddev>0.01</stddev></noise>
  </lidar>
</sensor>
```
Values are illustrative. `scan/horizontal` needs `samples` (default 640), `resolution`
(multiplies samples; if not 1 the data is interpolated), `min_angle`, `max_angle` (must be
at least `min_angle`); `vertical` is optional (samples default 1). `range` needs `min` and
`max`. Noise type is `gaussian` with `mean` and `stddev`. `visibility_mask` controls which
visuals the lidar sees.

## Camera
`<camera>`: `horizontal_fov` (default 1.047 rad), `image` (`width` 320, `height` 240,
`format` R8G8B8 by default, `anti_aliasing`), `clip` (`near` 0.1, `far` 100), `noise`
(gaussian, per pixel), `distortion` (k1, k2, k3, p1, p2, center), `lens`, `camera_info_topic`,
`optical_frame_id` (frame id used in the camera_info header), `triggered`/`trigger_topic`,
`save`. Depth cameras use `depth_camera` (`output`, own `clip`, far default 10);
`segmentation_type` is `semantic` or `panoptic`/`instance`; `box_type` is `2d`, `full_2d`
or `3d`. `lens/intrinsics` (fx, fy, cx, cy, s) override `horizontal_fov`.

## IMU
- `orientation_reference_frame/localization`: `CUSTOM` (default, uses `custom_rpy` and
  `parent_frame`), `NED`, `ENU`, `NWU`, `GRAV_UP`, `GRAV_DOWN` (with `grav_dir_x`).
- `angular_velocity` (rad/s) and `linear_acceleration` (m/s^2) each take per-axis `x`, `y`,
  `z` with optional noise.
- `enable_orientation` (default true) turns orientation output on or off.

## Self-check
`gz topic -e -t /scan` prints data from the topic you set; `gz topic -ft <topic>` shows a
frequency close to `update_rate`.

## Checked
Method: docs-checked 2026-11-09 against the sdformat 1.11 sensor.sdf, lidar.sdf, camera.sdf and imu.sdf (raw GitHub, read in full). Removed as unconfirmed: the `<gz_frame_id>` element and ROS frame_id derivation, "low RTF lowers real sensor rate", the requirement for the Sensors and Imu system plugins in the world, topic scoping rules, the `ros2 topic hz` check, and the landing-page source gazebosim.org/docs. The self-check relies on `gz topic` usage confirmed in other Gazebo tutorials.
