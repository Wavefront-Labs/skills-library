---
id: creative-arts.animation.blender.gp-fill-tool
name: gp-fill-tool
category: creative-arts
field: animation
product: blender
tags: [blender, grease-pencil, gp-fill-tool, gp-fill, gp-boundary-strokes, gap-closure]
level: practitioner
status: docs-checked
description: "Colour Grease Pencil line art with the Fill tool: fill solver, layers, direction, fill guides, gap closure (Radius/Extend), dilate and precision."
sources:
  - https://docs.blender.org/manual/en/latest/grease_pencil/modes/draw/tools/fill.html
  - https://docs.blender.org/manual/en/latest/grease_pencil/multiframe.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# gp-fill-tool

Goal: bucket-fill closed regions of line art reliably, frame after frame.

## Basics
Draw mode > **Fill** tool (uses the Fill brushes; picking a Fill brush activates the tool). Choose a material with Fill enabled and click inside a closed region. The result is a new closed stroke filled with the material, on the active layer.

## Fill settings (Tool Settings)
- **Direction** (hold Ctrl): Normal fills the region under the cursor; Inverted fills outside the boundary, for backgrounds.
- **Fill Solver** (Advanced): **Delaunay** uses stroke geometry and is independent of viewport resolution; **Pixel** rasterizes and flood fills, better for rough sketches.
- **Layers**: which layers form the boundary: Visible, Active, Layer Above, Layer Below, All Above, All Below.
- **Boundary**: All, Strokes or Edit Lines (fill guides only); Show Lines displays the boundary helpers.
- Pixel solver only: **Precision**, **Dilate/Contract** (grow the fill under the line), **Thickness**, **Simplify**, **Limit to Viewport**.
- Delaunay only: **Size** and **Size Unit** (View or Scene).
- **Ignore Transparent**: ignore strokes whose material opacity is below a threshold.
- **Auto-Remove Fill Guides**: delete fill guides after filling.

## Closing gaps
- **Fill guides**: Alt-LMB draws a temporary guide stroke across a gap; delete leftovers with Clean Up in the Grease Pencil menu (Edit mode), or enable Auto-Remove Fill Guides.
- **Gap Closure** (Pixel solver): Mode **Radius** (connect nearby open endpoints) or **Extend** (extend open stroke ends); Size, Detection Factor, Internal Gaps, Strokes Collision, Visual Aids. After the first click the helper lines show; change their length with PageUp/PageDown or the wheel, then click again to fill.

## Workflow
1. Lines on one layer, fills on another layer below it; set Layers so the boundary reads the line layer.
2. Fill regions per frame; fix leaks with fill guides or Gap Closure instead of redrawing lines.
3. With Multiframe on, the Fill tool applies to all selected keyframes.

## Verify
Hide the line layer: fills have no holes and tuck slightly under where lines were (raise Dilate if a sliver shows).

## Checked

2026-10-27, Blender 5.2 manual (projects.blender.org blender-manual, branch blender-v5.2-release RST) and Python API docs. Confirmed on the Fill Tool page: Direction (Ctrl), Fill Solver Delaunay/Pixel, Layers options, Boundary, Gap Closure modes Radius/Extend, Alt-LMB fill guides, PageUp/PageDown/Wheel for helper length, Auto-Remove Fill Guides. Removed the claims that fill works in screen space only (depends on solver), the Ctrl+Z leak advice and the Stroke Depth Order interaction, which no doc covers.
Method: documentation only; no commands were run.
