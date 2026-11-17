---
id: computing-software.robotics-software.robot-simulation-gazebo.sdf-fuel-includes
name: sdf-fuel-includes
category: computing-software
field: robotics-software
product: robot-simulation-gazebo
tags: [gz-fuel, fuel-models, include-uri, model-database, resource-path, nested-models]
level: practitioner
status: docs-checked
description: "Reuse models with include and Fuel URIs; how Gazebo resolves resource paths and plugin paths."
sources:
  - https://raw.githubusercontent.com/gazebosim/gz-sim/gz-sim9/tutorials/resources.md
  - https://raw.githubusercontent.com/gazebosim/sdformat/sdf14/sdf/1.11/world.sdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Includes, Fuel and resource paths
```xml
<include><uri>https://fuel.gazebosim.org/1.0/OpenRobotics/models/Sun</uri></include>
<include><uri>file:///path/to/model_dir</uri><name>r1</name><pose>1 0 0 0 0 0</pose></include>
```
`<include>` (SDF 1.11) takes a `uri` to a file or a model-database-style directory holding
exactly one model, light or actor, plus optional `name`, `static`, `pose` and
`placement_frame` overrides, and a `merge` attribute. The second line is illustrative.

## How Gazebo resolves entity URIs (Finding resources tutorial)
In order:
1. Paths on `GZ_SIM_RESOURCE_PATH` (if the path is a URI, the scheme is stripped).
2. Current running path or absolute path.
3. Gazebo Fuel: first the local cache (`$HOME/.gz/fuel`), then the web server.
`SDF_PATH` also works in some scenarios but is not recommended.

Models, lights and actors can also be created at runtime through the
`/world/<world_name>/create` service with an SDF string or a path/URL.

## Meshes
`<geometry><mesh><uri>` (and actor skin/animation filenames) are looked up first in the
current/absolute path, then on `GZ_SIM_RESOURCE_PATH`. A `name://` URI loads a mesh already
registered in the Mesh Manager.

## Plugins and GUI config paths
- System plugins: `GZ_SIM_SYSTEM_PLUGIN_PATH`, then `$HOME/.gz/sim/plugins`, then systems
  installed with Gazebo.
- GUI plugins: `GZ_GUI_PLUGIN_PATH` first, then those installed with Gazebo, and others.
- GUI config order: `--gui-config <file>`, then the world's `<gui>` plugins, then
  `$HOME/.gz/sim/<#>/gui.config`.

## ROS packages
`ros_gz_sim` can add model directories through `<gazebo_ros gazebo_model_path=...>` in
`package.xml` (see the ros-gz-launch-sim skill).

## Gotchas
- A stale Fuel cache is the first place a changed remote model is read from; the cache
  location is `$HOME/.gz/fuel`.

## Self-check
The included model appears in the running world with the overridden name and pose.

## Checked
Method: docs-checked 2026-11-09 against the gz-sim9 Finding resources tutorial and the sdformat 1.11 world.sdf (raw GitHub, read in full). Removed as unconfirmed: `model://` resolution with `name/model.sdf` and `model.config`, the export command using `ros2 pkg prefix`, relative/`model://` mesh paths inside models, `package://` handling, the `gz model --list` check, and the landing-page source gazebosim.org/docs.
