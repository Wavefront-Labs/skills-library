---
id: creative-arts.animation.blender.box-lasso-mask
name: box-lasso-mask
category: creative-arts
field: animation
product: blender
tags: [blender, sculpting, box-mask, lasso-mask, line-mask, polyline-mask, gesture-mask, masking]
level: practitioner
status: docs-checked
description: "Make fast precise sculpt masks in Blender with gesture tools: Box, Lasso, Line and Polyline Mask, Front Faces Only, Limit to Segment, plus Hide and Face Set gestures."
sources:
  - https://docs.blender.org/manual/en/latest/sculpt_paint/sculpting/tools/mask_tools.html
  - https://docs.blender.org/manual/en/latest/sculpt_paint/sculpting/introduction/gesture_tools.html
  - https://docs.blender.org/manual/en/latest/sculpt_paint/sculpting/tools/hide_tools.html
  - https://docs.blender.org/manual/en/latest/sculpt_paint/sculpting/tools/face_set_tools.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# box-lasso-mask

Goal: crisp, geometric masks without painting: straight cuts across limbs, rectangular panels, freehand regions.

## Tools (Toolbar in Sculpt Mode)

- **Box Mask** (shortcut B): drag a rectangle.
- **Lasso Mask**: freehand outline. The Lasso Mask operator is also on Ctrl-RMB.
- **Line Mask**: acts on everything on the highlighted side of the drawn line, extended both ways in the viewport. **Flip** (F) switches sides, **Snap** (Ctrl) constrains the line angle (5 degree steps by default, set in the header Snapping menu), **Limit to Segment** stops the effect at the ends of the drawn line.
- **Polyline Mask**: each LMB click adds a point; click the start point, double-click, or press Return to close.
- All mask gestures fully mask by default; holding Ctrl while selecting clears the mask. Hold Space to reposition the gesture while drawing.
- **Front Faces Only** (tool setting): only faces facing the view are masked. Turn it off to mask through the mesh, for example to slice straight across a limb.
- The same four gestures exist as Hide tools (Box/Lasso/Line/Polyline Hide: Ctrl reveals, a plain click without dragging reveals everything) and Face Set tools (each creates one new face set; also have Front Faces Only).

## Recipes

- Separate a hand: Line Mask across the wrist in front view with Front Faces Only off, then Mask > Mask Slice (with Slice to New Object) or Face Sets > Face Set from Masked.
- Panel lines on a hard-surface sculpt: Box Mask rectangles, Invert Mask (A pie, Ctrl-I), then work the unmasked area with the Layer brush or the Inflate mesh filter.

## Gotchas

- Masks are per vertex, so edges follow mesh resolution. Soften or sharpen the result with Mask > Mask Filters (Smooth/Sharpen, Grow/Shrink, Contrast).
- Gesture tools work in view space; rotate the view to align before drawing.

## Verify

The mask overlay shows straight, full-depth boundaries when Front Faces Only is off, and the result of Mask Slice matches the drawn shape.

## Checked

2026-10-27, Blender 5.2 manual (blender-v5.2-release branch). Confirmed against sculpt_paint/sculpting/tools/mask_tools, hide_tools, face_set_tools, introduction/gesture_tools and editing/mask: tool names, B shortcut for Box Mask, Ctrl-RMB for the Lasso Mask operator, Ctrl clears, Space moves, Line gesture Flip (F), Snap (Ctrl, 5 degree default) and Limit to Segment, Polyline closing methods, Front Faces Only. Removed the Polyline version gate, Alt angle snap and the Ctrl-W claim, which the manual does not support.
Method: documentation only; no commands were run.
