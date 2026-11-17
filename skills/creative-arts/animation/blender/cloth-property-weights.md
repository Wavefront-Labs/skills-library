---
id: creative-arts.animation.blender.cloth-property-weights
name: cloth-property-weights
category: creative-arts
field: animation
product: blender
tags: [blender, cloth, cloth-property-weights, stiffness-vertex-group, shrink-vertex-group, max-stiffness, variable-stiffness]
level: practitioner
status: docs-checked
description: "Vary Blender cloth stiffness across a garment with Property Weights: structural/shear/bending vertex groups with max values, plus shrink groups — collars, cuffs and stiff hems."
sources:
  - https://docs.blender.org/manual/en/latest/physics/cloth/settings/property_weights.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# cloth-property-weights

Goal: one cloth object with stiff and soft regions, such as a shirt with a crisp collar and cuffs.

## Setup (Physics > Cloth > Property Weights)

The panel constrains cloth properties from the Physical Properties and Shape panels to vertex groups.

- **Structural Group** with **Max Tension** and **Max Compression**.
- **Shear Group** with **Max Shearing**.
- **Bending Group** with **Max Bending**: the most useful for collars and cuffs.
- **Shrinking Group** with **Max Shrinking** (a negative value grows the cloth instead). This lives in Property Weights, not the Shape panel; the global *Shrinking Factor* is in Shape.
- Paint groups in Weight Paint with soft gradients to avoid creases at the boundary.

Each group limits where the matching property applies; judge how weights map to the base and Max values by testing on a small mesh.

## Recipes (starting points to tune)

- **Shirt**: Cotton-like base; a `stiff` group on collar, placket and cuffs as the Bending Group with a higher Max Bending.
- **Cape with a heavy hem**: use a stiffer hem group, pin at the shoulders, and raise the global Vertex Mass slightly; Vertex Mass is one value for the whole cloth.

## Gotchas

- A Max value lower than the base stiffness would soften the weighted area; test it visually.
- Vertex groups copied from another garment can carry over; check them before simulating.
- Changing groups invalidates the cache: Delete Bake and re-run.

## Verify

Simulate: weighted regions hold shape (collar stands, cuffs stay tubular) while the rest drapes.

## Checked

Date: 2026-10-27. Blender 5.2 manual (blender-v5.2-release branch). Confirmed: all Property Weights field names, and that the Shrinking Group belongs to Property Weights (the old text put it in the Shape panel). Removed the specific multipliers and the weight-interpolation detail that the manual does not state.
Method: documentation only; no commands were run.
