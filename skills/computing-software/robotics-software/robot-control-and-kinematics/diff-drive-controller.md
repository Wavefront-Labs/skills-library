---
id: computing-software.robotics-software.robot-control-and-kinematics.diff-drive-controller
name: diff-drive-controller
category: computing-software
field: robotics-software
product: robot-control-and-kinematics
tags: [diff-drive-controller, wheel-separation, wheel-radius, odom-diff-drive, cmd-vel-timeout, mobile-base-controller]
level: practitioner
status: docs-checked
description: "Configure diff_drive_controller for a two-wheel base: wheel geometry, odometry, cmd_vel and limits."
sources:
  - https://raw.githubusercontent.com/ros-controls/ros2_controllers/master/diff_drive_controller/doc/userdoc.rst
  - https://raw.githubusercontent.com/ros-controls/ros2_controllers/master/diff_drive_controller/src/diff_drive_controller_parameter.yaml
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# diff_drive_controller
The controller takes body velocity commands and translates them to wheel commands for a
differential drive base, and computes and publishes odometry from hardware feedback. It
offers task-space velocity, acceleration and jerk limits, automatic stop after a command
timeout, and is a chainable controller.

```yaml
diff_cont:
  ros__parameters:
    left_wheel_names: [left_wheel_joint]
    right_wheel_names: [right_wheel_joint]
    wheel_separation: 0.40      # shortest distance between left and right wheels
    wheel_radius: 0.05
    odom_frame_id: odom         # default
    base_frame_id: base_link    # default
    enable_odom_tf: true        # default
    cmd_vel_timeout: 0.5        # default; 0.0 disables the timeout
    linear.x.max_velocity: 1.0
    linear.x.max_acceleration: 1.0
    angular.z.max_velocity: 2.0
```
The numeric values are examples for your own robot; the parameter definition file lists
descriptions and defaults.

## Parameters worth knowing
- `left_wheel_names` and `right_wheel_names` must not be empty; `wheel_separation` and
  `wheel_radius` must be greater than zero.
- A wrong `wheel_separation` makes the robot behave incorrectly in curves; a wrong
  `wheel_radius` makes it move faster or slower than expected.
- Correction factors exist for deviations from the nominal geometry:
  `wheel_separation_multiplier`, `left_wheel_radius_multiplier`,
  `right_wheel_radius_multiplier` (all default 1.0).
- `pose_covariance_diagonal` and `twist_covariance_diagonal` default to zeros; the file
  suggests starting from 0.001 on five entries and 0.01 on the last, then tuning to your
  robot's odometry data.
- `open_loop: true` computes odometry from commanded values instead of feedback.
  `position_feedback` (default true) selects joint position feedback; false uses velocity.
- `tf_frame_prefix` is prepended to the odom and base frame ids; if empty, the
  controller's namespace is used. `tf_frame_prefix_enable` is deprecated.
- `publish_limited_velocity: true` publishes the limited command on `~/cmd_vel_out`.
  `velocity_rolling_window_size` defaults to 10.
- Limits are set per axis under `linear.x` and `angular.z`: max and min velocity,
  acceleration, deceleration, reverse variants (default to the negated forward values if
  unset) and jerk; unset limits default to NaN.

## Interfaces
- Subscribes to `~/cmd_vel` as `geometry_msgs/msg/TwistStamped`; only linear x and angular
  z are used.
- Publishes `~/odom` (`nav_msgs/msg/Odometry`) and `/tf` (only if `enable_odom_tf` is
  true). Service `~/set_odometry` sets the current odometry.
- Uses wheel joint position (or velocity when `position_feedback` is false) as state
  feedback, and commands joint velocity.
- In chained mode it exposes `<controller_name>/linear/velocity` (m/s) and
  `<controller_name>/angular/velocity` (rad/s) for a preceding controller.

## Gotchas
- Swapped left and right wheel lists mirror the turning.
- Wheel radius and separation errors scale odometry; correct them with the multipliers
  after measuring.

## Self-check
Commanding 0.2 m/s for 5 s moves about 1.0 m in odometry and in reality.

## Checked
Method: docs-checked 2026-11-09 against the ros2_controllers diff_drive_controller userdoc.rst and diff_drive_controller_parameter.yaml (both read in full from raw GitHub, current master). Removed as unconfirmed: the older-release `use_stamped_vel` note, the kinematics formulas, the advice to disable other odom tf publishers or remap to Nav2, and the landing-page source control.ros.org.
