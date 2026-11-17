---
id: creative-arts.animation.blender.scene-gravity-settings
name: scene-gravity-settings
category: creative-arts
field: animation
product: blender
tags: [blender, scene-settings, gravity-settings, scene-gravity, physics, simulation-scale, rigid-body-world]
level: practitioner
status: verified
description: "Control global physics in Blender: Scene > Gravity vector, per-system Field Weights, rigid body world speed and substeps, and why object scale matters more than gravity tweaks."
sources:
  - https://docs.blender.org/manual/en/latest/physics/forces/gravity.html
  - https://docs.blender.org/manual/en/latest/physics/forces/force_fields/introduction.html
  - https://docs.blender.org/manual/en/latest/physics/rigid_body/world.html
  - https://docs.blender.org/manual/en/latest/physics/fluid/type/domain/settings.html
  - https://docs.blender.org/api/current/bpy.types.Scene.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# scene-gravity-settings

Goal: simulations that fall at believable speed in the intended direction.

## Scene Properties > Gravity

- The Gravity panel in Scene properties has a checkbox for global gravity (`Scene.use_gravity`, default on) and a vector (`Scene.gravity`, default `(0, 0, -9.81)`, in m/s^2). It applies to all physics systems in the scene.
- The manual gives Moon gravity as -1.622 and Mars as -3.69 on Z. Tilt the vector for sideways gravity, or set 0 for space shots.
- The Mantaflow fluid solver uses the scene gravity by default. Disabling global gravity in the scene settings enables the fluid domain's own gravity options.

## Per-system scaling

- **Field Weights** panels (cloth, particle system, fluid domain, rigid body world) include a **Gravity** weight that scales how much that system is affected by gravity, a weight per force-field type, and an **All** weight. The fluid domain also has an **Effector** field (`effector_group`) that restricts which force fields can influence it.
- **Rigid Body World** (Scene properties): **Speed** (`time_scale`, default 1.0; changes simulation speed without changing gravity), **Substeps Per Frame** (default 10), **Solver Iterations** (default 10). Higher substeps and iterations are more accurate but slower.

## Scale beats gravity

Practice: fall speed looks wrong mostly because the object is the wrong size, since the simulation works in scene units. Model at real size (check the dimensions in the N panel) before touching gravity. For miniatures shot to look big, slow the simulation with Rigid Body World Speed (or the fluid domain Time Scale) rather than reducing gravity.

## Gotchas

- Changing gravity does not update an existing bake: delete the bakes (Delete All Bakes, see `bake-all-dynamics`) and bake again. After editing force-field settings, the manual says to free the cache of particle, soft body or cloth systems because it is not done automatically.
- Force fields automatically affect everything; turn the weight down in a system's Field Weights panel to exclude it.

## Verify

Drop a 1 m cube so its underside starts 4.9 m above the floor: from d = g t^2 / 2 with g = 9.81 it lands in about 1 s (24 frames at 24 fps). Measured with a rigid body cube in Blender 4.5.14 (start at frame 1, underside 4.9 m up): the cube first reached the floor at frame 25 (centre height 0.541; rest height is about 0.5 plus collision margin).

## Checked

Date: 2026-10-27. Documentation release: Blender 5.2 manual (blender-v5.2-release RST) and current Python API docs.
Confirmed: Scene Gravity panel and default -9.81 on Z (manual and `Scene.gravity` default); `Scene.use_gravity` default True; Rigid Body World Speed/Substeps Per Frame/Solver Iterations and their defaults (`RigidBodyWorld` API); fluid domain uses scene gravity unless disabled; Field Weights Gravity, Effector Collection and All entries. Removed: the "0 to 1" weight range and 0.3 example, "Use Scene Gravity" checkbox name, particle Timestep/Subframes mention, "Time Stretching", Unit Scale and "Real World Size" claims (no doc coverage).
Run check, 2026-11-01, Blender 4.5.14 LTS headless: Scene.use_gravity (label Global Gravity) True and Scene.gravity (0, 0, -9.81) defaults, settable to -1.622; RigidBodyWorld time_scale (panel label Speed in the UI source) 1.0, substeps_per_frame 10, solver_iterations 10; EffectorWeights has gravity and all; cloth, rigid body world and fluid domain each have effector_weights; the fluid panel source shows Scene Gravity while scene gravity is on and an editable Gravity when it is off; the drop test above. Unrun (documentation only): Moon and Mars values from the manual, cache invalidation advice, particle-system Field Weights, the Speed-for-miniatures advice.

Method: manual text confirmed from documentation; properties and the drop test run headless in Blender 4.5.14.
