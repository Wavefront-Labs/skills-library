---
id: creative-arts.animation.blender.vertex-paint-brush-masking
name: vertex-paint-brush-masking
category: creative-arts
field: animation
product: blender
tags: [blender, vertex-paint, vertex-paint-brush, vertex-paint-masking, color-attributes, selection-masking]
level: practitioner
status: docs-checked
description: "Vertex paint in Blender with control: brush types, colour attribute domain and data type, the paint mask for per-face-corner colours, Set Vertex Colors, Sample Color."
sources:
  - https://docs.blender.org/manual/en/latest/sculpt_paint/vertex_paint/brushes.html
  - https://docs.blender.org/manual/en/latest/sculpt_paint/vertex_paint/editing.html
  - https://docs.blender.org/manual/en/latest/modeling/meshes/properties/object_data.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---
# vertex-paint-brush-masking

Goal: paint vertex colours exactly where intended, with hard or soft transitions.

## Colour attribute first
Object Data > **Color Attributes** > plus. **Domain**: *Vertex* (one colour per vertex) or *Face Corner* (per corner of each face). **Data Type**: *Color* (floating-point RGBA) or *Byte Color* (8-bit RGBA). Painting a vertex modifies connected faces and edges with a gradient to neighbouring vertex colours; occluded faces are not modified.

## Brushes
Brush types and Essentials brushes: Paint Vertex (Paint Hard, Paint Soft, Paint Hard Pressure, Paint Soft Pressure, Airbrush), Blur (colour value ignored; strength sets the blur), Average (paints the average colour under the brush), Smear (drags colours like finger painting). Brush Strength can be changed interactively with Shift-F; the brush settings include Front Faces Only.
- **Paint > Set Vertex Colors** (Ctrl-X) fills the active colour attribute with the current paint colour; *Affect Alpha* sets the colour fully opaque instead of reusing existing alpha.
- **Paint > Sample Color**: Shift-X samples the colour under the cursor into the active Paint brush; Shift-Ctrl-X samples the merged viewport colour including lighting and shading. From the menu you can drag across colours to sample their average.

## Masking and hard edges
Enabling the **paint mask** in the Vertex Paint header paints per face corner; the manual says this is useful for sharp edges in the colour attribute on low-poly assets. Editing operators (Smooth, Invert, Levels, Hue/Saturation/Value, Brightness/Contrast) act on the selected vertices.

## Gotchas
- Vertex colour resolution is the vertex count; for much higher density, the manual points to painting in Sculpt mode.
- Front Faces Only decides whether strokes affect the back of thin geometry.

## Verify
Viewport Shading > Solid > Color: **Attribute** shows the active colour attribute.

## Checked
Date: 2026-10-27. Documentation: Blender manual (Vertex Paint brushes and editing, Object Data, brush settings), branch blender-v5.2-release. Confirmed: brush types and names, Set Vertex Colors with Ctrl-X and Affect Alpha, Sample Color shortcuts, paint mask for per-corner painting, Domain and Data Type options, Solid Attribute view. Removed unconfirmed claims: the Shift-K shortcut, the long blend mode list, sRGB and engine import remarks, face and vertex selection masking toggle details, hide and unhide masking and the Byte Color clipping note.
Method: documentation only; no commands were run.
