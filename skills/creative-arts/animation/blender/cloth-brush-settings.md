---
id: creative-arts.animation.blender.cloth-brush-settings
name: cloth-brush-settings
category: creative-arts
field: animation
product: blender
tags: [blender, sculpting, cloth-brush-settings, simulation-area, cloth-deformation-type, sculpt-cloth-collisions, cloth-pin-boundary, cloth-brush]
level: practitioner
status: docs-checked
description: "Sculpt folds with Blender's Cloth brush and Cloth Filter: deformation types, simulation area, mass and damping, collisions, pinned simulation boundary and face set limits."
sources:
  - https://docs.blender.org/manual/en/latest/sculpt_paint/sculpting/brushes/cloth.html
  - https://docs.blender.org/manual/en/latest/sculpt_paint/sculpting/tools/cloth_filter.html
  - https://docs.blender.org/manual/en/latest/sculpt_paint/sculpting/introduction/cloth_sculpting.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# cloth-brush-settings

Goal: believable fabric folds and wrinkles on garments directly in sculpt mode. Overview with pose and boundary brushes is in `creative-arts.animation.blender.sculpt-cloth-pose-brushes`.

## Where

Cloth is a brush type (Sidebar > Tool > Brush Settings > Advanced > Brush Type). It runs a simplified cloth simulation under the brush cursor. A small brush size makes the calculation much faster; large sizes may be too slow to use.

## Deformation type

*Drag* (pull the cloth toward the cursor), *Push*, *Pinch Point* (pull into a point), *Pinch Perpendicular* (pull into a line), *Inflate* (air under the cloth), *Grab* (pick up and move), *Expand* (stretch out), *Snake Hook* (moves cloth without surface artifacts and gives the most natural folds of the modes).

## Simulation area and forces

- **Simulation Area**: *Local* simulates only an area around the brush limited by a fixed radius; *Global* simulates the whole mesh (can be slow); *Dynamic* moves the active area with the brush, still limited by a fixed radius.
- **Simulation Limit**: factor relative to the brush radius that limits the simulation. **Simulation Falloff**: a factor of the limit, drawn as a dashed circle, over which the effect fades.
- **Pin Simulation Boundary**: locks vertices in the falloff area to avoid artifacts and soften the transition to unaffected areas.
- **Force Falloff**: Radial (sphere) or Plane. **Cloth Mass** (mass per simulation particle). **Cloth Damping** (how much applied force propagates through the cloth). **Soft Body Plasticity** (how much the cloth keeps its original shape, like a soft body).
- **Persistent** stops deformation accumulating after each stroke so you can keep simulating from the same base; **Set Persistent Base** resets the base.
- **Use Collisions**: the colliding object needs Collision physics enabled.

## Related tools

- Masked vertices are pinned in the simulation, face set boundaries can be auto-masked, and the Sculpt gravity factor also applies.
- **Cloth Filter** (Toolbar) simulates all vertices at once: drag away from the object for a positive effect. Types: Gravity, Inflate, Expand, Pinch, Scale. It has Strength, Force Axis, Orientation (Local, World, View), Cloth Mass, Cloth Damping, **Use Face Sets** (only the face set under the mouse) and Use Collisions.
- Pose and Boundary brushes can also run cloth sculpting by changing Deformation Target to Cloth Simulation.

## Gotchas

- Topology resolution drives fold size and detail; use even, well-distributed topology. Cloth is best for base meshes and larger folds; high-resolution detailing is slower.
- Collisions only happen with objects that have Collision physics.

## Verify

Strokes form folds without jagged spikes and the garment stays outside the body (check from the side with X-ray).

## Checked

2026-10-27, Blender 5.2 manual (blender-v5.2-release branch). Confirmed against sculpt_paint/sculpting/brushes/cloth, tools/cloth_filter and introduction/cloth_sculpting: deformation types, simulation area modes, Simulation Limit/Falloff, Pin Simulation Boundary, Force Falloff, mass, damping (damping is about force propagation, not stiffness), plasticity, Persistent, collisions requirement, Cloth Filter types and options, Deformation Target. Removed unconfirmed claims about Ctrl inversion, flipped normals, self-collision and a Simulate by Face Sets brush option.
Method: documentation only; no commands were run.
