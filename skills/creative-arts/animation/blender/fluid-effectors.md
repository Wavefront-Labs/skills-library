---
id: creative-arts.animation.blender.fluid-effectors
name: fluid-effectors
category: creative-arts
field: animation
product: blender
tags: [blender, fluid, mantaflow, fluid-effectors, effector, fluid-guide, obstacle]
level: practitioner
status: docs-checked
description: "Use Mantaflow effector objects as colliders and guides: is planar, surface thickness, use effector toggle, guide velocity and guide modes."
sources:
  - https://docs.blender.org/manual/en/latest/physics/fluid/type/effector.html
  - https://docs.blender.org/manual/en/latest/physics/fluid/type/domain/guides.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# fluid-effectors

## Collision effectors

- Physics > Fluid > Type **Effector**, Effector Type **Collision**: the object collides with the fluid.
- **Is Planar**: for a single-dimension object such as a plane, or a non-manifold mesh.
- **Surface Thickness**: additional area around the effector that counts as effector.
- **Use Effector**: enables or disables the effector; keyframe it to switch collision on and off.
- **Sampling Substeps**: reduces gaps in collision with fast-moving effectors.

## Guide effectors

- Effector Type **Guide**: the velocity of the object is used when baking the guiding, so guide objects must move.
- **Guide Mode** (how velocities are written to the domain's guiding field): Maximize, Minimize, Override, Averaged.
- **Velocity Factor** multiplies the guiding velocities (useful with several guides).
- Domain > **Guides** panel: enabling guides switches to the more accurate but more expensive pressure solve, so only enable it when you use guiding. Settings: Weight (lag of the guiding), Size (size of the vortices), Velocity Factor, Velocity Source (Effector, or another baked Domain which may have a different resolution or type), Guide Parent. Bake Guides is available with the Modular cache and the Effector source; once effectors are baked the domain resolution cannot change.

## Force fields

Force fields such as wind or vortex act on fluids; per-type influence is set in the domain's Field Weights panel.

## Gotchas

- Fluid leaking through a thin container wall: try a larger Surface Thickness, Sampling Substeps for fast colliders, or a higher resolution.
- A guide object that does not move contributes no guiding velocity.

## Verify

Bake with the container at final resolution and look at the domain in the viewport: no fluid outside the walls.

## Checked

Checked 2026-10-27 against the Blender 5.2 manual (physics/fluid/type/effector and physics/fluid/type/domain/guides; branch blender-v5.2-release) and the 5.2 source (rna_fluid.cc). Confirmed: Effector Type Collision and Guide, Is Planar, Surface Thickness, Use Effector, Sampling Substeps, Guide Mode options, Velocity Factor, and every Guides panel setting including Velocity Source, Guide Parent and Bake Guides conditions.

Method: documentation only; no commands were run.
