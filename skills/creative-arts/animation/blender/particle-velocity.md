---
id: creative-arts.animation.blender.particle-velocity
name: particle-velocity
category: creative-arts
field: animation
product: blender
tags: [blender, particles, particle-velocity, normal-velocity, tangent-velocity, object-velocity]
level: practitioner
status: docs-checked
description: "Set Blender particle initial velocity: Normal, Tangent, Tangent Phase, Object Align X/Y/Z, Object Velocity and Randomize, plus the related Rotation panel options."
sources:
  - https://docs.blender.org/manual/en/5.2/physics/particles/emitter/velocity.html
  - https://docs.blender.org/manual/en/5.2/physics/particles/emitter/rotation.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# particle-velocity

## Velocity panel (Particle System > Velocity)

For Emitter and Hair particle systems these give the particles an initial velocity:

- **Normal**: the emitter surface normals give the starting speed.
- **Tangent**: the tangent speed gives the starting speed. **Tangent Phase** rotates the surface tangent.
- **Object Align** X, Y, Z: an initial velocity along the X, Y and Z axes.
- **Object Velocity**: the movement of the emitter object gives the starting speed.
- **Randomize**: random variation of the starting speed (a texture can limit where it applies).

## Rotation panel (related)

- **Orientation Axis** aligns the X axis of new particles to: None (global X), Normal, Normal-Tangent, Velocity / Hair, Global X/Y/Z, or Object X/Y/Z.
- **Randomize** (initial rotation on all axes), **Phase** (-1 to 1 = -180 to 180 degrees around X), **Randomize Phase** (0 to 2 = 0 to 360 degrees), **Dynamic** (whether rotation can change over time).
- **Angular Velocity** (needs Dynamic): Axis None, Velocity, Horizontal, Vertical, Global X/Y/Z or Random, with an Amount for spin speed.
- To make particles point along a Curve Guide, set Orientation Axis to Velocity / Hair, enable Dynamic, and set the Angular Velocity Axis to Velocity.
- Set Viewport Display > Display As to Axis to see particle orientation.

## Verify

For a fountain launched upward at v under gravity g, the apex height is h = v^2 / (2g); with v = 6 and g = 9.81 that is about 1.8 m (assuming Newtonian physics with default gravity and no drag).

## Checked

Date: 2026-10-27. Documentation: Blender 5.2 manual (Particle Velocity and Rotation pages); the apex height was computed from the standard formula. Confirmed: all velocity and rotation options, ranges for Phase and Randomize Phase, the Curve Guide orientation recipe. Corrected: the names are Tangent Phase and Object Align (not "Rotation" and "Object Aligned"). Removed as unconfirmed: recipe numbers, "Physics None does nothing", units and Object Velocity gotchas.
Method: documentation only; no commands were run.
