---
id: creative-arts.animation.blender.rigid-body-world
name: rigid-body-world
category: creative-arts
field: animation
product: blender
tags: [blender, rigid-body, rigid-body-world, substeps, solver-iterations, rigid-body-cache, time-scale, split-impulse]
level: practitioner
status: verified
description: "Tune Blender's Rigid Body World: collection, Substeps Per Frame, Solver Iterations, Split Impulse, speed (time scale), cache frame range and why sims explode or jitter."
sources:
  - https://docs.blender.org/manual/en/latest/physics/rigid_body/world.html
  - https://docs.blender.org/manual/en/latest/physics/rigid_body/tips.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# rigid-body-world

## Settings (Scene Properties > Rigid Body World)

- **Collection**: holds the rigid body objects (default name "RigidBodyWorld"); **Constraints**: holds constraint objects. Bodies and constraints only count if they are in these collections. You can create several worlds' collections and assign objects to them.
- **Speed** (`time_scale`, default 1, range 0 to 100): speeds up or slows down the simulation.
- **Split Impulse**: reduces extra velocity that builds up when objects collide and limits the force separating them on collision; generally gives nicer results but lowers stability (especially when stacking many objects), so use it only when necessary.
- **Substeps Per Frame** (`substeps_per_frame`, default 10): simulation steps per frame; higher is more accurate but slower.
- **Solver Iterations** (`solver_iterations`, default 10): constraint solver iterations per step; higher is more accurate but slower, and makes constraints and stacking more stable.
- **Cache** (subpanel): **Start / End** frames; **Bake**, **Delete Bake**, **Calculate to Frame**, **Current Cache to Bake**, **Bake All Dynamics**, **Delete All Bakes**, **Update All to Frame**.
- **Field Weights**: external force effectors also influence rigid bodies.

## Troubleshooting (from the manual's tips)

- Simplest stability improvement: more steps per second. Too many steps can make it less stable (if you need more than 1000, look at other fixes).
- More Solver Iterations help constraints and stacking.
- Small or fast objects pass through each other: avoid Mesh shapes and raise the collision margin.
- Avoid small objects; ideally at least 20 cm in diameter.
- Enabling a constraint between badly aligned objects mid-sim can launch them.

## Gotchas

- Save the file before baking; an unsaved file keeps the cache in memory.
- You need to be in Object Mode to bake.

## Verify

Stacks rest still, fast projectile collisions register, and the bake completes without explosion.

## Checked

Date: 2026-10-27. Blender 5.2 manual (blender-v5.2-release branch). Confirmed: Rigid Body World settings and cache buttons, Collection and Constraints behaviour, and the Tips page stability advice. Corrected Split Impulse: it reduces bounce but lowers stability, so it is not a fix for jittering stacks. Removed default and recommended values for Substeps and Iterations, the gravity location claim, and the unconfirmed claim that linked scenes do not share caches.
Run check, 2026-11-01, Blender 4.5.14 LTS headless (bpy, factory settings): RigidBodyWorld properties collection, constraints, enabled, time_scale 1, substeps_per_frame 10, solver_iterations 10, use_split_impulse False, point_cache (frame_start, frame_end), effector_weights; the Scene panel label for time_scale is Speed and the cache buttons are Calculate to Frame, Current Cache to Bake, Bake All Dynamics, Delete All Bakes and Update All to Frame (shipped properties_scene.py and properties_physics_common.py); rigidbody operators world_add, object_add, constraint_add, connect, bake_to_keyframes exist. Not run (confirmed from the manual only): the Split Impulse trade-off, the stability tips and the save-before-baking and Object Mode notes.

Method: manual text and shipped UI scripts confirmed from documentation; the listed behaviour run headless in Blender 4.5.14.
