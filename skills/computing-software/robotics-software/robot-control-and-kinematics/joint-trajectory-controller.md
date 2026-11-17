---
id: computing-software.robotics-software.robot-control-and-kinematics.joint-trajectory-controller
name: joint-trajectory-controller
category: computing-software
field: robotics-software
product: robot-control-and-kinematics
tags: [joint-trajectory, jtc, follow-joint-trajectory, trajectory-msgs, goal-tolerance, jtc-constraints, control-controllers]
level: practitioner
status: docs-checked
description: "Configure and command joint_trajectory_controller via topic or FollowJointTrajectory action with tolerances."
sources:
  - https://raw.githubusercontent.com/ros-controls/ros2_controllers/master/joint_trajectory_controller/doc/userdoc.rst
  - https://raw.githubusercontent.com/ros-controls/ros2_controllers/master/joint_trajectory_controller/doc/trajectory.rst
  - https://raw.githubusercontent.com/ros-controls/ros2_controllers/master/joint_trajectory_controller/src/joint_trajectory_controller_parameters.yaml
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# joint_trajectory_controller
Executes joint-space trajectories on a group of joints, interpolating in time between
waypoints (positions, optionally velocities and accelerations). Even single-point
trajectories are accepted. The controller expects at least position feedback; it does not
integrate velocity or acceleration states itself, so hardware that only provides those
must integrate them in the hardware interface.

```yaml
controller_manager:
  ros__parameters:
    arm_controller:
      type: "joint_trajectory_controller/JointTrajectoryController"

arm_controller:
  ros__parameters:
    joints: [joint1, joint2]
    command_interfaces: [position]
    state_interfaces: [position, velocity]
    allow_partial_joints_goal: false
    constraints:
      stopped_velocity_tolerance: 0.01
      goal_time: 10.0
      joint1: {trajectory: 0.05, goal: 0.03}
```
Values are examples; defaults for the constraints are `stopped_velocity_tolerance` 0.01
and `goal_time` 10.0.

## Interfaces
- Action `<controller_name>/follow_joint_trajectory` (`control_msgs/action/FollowJointTrajectory`):
  the primary way to send trajectories, favoured when execution monitoring is wanted.
  Goals may carry path and goal tolerances; otherwise the parameter defaults are used.
- Topic `<controller_name>/joint_trajectory` (`trajectory_msgs/msg/JointTrajectory`):
  fire-and-forget; goal tolerances are not used, but if state tolerances are violated the
  trajectory is aborted and the position held.
- Publishes `<controller_name>/controller_state`; service `<controller_name>/query_state`
  returns the state at a future time.
- Both input paths need values for all controller joints unless
  `allow_partial_joints_goal` is true.

## Command and state interface rules
- Supported command interface combinations: position; position+velocity;
  position+velocity+acceleration; velocity; effort; position+effort.
- Position and acceleration commands are forwarded; velocity and effort commands come from
  a PID loop on the following error if gains are configured.
- With a velocity-only command interface, state interfaces must include position and
  velocity; effort, position+effort and acceleration command interfaces also need position
  and velocity states. A velocity state needs a position state.

## Interpolation
- `interpolation_method` is `splines` (default) or `none`.
- Spline strategy follows the waypoint content: position only gives linear
  interpolation (continuous position, discontinuous velocity; discouraged), position and
  velocity gives cubic, position, velocity and acceleration gives quintic.
- The documentation warns there is no sanity check: missing fields needed by your command
  interface and PID setup can crash the controller.

## Timing and replacement
- Header stamp zero means start now. A new trajectory is blended with the running one
  (`allow_trajectory_replacement`, default true); waypoints in the past are dropped, and
  if all waypoints are in the past the new trajectory is rejected and the current one
  continues.
- Only one action goal is active at a time; a new action goal preempts and aborts the
  old one. An empty trajectory sent on the topic overrides the action goal without
  aborting it.

## Gotchas
- If tolerances are violated during action execution the goal is aborted, the client is
  notified and the current position is held; widen the goal tolerance for slow drives.
- Per-joint tolerance of 0 in a goal message means unspecified (default used); -1 erases
  the tolerance.

## Self-check
The commanded point is reached within tolerance and the action returns success.

## Checked
Method: docs-checked 2026-11-09 against the ros2_controllers joint_trajectory_controller userdoc.rst, trajectory.rst and joint_trajectory_controller_parameters.yaml (all read in full from raw GitHub, current master). Removed as unconfirmed: the `ros2 topic pub` example, "late starts rejected as past" wording (replaced by the documented waypoint-dropping rule), "feedback on controller_state" wording, the MoveIt usage claim, and the landing-page source control.ros.org.
