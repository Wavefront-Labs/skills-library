---
id: computing-software.robotics-software.moveit-manipulation.time-parameterization
name: time-parameterization
category: computing-software
field: robotics-software
product: moveit-manipulation
tags: [time-parameterization, totg, ruckig, iterative-parabolic, velocity-scaling, jerk-smoothing]
level: advanced
status: docs-checked
description: "Time-parameterize paths with TOTG or Ruckig smoothing and apply velocity and acceleration scaling."
sources:
  - https://moveit.picknik.ai/main/index.html
  - https://github.com/moveit/moveit2
  - https://github.com/moveit/moveit2_tutorials
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Time parameterization
- Planners output paths; adapters add timing. Common ones: `AddTimeOptimalParameterization` (TOTG) and `AddRuckigTrajectorySmoothing` (jerk-limited, uses `max_jerk` from the joint limits).
- Scaling: per request or via `setMaxVelocityScalingFactor`/`setMaxAccelerationScalingFactor` (0 to 1); default factors come from `joint_limits.yaml`.
- Standalone: `trajectory_processing::TimeOptimalTrajectoryGeneration().computeTimeStamps(robot_traj, vel_scale, acc_scale)`.
- Check the result for monotonic time stamps and endpoint velocities near zero.
- Final execution speed also depends on the controller's tolerances and interpolation (spline vs linear).

## Gotchas
- Missing acceleration limits make TOTG fail.
- Aggressive scaling can exceed the real drive limits even when MoveIt accepts it.

## Self-check
Halving the velocity scaling roughly doubles trajectory duration.

## Checked
2026-11-03: parameter, plugin, API and command names compared with the MoveIt 2 sources (moveit2 repository headers, servo_parameters.yaml, servo_node.cpp, datatypes.hpp, moveit_py bindings; moveit2_tutorials pages for controller configuration, OMPL, Pilz, setup assistant and Bullet). Removed or corrected: `AddIterativeParabolicTimeParameterization` (no longer in the source) and the default-adapter claim.

Method: documentation only; no commands were run.
