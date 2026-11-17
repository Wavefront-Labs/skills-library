---
id: creative-arts.animation.blender.gp-vertex-paint
name: gp-vertex-paint
category: creative-arts
field: animation
product: blender
tags: [blender, grease-pencil, gp-vertex-paint, gp-tint, vertex-color, 2d-colouring]
level: practitioner
status: docs-checked
description: "Colour Grease Pencil strokes and fills with vertex paint: brushes, Stroke/Fill modes, the Tint brush, Color Attribute paint mode, mix factor and Paint menu."
sources:
  - https://docs.blender.org/manual/en/latest/grease_pencil/modes/vertex_paint/introduction.html
  - https://docs.blender.org/manual/en/latest/grease_pencil/modes/vertex_paint/brushes.html
  - https://docs.blender.org/manual/en/latest/grease_pencil/modes/vertex_paint/editing.html
  - https://docs.blender.org/manual/en/latest/grease_pencil/modes/vertex_paint/tool_settings/brush.html
  - https://docs.blender.org/manual/en/latest/grease_pencil/modes/draw/brushes/tint.html
  - https://docs.blender.org/manual/en/latest/grease_pencil/modes/draw/tool_settings/color.html
  - https://docs.blender.org/manual/en/latest/editors/3dview/display/overlays.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# gp-vertex-paint

Goal: per-stroke colour variation without making dozens of materials.

## How it works
Each point can carry a colour (Color Attribute) that mixes with the material Base Color according to the brush settings. Vertex paint works in sRGB while materials are in linear space, so equal RGB values look different. In Draw mode, vertex paint shows only in Material Preview and Rendered shading by default; use Vertex Paint mode, or set Solid shading Color to Attribute, to see it in Solid. The Vertex Paint Opacity overlay controls its visibility.

## Vertex Paint mode brushes (Essentials)
| Brush | Effect |
|---|---|
| Paint Point Color | Paint a colour onto points |
| Blur Point Color | Smooth colours of adjacent points (colour value ignored) |
| Average Point Color | Paint the average of colours under the brush |
| Smear Point Color | Drag colours along |
| Replace Point Color | Change only points that already have a colour |
Brush settings: Blend, Size, Strength, **Mode** (Stroke, Fill, Stroke & Fill), colour picker and palette, Falloff. Selection Mask (1, 2, 3) restricts painting to selected points or strokes; Multiframe applies across keyframes.

## Tint brush (Draw mode)
Brush > **Tint** paints colour onto points of existing strokes, mixing with the material colour; Mode is Stroke and Fill, Stroke or Fill, and Ctrl-LMB erases the colour attribute.

## Drawing with a colour attribute
Draw mode Color panel: **Paint Mode** Material (stroke or fill base colour) or Color Attribute; **Mode** Stroke, Fill or Stroke & Fill; **Mix Factor** between the chosen colour and the base material colour.

## Paint menu (Vertex Paint mode)
Set Color Attribute, Reset Vertex Color, Invert, Levels, Hue/Saturation/Value, Brightness/Contrast, Sample Color (Shift-X).

## Gotchas
- Colour mixes with, not multiplies, the material colour.
- Check modifiers (such as Tint) when colours look off.
- Reset Vertex Color on selected strokes (all if none selected) removes the colour attribute.

## Verify
Paint > Reset Vertex Color on a test stroke returns it to the material colour.

## Checked

2026-10-27, Blender 5.2 manual (projects.blender.org blender-manual, branch blender-v5.2-release RST) and Python API docs. Confirmed brush names, Mode options (Stroke & Fill), Paint Mode Material or Color Attribute, Mix Factor, Tint brush Ctrl-LMB erase, Paint menu operators, sRGB note and the Draw mode visibility caveat. Removed Draw/Blur/Average/Smear/Replace short names and the alpha-zero description, and the SVG/PDF export claim.
Method: documentation only; no commands were run.
