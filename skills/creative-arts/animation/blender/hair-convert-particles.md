---
id: creative-arts.animation.blender.hair-convert-particles
name: hair-convert-particles
category: creative-arts
field: animation
product: blender
tags: [blender, hair, hair-curves, hair-convert-particles, convert-hair, particle-hair]
level: practitioner
status: docs-checked
description: "Convert Blender particle hair to a Curves object and Curves back to a hair particle system, with the menu locations and the surface and UV requirements."
sources:
  - https://docs.blender.org/manual/en/latest/sculpt_paint/curves_sculpting/introduction.html
  - https://docs.blender.org/api/current/bpy.ops.curves.html
  - https://docs.blender.org/api/current/bpy.ops.object.html
  - https://docs.blender.org/manual/en/latest/physics/particles/hair/introduction.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# hair-convert-particles

## Particle hair to Curves
Select the mesh object, open the Particle properties tab and use the particle specials menu (dropdown beside the particle system list) > **Convert to Curves** (operator curves.convert_from_particle_system: adds a new Curves object based on the current state of the particle system; shown for hair type systems). Then check the Curves Data > **Surface** panel: Surface object and UV Map.

## Curves to particle system
- Curves menu in Curves Sculpt mode > **Convert to Particle System**, or Object > Convert > **Particle System** with a Curves object active (operator curves.convert_to_particle_system: adds or updates a hair particle system on the surface object).
- The manual says it exists for backwards compatibility with the older hair particle system, which is the only place Hair Dynamics lives.

## Generic conversion
Object > Convert > Curves (object.convert target Curves) creates Curves from evaluated curve data; it is a different operator from the particle conversion.

## Gotchas
- Conversion needs the Curves object to have a surface mesh and UV map set (Curves Data > Surface) for brushes and for the Deform Curves on Surface node.
- Settings that exist only on the particle side (such as Hair Dynamics) are not Curves settings; set them up on the particle system after converting.
- Curves Sculpt tools only use the original surface mesh, not its modifiers.

## Verify
Overlay the new object over the source: strands coincide.

## Checked

2026-10-27, Blender 5.2 manual (projects.blender.org blender-manual, branch blender-v5.2-release RST) and Python API docs. Confirmed operator behaviour in the Python API and menu entries in the 5.2 UI scripts (particle specials menu Convert to Curves; Curves menu and Object > Convert Particle System). Removed claims that children become real curves, what settings carry over, the Alembic note and the display-amount advice; none are documented. The old Convert > Curves instruction for particles was wrong: that operator is for evaluated curve data.
Method: documentation only; no commands were run.
