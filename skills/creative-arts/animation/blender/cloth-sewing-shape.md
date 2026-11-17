---
id: creative-arts.animation.blender.cloth-sewing-shape
name: cloth-sewing-shape
category: creative-arts
field: animation
product: blender
tags: [blender, cloth, cloth-sewing, sewing-springs, cloth-shape-settings, cloth-shrink, dynamic-mesh, garment-assembly]
level: practitioner
status: docs-checked
description: "Assemble garments from flat panels with Blender cloth sewing springs (loose edges, max sewing force) and use Shape settings: shrinking factor, dynamic mesh, rest shape key."
sources:
  - https://docs.blender.org/manual/en/latest/physics/cloth/settings/shape.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# cloth-sewing-shape

Goal: pattern-based garments inside Blender. Garment modelling overview: `cloth-garment-modeling`.

## Sewing

1. Model flat front and back panels around the body, outside it so the cloth does not start penetrating the collider. Connect matching seam vertices with extra edges that belong to no face (loose edges).
2. Physics > Cloth > **Shape > Sewing** on. **Max Sewing Force** caps the spring force; zero is unbounded, which the manual advises against in most cases because the initial frames, with the ends far apart, can produce extreme forces and instability.
3. With the body as a collider, play: sewing springs pull the panels together.
4. Apply the Cloth modifier at a good frame to freeze the shape (Apply removes the modifier), then merge seam vertices if needed and add a fresh cloth sim for animation.

## Shape settings

- **Shrinking Factor**: shrink the cloth; a negative value grows it. The **Shrinking Group** and **Max Shrinking** are in Property Weights (see `cloth-property-weights`).
- **Dynamic Mesh**: rest shape is recalculated every frame from shape keys or modifiers above Cloth (Armature or other deformers), so unpinned cloth can squash and stretch with a character while otherwise moving under the sim. Normally the first frame defines the rest shape for the whole sim.
- **Rest Shape Key**: start the sim from a chosen shape key instead of the evaluated shape (for example a pre-draped state). Mutually exclusive with Dynamic Mesh, and only shown when the mesh has shape keys.
- **Pin Group** and **Stiffness** are also in Shape (see `cloth-pinning`).

## Gotchas

- Sewing edges must be loose; faces between seams behave as fabric.
- A sewing spring is not a pin: cloth stays free to slide, as with a clasp on a cloak.

## Verify

After stitching, seams are closed and the garment rests on the body without penetration.

## Checked

Date: 2026-10-27. Blender 5.2 manual (blender-v5.2-release branch). Confirmed: Sewing, Max Sewing Force (zero unbounded, not recommended), Shrinking Factor sign, Dynamic Mesh, Rest Shape Key (exclusive with Dynamic Mesh, visible only with shape keys) and the Cloth modifier Apply behaviour. Removed the unsourced "4.x" version tag and the Merge/Bridge workflow specifics.
Method: documentation only; no commands were run.
