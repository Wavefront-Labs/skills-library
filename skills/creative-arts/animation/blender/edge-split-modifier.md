---
id: creative-arts.animation.blender.edge-split-modifier
name: edge-split-modifier
category: creative-arts
field: animation
product: blender
tags: [blender, edge-split, modifiers, shading, sharp-edges, smooth-by-angle]
level: practitioner
status: verified
description: "Split mesh edges by angle or Sharp marks with Blender's Edge Split modifier for crisp shading, and when Smooth by Angle or custom normals are the better choice."
sources:
  - https://docs.blender.org/manual/en/latest/modeling/modifiers/generate/edge_split.html
  - https://docs.blender.org/manual/en/latest/modeling/modifiers/normals/smooth_by_angle.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# edge-split-modifier

Goal: crisp shading on chosen edges of a smooth-shaded mesh by splitting (duplicating) the edges, which breaks the links between faces so vertex normals are not shared across the edge.

## Settings

- **Edge Angle** (+ **Split Angle**): split an edge when the angle between its two faces is greater than Split Angle. At 0 all edges are split; at 180 none are.
- **Sharp Edges**: split edges marked Sharp.
- Both can be active at once. The manual says non-manifold edges are always split, but in a Blender 4.5.14 run an edge shared by three faces was not split (vertex count unchanged at Split Angle 180), so check before relying on it.
- Defaults: Edge Angle and Sharp Edges both on, Split Angle 30 degrees.

## Use it or not

The manual says this modifier is kept mostly for historical and compatibility reasons: everything it does for shading, and more, can be done with custom normals. Unless you really need the topology changes it generates, it advises against using it in new projects.

- **Smooth by Angle** sets edge sharpness by angle (Angle option, plus *Ignore Sharpness*). It is a geometry nodes asset in the bundled Essentials asset library; *Object > Shade Auto Smooth* adds it, and Shade Smooth or Shade Flat removes it.
- Splitting can also be done manually in Edit Mode (Edge Split operator).

## Stack placement

The manual's examples show smooth shading with Edge Split, and with Edge Split plus Subdivision Surface; compare the order in your own stack, since splitting changes topology that later modifiers see.

## Verify

Hard edges show a break in highlights under a matcap or lit render, while the Edit Mode mesh is unchanged (the modifier is non-destructive until applied).

## Checked

Date: 2026-10-27. Documentation release: Blender manual, 5.2 release branch (Edge Split and Smooth by Angle pages). Confirmed: options, always-split non-manifold edges, the historical-use note, Smooth by Angle as a bundled geometry nodes asset with the Shade Auto Smooth operator. Removed unconfirmed version gate, exporter and stack-order advice.
Run check, 2026-11-01, Blender 4.5.14 LTS headless: a cube gives 24 vertices at 30 degrees and at 0 degrees and 8 at 180 degrees; Sharp Edges alone gives 8 with no edge marked and 24 with all marked; a UV sphere stays at 482 vertices at 30 degrees and becomes 1984 at 0 degrees; a boundary plane is not split; the Smooth by Angle asset exists in the bundled assets (inputs Angle 30 degrees and Ignore Sharpness) and Shade Smooth and Shade Flat remove a Smooth by Angle modifier; Object menu lists Shade Auto Smooth. Corrected the non-manifold claim.

Method: manual text confirmed from documentation; Edge Split behaviour run headless in Blender 4.5.14.
