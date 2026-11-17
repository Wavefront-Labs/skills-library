---
id: computing-software.robotics-software.robot-simulation-gazebo.gz-system-plugins
name: gz-system-plugins
category: computing-software
field: robotics-software
product: robot-simulation-gazebo
tags: [gz-plugins, system-plugin, gz-systems, buoyancy, hydrodynamics]
level: practitioner
status: docs-checked
description: "Load and write Gazebo system plugins: SDF attachment, search paths, update interfaces, buoyancy example."
sources:
  - https://raw.githubusercontent.com/gazebosim/gz-sim/gz-sim9/tutorials/createsystemplugins.md
  - https://raw.githubusercontent.com/gazebosim/gz-sim/gz-sim9/tutorials/resources.md
  - https://raw.githubusercontent.com/gazebosim/gz-sim/gz-sim9/tutorials/adding_system_plugins.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Gazebo system plugins
All systems are loaded as plugins at runtime. Each system is attached to a world, model,
sensor or actor entity. `filename` is the shared library and `name` the class.

```xml
<plugin filename="gz-sim-trajectory-follower-system" name="gz::sim::systems::TrajectoryFollower">
  <link_name>base_link</link_name><force>0.2</force><torque>0.01</torque>
  <range_tolerance>0.1</range_tolerance>
  <waypoints><waypoint>1 0</waypoint></waypoints>
</plugin>
```
Place `<plugin>` under `<world>`, `<model>` or `<sensor>`. The same tutorial loads
`gz-sim-hydrodynamics-system` (`gz::sim::systems::Hydrodynamics`) with `link_name` and
damping coefficients, and a buoyancy plugin, for a floating vehicle; a maritime model needs
at least buoyancy and hydrodynamics. A model that is not `<static>` falls under gravity
without support.

## Where Gazebo finds system plugins
In order: `GZ_SIM_SYSTEM_PLUGIN_PATH`, `$HOME/.gz/sim/plugins`, systems installed with
Gazebo. Systems can also be passed via `ServerConfig::PluginInfo`. Gazebo ships a `diff_drive`
plugin implementing a differential drive controller.

## Writing a system (create-system-plugins tutorial)
Inherit from `System` plus the interfaces you need:
- `ISystemConfigure`: once at load, read-write; read SDF config, register events.
- `ISystemPreUpdate`: read-write; state changes before physics, such as applying control.
- `ISystemUpdate`: read-write; the physics step, rarely needed by non-physics systems.
- `ISystemPostUpdate`: read-only; read results (sensors, rendering, controller feedback).
- `ISystemReset`: once at reset, read-write.
Controllers use PostUpdate to read state and PreUpdate to act on the next frame.
`UpdateInfo::simTime` is the time reached after PreUpdate and Update, so it is 0 when
started paused. Build a shared library linked to `gz-plugin<N>` (`COMPONENTS register`) and
`gz-sim9`, register it, and load it in the world with `filename` set to the library name.

## Self-check
The plugin class named in `name` loads (no "Failed to load plugin" message) and its effect
shows in the running world.

## Checked
Method: docs-checked 2026-11-09 against the gz-sim9 create-system-plugins, finding-resources and adding-system-plugins tutorials (raw GitHub, read in full). Removed as unconfirmed: the DiffDrive, JointController, JointStatePublisher and OdometryPublisher parameter lists, plugin filenames other than the ones above, Fortress `ignition-gazebo-*` names, wheel-radius odometry gotcha, topic scoping rule, the `gz topic` Twist self-check, and the landing-page source gazebosim.org/docs.
