---
id: creative-arts.animation.blender.text-extrude-bevel
name: text-extrude-bevel
category: creative-arts
field: animation
product: blender
tags: [blender, text-object, 3d-text, text-extrude, text-bevel, text-geometry, offset, resolution]
level: practitioner
status: docs-checked
description: "Give Blender text depth: Geometry Offset, Extrude and Bevel (shared with curves), Fill Solver Delaunay for fonts, materials per character and conversion to mesh."
sources:
  - https://docs.blender.org/manual/en/5.2/modeling/texts/properties.html
  - https://docs.blender.org/manual/en/5.2/modeling/curves/properties/geometry.html
  - https://docs.blender.org/manual/en/5.2/modeling/texts/selecting.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# text-extrude-bevel

Goal: crisp 3D lettering with chamfered or rounded edges.

## Properties > Data > Geometry

- **Offset** is specific to text: it offsets the control points of the curves that define the letters, making them thinner or thicker. Use with care: it quickly leads to artifacts.
- **Extrude**, **Taper** and **Bevel** are shared with curve data-blocks (see the curve-bevel and curve-taper skills): Bevel Round (Depth, Resolution, Fill Caps), Object and Profile modes, Factor Start/End.
- Bevel is applied to the curves that define the letters, so it normally follows their outlines (two parallel beveled curves rather than a single one).
- How a Taper Object acts depends on how the letter curves are built; results can look quite random.

## Shape panel

- Most Shape settings are shared with curves (Dimensions, Resolution Preview/Render U, Fill Mode, Twist).
- **Fill Solver**: most font files contain self-intersecting curves, so the manual recommends *Delaunay* for text objects (Sweep Line does not support self-intersection). **Fill Rule** (Even-Odd, Non-Zero) applies to Delaunay.
- **Fast Editing**: do not fill the letters in Edit Mode, only show outlines.

## Materials per part

- In Edit Mode select characters and assign different materials (the Selecting Text page notes the selection is used to specify materials and styles).
- A text object has no separate material slots for the front face, sides and bevel as such; to split them, convert to mesh (Object > Convert > Mesh) and assign by face selection.

## Cleanup after converting

The topology of converted text is usually messy: use a Limited Dissolve deletion or a Remesh modifier.

## Verify

Zoom in on tight letters such as `e`, `a`, `s`: no overlapping faces in wireframe; face orientation overlay all blue.

## Checked

Date: 2026-10-27. Documentation: Blender 5.2 manual (Text Properties, curve Geometry panel, Selecting Text, Editing Text Objects). Confirmed: Offset description, shared Extrude/Taper/Bevel, bevel following letter outlines, Fill Solver recommendation, Fill Rule, Fast Editing, materials by selection, cleanup tip. Removed as unconfirmed: extrude symmetry and numeric depth/offset values, default Fill Mode and Preview U, Shade Auto Smooth and Weighted Normal advice, Fill Caps statement, and the Geometry-node normal mask for separating faces.
Method: documentation only; no commands were run.
