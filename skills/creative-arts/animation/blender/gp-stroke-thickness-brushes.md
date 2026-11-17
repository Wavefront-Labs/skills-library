---
id: creative-arts.animation.blender.gp-stroke-thickness-brushes
name: gp-stroke-thickness-brushes
category: creative-arts
field: animation
product: blender
tags: [blender, grease-pencil, gp-stroke-thickness, gp-brush-settings, gp-pressure, gp-radius]
level: practitioner
status: docs-checked
description: "Tune Grease Pencil draw brushes: size and strength with pressure curves, stabilise, active smooth, post-processing, randomize, spacing and layer thickness override."
sources:
  - https://docs.blender.org/manual/en/latest/grease_pencil/modes/draw/brushes/draw.html
  - https://docs.blender.org/manual/en/latest/grease_pencil/properties/layers.html
  - https://docs.blender.org/manual/en/latest/grease_pencil/modes/edit/stroke_menu.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# gp-stroke-thickness-brushes

Goal: line quality that matches the intended style and is consistent across shots.

## Size and strength
Draw brush **Size** is the brush diameter in pixels (F adjusts interactively); **Strength** is stroke alpha from 0.0 to 1.0 (Shift-F). Each has a stylus **pressure** toggle whose response is a curve widget: shape it to keep light pressure thin. Layer Adjustments > **Stroke Thickness** overrides thickness for a whole layer, and Tint Color tints it.

## Stroke behaviour (Brush settings > Stroke)
- **Post-Processing** (runs after the stroke): Smooth, Iterations, Subdivisions, Simplify, **Trim Strokes End**, **Outline** (Material, Thickness), Curve Type (Catmull Rom, Poly, Bezier, NURBS) with Threshold.
- **Randomize**: Radius, Strength, UV, Hue, Saturation, Value, Jitter; Stroke Random limits randomness to stroke level; Use Pressure scales effects.
- **Stabilize Stroke**: Radius and Factor.
- Advanced: Spacing (percent of size), **Active Smooth**, Angle and Factor (calligraphy), Hardness and Aspect (for Dot or Box stroke materials only).
- Caps Type: Round or Flat; Stroke Mode: Stroke, Fill or Both.

## Presets
Brushes are assets listed in the Asset Shelf (Draw category); duplicate a bundled brush before editing it.

## Gotchas
- Brush changes affect only new strokes; use Stroke > Set Uniform Thickness or Edit/Sculpt tools to change existing ones.
- Strong Simplify removes fine detail such as eye highlights.
- Hardness has no effect on normal line strokes; it needs Dots or Squares.

## Verify
Draw a test sheet of light, medium and heavy strokes and compare with the style frame at render resolution.

## Checked

2026-10-27, Blender 5.2 manual (projects.blender.org blender-manual, branch blender-v5.2-release RST) and Python API docs. Confirmed Size in pixels, Strength range and Shift-F, pressure curve widgets, Post-Processing, Randomize, Stabilize Stroke, Active Smooth, Spacing, Hardness limitation and Layer Stroke Thickness on the Draw Brushes and Layers pages. Removed Radius-in-scene-units, pre-4.3 Thickness Scale, tablet API preference and the recommended settings that no manual page states.
Method: documentation only; no commands were run.
