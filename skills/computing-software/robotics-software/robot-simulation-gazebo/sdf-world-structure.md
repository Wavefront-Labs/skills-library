---
id: computing-software.robotics-software.robot-simulation-gazebo.sdf-world-structure
name: sdf-world-structure
category: computing-software
field: robotics-software
product: robot-simulation-gazebo
tags: [sdf-world, sdformat, world-sdf, light, ground-plane, scene-broadcaster, gz-worlds]
level: practitioner
status: docs-checked
description: "Author an SDF world file: world element contents, system plugins, server-config defaults and includes."
sources:
  - https://raw.githubusercontent.com/gazebosim/sdformat/sdf14/sdf/1.11/world.sdf
  - https://raw.githubusercontent.com/gazebosim/gz-sim/gz-sim9/tutorials/server_config.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# SDF world
A world is a `<world name="...">` inside `<sdf version="...">`; the name must be unique
(default `__default__`).

```xml
<sdf version="1.6">
  <world name="fuel_preview">
    <plugin filename="gz-sim-scene-broadcaster-system"
            name="gz::sim::systems::SceneBroadcaster"/>
    <include><uri>https://fuel.gazebosim.org/1.0/OpenRobotics/models/Sun</uri></include>
  </world>
</sdf>
```
(Adapted from the Gazebo server-config tutorial, which uses `sdf version="1.6"`.)

## What a world can contain (SDF 1.11 spec)
- Required: `gravity` (default 0 0 -9.8 m/s^2), `magnetic_field`, `atmosphere`, `scene`, and
  at least one `physics`.
- Optional or repeatable: `audio`, `wind` (`linear_velocity`), `gui`, `light`, `frame`,
  `joint`, `model`, `actor`, `plugin`, `road`, `spherical_coordinates`, `state`,
  `population`, `include`.
- `<include>` takes a `uri` (a directory following the model database structure, or a
  file) that holds a single model, light or actor; optional `name`, `static` and `pose`
  overrides, a `placement_frame`, and a `merge` attribute. URIs can be Fuel URLs.

## System plugins and defaults (server-config tutorial)
- Systems are loaded as `<plugin filename=... name=...>` entries; the Physics system uses
  `gz-sim-physics-system` / `gz::sim::systems::Physics`, the scene broadcaster
  `gz-sim-scene-broadcaster-system` / `gz::sim::systems::SceneBroadcaster`.
- The server loads default plugins from `server.config` (including Physics and
  UserCommands). A plugin already in the SDF is not loaded twice.
- To use only the plugins in the file, set
  `<gz:policies><include_server_config_plugins>false</include_server_config_plugins></gz:policies>`
  in the world. In the tutorial's example, with only SceneBroadcaster loaded, a cone does not
  fall under gravity even when running with `-r`.
- `$HOME/.gz/sim/<#>/server.config` holds the defaults; deleting it regenerates it.

## Gotchas
- A world with the server defaults disabled and no Physics plugin does not simulate
  dynamics.
- Check the `sdf version` your Gazebo release supports.

## Self-check
`gz sim -r world.sdf` loads the world; adding the policy above changes which systems run.

## Checked
Method: docs-checked 2026-11-09 against the sdformat 1.11 world.sdf and the gz-sim9 server_config.md tutorial (raw GitHub, read in relevant parts). Removed as unconfirmed: the ground-plane and directional-light snippet, "SDF 1.9 for Harmonic", the pose convention line, "UserCommands blocks GUI spawning", `/world/<name>/...` topic naming, the `gz sdf -k` check, and the landing-page source gazebosim.org/docs.
