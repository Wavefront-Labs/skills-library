---
id: creative-arts.animation.blender.fluid-domain-resolution
name: fluid-domain-resolution
category: creative-arts
field: animation
product: blender
tags: [blender, fluid, mantaflow, fluid-domain-resolution, resolution-divisions, cfl, time-scale]
level: practitioner
status: verified
description: "Size a Blender Mantaflow domain: resolution divisions, voxel size vs scale, time scale, CFL number and adaptive timesteps for stable sims."
sources:
  - https://docs.blender.org/manual/en/latest/physics/fluid/type/domain/settings.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# fluid-domain-resolution

## Resolution Divisions

- **Resolution Divisions** (`resolution_max`, default 32 in 4.5.14): number of voxels along the domain's longest side of its bounding box. Voxel size = longest side / divisions. A 4 m domain at 128 = 3.1 cm voxels.
- Larger domains need more divisions for the same detail: a 1 m cube at 64 divisions matches a 2 m cube at 128.
- Keep the domain just large enough for the simulation: large domains need higher resolutions and longer bakes. Shrinking the box is cheaper than raising divisions.
- The Domain panel can preview voxel size as a small cube in the 3D Viewport.

## Time

- **Time Scale** (`time_scale`, default 1, range 0.0001 to 10): low values give slow motion, higher values advance the sim faster.
- **Adaptive Time Steps** (`use_adaptive_timesteps`, on by default; Timesteps Minimum 1 and Maximum 4 by default): the solver decides when to run several steps per frame, using the Timesteps Minimum/Maximum, the frame rate and the Time Scale.
- **CFL Number** (`cfl_condition`, default 2, range 0 to 10): the maximum velocity per grid cell, in cells per time step. Fluid may move at most this far in one step, otherwise the solver subdivides the step. Larger CFL = fewer steps and less accuracy for fast flow; smaller CFL = more steps, longer sims, better accuracy at high velocities.
- When lowering CFL raise **Timesteps Maximum**; when raising CFL adjust **Timesteps Minimum**.

## Domain shape and gravity

- Translation, rotation and scaling of the domain are allowed; a non-box mesh still uses its bounding box as the domain.
- Fluids cannot leave the domain: they collide with the edge or disappear depending on **Border Collisions** (which sides deflect and which let fluid pass).
- Gravity: the solver uses scene gravity by default; disabling global gravity in the scene settings enables the fluid's own gravity fields.
- **Delete in Obstacle** removes fluid volume that intersects an obstacle.
- The Domain Type (Liquid or Gas) cannot be changed dynamically.

## Verify

Bake a short range at two Resolution Divisions values: the overall motion should agree while the finer one shows more detail.

## Checked

Checked 2026-10-27 against the Blender 5.2 manual (physics/fluid/type/domain/settings; branch blender-v5.2-release) and the 5.2 source (rna_fluid.cc). Confirmed: Resolution Divisions definition and worked example, Time Scale, Adaptive Time Steps, CFL Number and its trade-off, Timesteps Minimum/Maximum advice, bounding-box rule, Border Collisions, Gravity and Delete in Obstacle behaviour.

Run check, 2026-11-01, Blender 4.5.14 LTS headless (bpy, factory settings): FluidDomainSettings resolution_max 32 (UI label Resolution Divisions in the shipped properties_physics_fluid.py), time_scale 1, use_adaptive_timesteps True, cfl_condition 2, timesteps_min 1, timesteps_max 4, delete_in_obstacle (UI label Delete in Obstacle), gravity default (0, 0, -9.81), domain_type items GAS and LIQUID with GAS the default, six use_collision_border_* flags. Not run (confirmed from the manual only): the voxel-size arithmetic, the CFL trade-off, the Border Collisions meaning and the gravity override behaviour.

Method: manual text and shipped UI scripts confirmed from documentation; the listed behaviour run headless in Blender 4.5.14.
