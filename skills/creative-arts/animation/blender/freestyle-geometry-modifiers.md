---
id: creative-arts.animation.blender.freestyle-geometry-modifiers
name: freestyle-geometry-modifiers
category: creative-arts
field: animation
product: blender
tags: [blender, freestyle-geometry-modifiers, freestyle-strokes, freestyle-chaining, freestyle, line-style, npr]
level: advanced
status: docs-checked
description: "Shape Freestyle strokes: chaining, splitting, sorting, caps and dashes, plus geometry modifiers such as sampling, Bezier, noise, backbone stretcher and blueprint."
sources:
  - https://docs.blender.org/manual/en/latest/render/freestyle/view_layer/line_style/strokes.html
  - https://docs.blender.org/manual/en/latest/render/freestyle/view_layer/line_style/modifiers/geometry/index.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# freestyle-geometry-modifiers

Goal: sketchy, hand-drawn or technical stroke geometry rather than clean vector edges.

## Strokes panel (Line Style → Strokes)

- **Chaining**: *Plain* (join connected edges into long strokes) or *Sketchy* (multiple overlapping passes with *Rounds*). *Same Object* keeps strokes per object.
- **Splitting**: break strokes at a *Min/Max 2D Angle*, every *2D Length*, or at material boundaries; *Pattern* for dash-like splitting.
- **Sorting**: *Sort Key* (Distance from Camera, 2D Length, Projected X/Y) with *Integration Type* and *Sort Order* (Reverse); controls how overlapping strokes stack.
- **Selection**: *Min/Max 2D Length* and *Chain Count* (first N chains).
- **Caps**: Butt, Round, Square.
- **Dashed Line**: three Dash/Gap pairs; a zero gap makes that dash be ignored. Dashes are separate strokes, so caps and colour, alpha and thickness modifiers apply to them.

## Geometry modifiers

| Modifier | Effect |
|---|---|
| Sampling | stroke precision for the modifiers after it; smaller value = more precise |
| Bezier Curve | replaces the stroke with a Bezier approximation (*Error* = max distance) |
| Simplification | merges close vertices (*Tolerance*) |
| Sinus Displacement | wavy strokes (*Wavelength*, *Amplitude*, *Phase*) |
| Spatial Noise / Perlin Noise 1D / Perlin Noise 2D | hand-drawn wobble |
| Backbone Stretcher | adds *Backbone Length* to both stroke ends |
| Tip Remover | removes *Tip Length* at both ends |
| Polygonization | simplifies strokes to jagged polylines (*Error*) |
| Guiding Lines | replaces a stroke with a straight line between its ends (*Offset*) |
| Blueprint | circles, ellipses or squares drawn over several *Rounds* |
| 2D Offset / 2D Transform | offset (Start, End, X, Y); scale then rotate around a *Pivot* |

Order matters: modifiers apply top to bottom. Put Sampling first, then displacement/noise.

## Gotchas

- Perlin Noise 1D has a *Seed* (same seed on a stroke gives the same result); Spatial Noise has none (Pure Random option instead).
- Sketchy chaining generates *Rounds* strokes per chain and is only useful with random-driven modifiers.
- Manual warning: too small Sampling values need a huge amount of time and memory at render.
- Guiding Lines works best on short strokes: combine with splitting by 2D angle or 2D length.

## Verify

Render a still at final resolution and confirm overshoot with Backbone Stretcher, wobble with noise and dashes where set.

## Checked

2026-10-27 against the Blender 5.2 manual (Freestyle, Line Style, Strokes and Geometry Modifiers pages). Confirmed Strokes panel options (caps, chaining, splitting, sorting, selection, dashes) and the geometry modifier names and parameters. Removed unconfirmed pixel units and the claim that noise without a seed changes per frame.
Method: documentation only; no commands were run.
