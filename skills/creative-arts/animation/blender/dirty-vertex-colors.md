---
id: creative-arts.animation.blender.dirty-vertex-colors
name: dirty-vertex-colors
category: creative-arts
field: animation
product: blender
tags: [blender, vertex-paint, dirty-vertex-colors, cavity-vertex-colors, cavity, ambient-occlusion]
level: practitioner
status: docs-checked
description: "Generate cavity and edge-wear maps as vertex colours in Blender with Dirty Vertex Colors: blur, highlight and dirt angles, dirt only, normalize."
sources:
  - https://docs.blender.org/manual/en/latest/sculpt_paint/vertex_paint/editing.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# dirty-vertex-colors

Goal: a cheap, bake-free cavity mask stored on vertices for wear, dirt or stylised shading.

## Run it

Vertex Paint mode, Paint menu, **Dirty Vertex Colors**. It generates a dirt map gradient based on cavity. Options:

| Option | Effect |
|---|---|
| Blur Strength | Blur strength per iteration |
| Blur Iterations | Number of blur passes; higher blurs more |
| Highlight Angle | Clamps the angle for convex areas. Lower values raise contrast but can clamp. 90 is flat, 180 is infinitely pointed |
| Dirt Angle | Clamps the angle for concave areas. Higher values raise contrast but can clamp. 90 is flat, 0 is infinitely deep |
| Dirt Only | Does not calculate cleaning of convex areas |
| Normalize | Picks optimal contrast by lowering Highlight Angle and raising Dirt Angle automatically |

Turn Normalize off to get consistent results across multiple objects.

## Related Paint-menu tools (same page)

Smooth Vertex Colors, Vertex Color from Weight (active weight to grayscale), Invert, Levels, Hue/Saturation/Value, Brightness/Contrast on selected vertices, and Set Vertex Colors (Ctrl X, fills the active Color Attribute with the paint colour; Affect Alpha sets it opaque). Sample Color: Shift X samples under the cursor, Shift Ctrl X samples the merged viewport colour including lighting and shading.

## Practical notes

- The result depends on mesh density, so work on a mesh with enough vertices.
- Check the result in a viewport mode that displays the colour attribute.

## Checked

Method: 2026-11-09 read the Blender manual source for Editing Vertex Paint Colors; removed shader-use, alternatives and behaviour claims the page does not state.
