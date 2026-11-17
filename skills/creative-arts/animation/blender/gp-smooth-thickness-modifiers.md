---
id: creative-arts.animation.blender.gp-smooth-thickness-modifiers
name: gp-smooth-thickness-modifiers
category: creative-arts
field: animation
product: blender
tags: [blender, grease-pencil, gp-smooth-modifier, gp-thickness-modifier, line-weight, gp-modifiers]
level: practitioner
status: docs-checked
description: "Clean and style Grease Pencil lines non-destructively with the Smooth and Thickness modifiers: affect toggles, repeat, keep shape, uniform thickness and influence filters."
sources:
  - https://docs.blender.org/manual/en/latest/grease_pencil/modifiers/deform/smooth.html
  - https://docs.blender.org/manual/en/latest/grease_pencil/modifiers/deform/thickness.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# gp-smooth-thickness-modifiers

Goal: consistent line weight and smoothness across hand-drawn, Line Art or imported strokes.

## Smooth modifier

- **Affect**: Position, Strength (opacity), Thickness, UV (UV rotation).
- **Factor**: strength of the smoothing. **Repeat**: number of smoothing iterations (like running the Smooth tool several times; high values can reduce animation FPS).
- **Keep Shape**: try to maintain the overall shape of the original stroke. **Smooth Ends**: also smooth the stroke ends.
- Influence filters restrict where it applies.

Use after Line Art to remove stair-stepping, or on shaky tablet drawing.

## Thickness modifier

- **Thickness Factor**: value added to or subtracted from the existing point thickness.
- **Uniform Thickness**: makes the thickness equal for the entire stroke, with an absolute *Thickness*.
- Influence filters (layer, material, vertex group, custom curve along the stroke) restrict or shape the effect.

## Order

Modifiers apply top to bottom: generators such as Line Art first, then Smooth, then Thickness.

## Verify

Toggle the modifiers off and on and confirm weight and smoothness change without losing the shape.

## Checked

2026-10-27 against the Blender 5.2 manual (Grease Pencil Smooth and Thickness modifier pages and influence filters). Confirmed Smooth options (Affect, Factor, Repeat, Keep Shape, Smooth Ends) and Thickness options (Uniform Thickness, Thickness Factor). Removed the unconfirmed claim that Thickness Factor multiplies (the manual says it adds or subtracts), the "Normalize" option, version-specific units, the taper-curve recipe and the screen-space versus world-space gotcha.
Method: documentation only; no commands were run.
