---
id: computing-software.robotics-software.ros2-core.rep103-rep105-frames
name: rep103-rep105-frames
category: computing-software
field: robotics-software
product: ros2-core
tags: [rep-103, rep-105, units, coordinate-frames, enu-ned, base-link-odom-map, ros2-conventions-reps]
level: practitioner
status: docs-checked
description: "Apply REP 103 units and axis conventions and REP 105 frames (map, odom, base_link)."
sources:
  - https://www.ros.org/reps/rep-0103.html
  - https://www.ros.org/reps/rep-0105.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# REP 103 and REP 105
- REP 103: SI units; body frame x forward, y left, z up; for short-range geographic positions use ENU (X east, Y north, Z up). Euler angles are fixed-axis roll, pitch, yaw about X, Y, Z.
- Camera frames with an `_optical` suffix use a different convention (z forward); a NED convention should use a secondary frame with a `_ned` suffix.
- REP 105 frame tree: `map -> odom -> base_link`. `odom` is continuous (no discrete jumps) but drifts without bound, and is typically computed from an odometry source; `map` is not continuous and a localization component re-computes `map -> odom` to correct drift.

## Gotchas
- Mixing NED and ENU conventions without a transformed secondary frame gives wrong orientation.
- Degrees where code expects radians (REP 103 standardises on SI units).

## Self-check
Robot drives forward and `odom` x increases while RViz arrow points the same way.

## Checked
2026-11-03. Confirmed in REP 103 (SI units, x forward / y left / z up, ENU, `_optical` suffix, `_ned` suffix, fixed-axis roll-pitch-yaw) and REP 105 (map -> odom -> base_link, odom continuous and drifting, map not continuous, localization recomputes the transform). Removed: base_footprint, two-publisher and IMU-yaw claims, quaternion-in-messages and optical axis details (not read in the REP text).
Method: documentation only; no commands were run.
