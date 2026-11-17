---
id: computing-software.robotics-software.robot-control-and-kinematics.controller-manager-cli
name: controller-manager-cli
category: computing-software
field: robotics-software
product: robot-control-and-kinematics
tags: [controller-manager, ros2-control-cli, spawner, list-controllers, switch-controllers, joint-state-broadcaster, control-framework]
level: practitioner
status: docs-checked
description: "Operate ros2_control with the controller manager, spawner and ros2 control CLI."
sources:
  - https://github.com/ros-controls/ros2_control/blob/master/ros2controlcli/doc/userdoc.rst
  - https://github.com/ros-controls/ros2_control/blob/master/controller_manager/doc/userdoc.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Controller manager
**Goal:** load, start and stop controllers safely.

```yaml
controller_manager:
  ros__parameters:
    joint_state_broadcaster: {type: joint_state_broadcaster/JointStateBroadcaster}
    arm_controller: {type: joint_trajectory_controller/JointTrajectoryController}
```
```bash
ros2 run controller_manager spawner joint_state_broadcaster arm_controller --controller-manager /controller_manager
ros2 control list_controllers
ros2 control list_hardware_interfaces       # available command and state interfaces, with claimed status
ros2 control list_hardware_components
ros2 control set_controller_state arm_controller inactive      # or: switch_controllers --deactivate
```
- The controller manager can be launched with the `ros2_control_node` executable; controllers are declared in its parameters as `<controller_name>.type`.
- `set_controller_state` accepts unconfigured, inactive or active; `spawner` loads, configures and starts a controller, `unspawner` stops and unloads it.

## Gotchas
- Point `spawner` and the `ros2 control` verbs at the right manager with `-c`/`--controller-manager` when it is not the default.

## Self-check
`list_controllers` shows `joint_state_broadcaster` and your controller `active`.

## Checked
2026-11-03. Confirmed in the ros2_control repo docs (ros2controlcli userdoc: `list_controllers`, `list_hardware_components`, `list_hardware_interfaces`, `set_controller_state` with unconfigured/inactive/active, `switch_controllers --activate/--deactivate`, `-c`; controller_manager userdoc: `spawner`, `unspawner`, `ros2_control_node`, `<controller_name>.type`). Removed: `update_rate` value and loop description, single-claim rule, broadcaster `/joint_states` claim, plugin-type gotcha, Gazebo plugin mention (not in pages read), "older" qualifier.
Method: documentation only; no commands were run.
