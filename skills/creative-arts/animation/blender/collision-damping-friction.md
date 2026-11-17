---
id: creative-arts.animation.blender.collision-damping-friction
name: collision-damping-friction
category: creative-arts
field: animation
product: blender
tags: [blender, collision, collision-damping, collision-friction, stickiness, permeability]
level: practitioner
status: docs-checked
description: "Tune Blender collision physics for particles, soft bodies and cloth: damping, randomize, friction, stickiness, permeability, kill particles and field absorption."
sources:
  - https://docs.blender.org/manual/en/latest/physics/collision.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# collision-damping-friction

## Collision panel (Physics > Collision), Particle section

- **Permeability**: fraction of particles passing through the mesh.
- **Stickiness**: how much particles stick to the object.
- **Kill Particles**: deletes particles on impact.
- **Damping**: damping during a collision, independent of particle velocity. **Randomize** adds random variation.
- **Friction**: friction during movement along the surface. **Randomize** likewise.

## Soft Body and Cloth section

- **Damping**: amount of bounce absorbed. 0.0 is no damping (maximum bounciness for soft bodies); 1.0 is maximum damping (no bounce).
- **Thickness** (Outer, Inner): see `collision-thickness`.
- **Friction**: how slippery the cloth is against the collider.
- **Single Sided**: the collider is treated as the boundary of a solid and ejects intersecting cloth along its normal.
- **Override Normals**: cloth collision impulses act along the collider normals.

## Field Absorption (Collision section)

Fraction of an effector's force the collider blocks; 100 percent lets none through. Several colliders in a row multiply: absorptions of 10, 43 and 3 percent leave about 50 percent absorbed overall.

## Gotchas

- Settings live on the collider, not on the particle, soft body or cloth system. Changing deflection settings does not recalculate existing sims: Delete Bake and re-run.
- Hair particles ignore deflecting objects; animate hair as soft bodies if it must collide.
- Soft body deflection is difficult and fast movers can penetrate.
- Rigid bodies use their own Friction and Bounciness (Physics > Rigid Body > Collisions), not this panel.
- The Collision modifier must come after shape keys and Armature on an animated collider.

## Verify

Rain particles with Kill Particles on vanish on contact; a soft body with Damping 1.0 does not bounce while 0.0 bounces maximally.

## Checked

Date: 2026-10-27. Blender 5.2 manual (blender-v5.2-release branch). Confirmed: all Particle and Soft Body and Cloth fields, the Damping 0.0 and 1.0 meanings, Field Absorption and its worked example, the hair and recalculation notes and the modifier-order note. Removed the unsupported 5-10 cloth friction recommendation and the Damping 0.5 half-height claim.
Method: documentation only; no commands were run.
