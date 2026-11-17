---
id: computing-software.robotics-software.robot-simulation-gazebo.gz-physics-tuning
name: gz-physics-tuning
category: computing-software
field: robotics-software
product: robot-simulation-gazebo
tags: [gz-physics, max-step-size, real-time-factor, dart, bullet, contact-friction]
level: advanced
status: docs-checked
description: "Set Gazebo physics step size, real-time factor, engine choice and surface friction/contact parameters in SDF."
sources:
  - https://raw.githubusercontent.com/gazebosim/gz-sim/gz-sim9/tutorials/physics.md
  - https://raw.githubusercontent.com/gazebosim/sdformat/sdf14/sdf/1.11/physics.sdf
  - https://raw.githubusercontent.com/gazebosim/sdformat/sdf14/sdf/1.11/surface.sdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Physics tuning
World-level physics lives in the SDF `<physics>` element; per-collision behaviour lives in
`<surface>`.

```xml
<physics name="1ms" type="dart">
  <max_step_size>0.001</max_step_size>
  <real_time_factor>1.0</real_time_factor>
</physics>
```

## World physics (SDF 1.11 spec)
- `max_step_size`: maximum step at which every system can interact with the world state
  (default 0.001).
- `real_time_factor`: target ratio of simulation time to real time (default 1.0).
- `real_time_update_rate`: physics updates per real-time second (default 1000); the spec
  notes it is to be deprecated in favour of `real_time_factor`.
- `max_contacts`: maximum contacts between two entities (default 20); a collision's own
  `max_contacts` overrides it.
- `name` and `default` attributes: several physics profiles may exist; the first marked
  `default` is used, otherwise the first.
- `type` attribute is documented as ode, bullet, simbody or dart.

## Choosing an engine (Gazebo Sim physics tutorial)
- Default engine is DART. Bullet (`gz-physics-bullet-plugin`) and Bullet Featherstone
  (`gz-physics-bullet-featherstone-plugin`) have preliminary support.
- Select on the command line: `gz sim --physics-engine gz-physics-bullet-featherstone-plugin`
  (library name; `lib` prefix and extension optional), or in the world with the Physics
  system plugin:
```xml
<plugin filename="gz-sim-physics-system" name="gz::sim::systems::Physics">
  <engine><filename>CustomEngine</filename></engine>
</plugin>
```
- Custom engine libraries are found through `GZ_SIM_PHYSICS_ENGINE_PATH` (colon-separated
  on Linux, semicolon on Windows).
- DART options through SDF: `//physics/dart/collision_detector` (`ode` per the tutorial's
  default, also `bullet`, `fcl`, `dart`) and `//physics/dart/solver/solver_type`
  (`dantzig` default, `pgs`). Not every option is supported by every engine.

## Surface parameters (SDF 1.11 spec, per collision)
- Friction: `<surface><friction><ode><mu>` and `<mu2>` (default 1; unitless maximum ratio of
  friction force to normal force in the first and second friction directions), `fdir1`
  (direction in the collision frame), `slip1`/`slip2` (force-dependent slip, default 0).
  Bullet equivalents are `<bullet><friction>`, `friction2`, `rolling_friction`.
- Torsional friction: `<friction><torsional><coefficient>` (default 1.0) with `patch_radius`
  or `surface_radius`.
- Bounce: `restitution_coefficient` 0 to 1 (default 0) and `threshold` (default 100000;
  velocity below which restitution is 0).
- Contact: `<contact><ode>` has `soft_cfm`, `soft_erp`, `kp`, `kd`, `max_vel`, `min_depth`;
  `collide_bitmask`, `category_bitmask` and `collide_without_contact` filter collisions.
- ODE and Bullet engine blocks (`cfm`, `erp`, `contact_surface_layer`, `iters`, `sor`) are in
  the spec but the Gazebo Sim tutorial documents DART only; check engine support before
  relying on them.

## Gotchas
- A smaller `max_step_size` costs CPU; the spec gives no recommended range.
- Friction and contact behaviour can differ between engines; recheck after switching.

## Self-check
Changing `max_step_size` or the engine in the world file visibly changes the simulation step
reported by the running world.

## Checked
Method: docs-checked 2026-11-09 against gz-sim9 tutorials/physics.md and the sdformat 1.11 physics.sdf and surface.sdf (raw GitHub, read in full). Removed as unconfirmed: "typical 0.001 to 0.004 s", RTF 0 meaning unbounded, `gz topic -e -t /stats`, TPE engine and kinematic-only claim, the `gz-physics-bullet-plugin` plugin-tag form, the "wheel slip is friction or inertia" and "exploding models" causal claims, odometry-within-few-percent check, and the landing-page source gazebosim.org/docs.
