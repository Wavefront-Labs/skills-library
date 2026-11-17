---
id: creative-arts.animation.blender.gp-outline-modifier
name: gp-outline-modifier
category: creative-arts
field: animation
product: blender
tags: [blender, grease-pencil, gp-outline-modifier, gp-outline, stroke-to-fill, gp-modifiers]
level: practitioner
status: docs-checked
description: "Convert Grease Pencil strokes to camera-facing outlines with the Outline modifier: thickness, target material, subdivisions, sample length and keep shape."
sources:
  - https://docs.blender.org/manual/en/latest/grease_pencil/modifiers/generate/outline.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# gp-outline-modifier

Goal: render strokes as outline shapes (double lines, coloured border around thick strokes).

## Settings (Grease Pencil Outline modifier)

- **Thickness**: thickness of the generated outline strokes.
- **Keep Shape**: the perimeter strokes stay inside the original stroke perimeter to keep the original shape.
- **Subdivisions**: number of subdivisions of the generated outline.
- **Sample Length**: accuracy of the perimeter conversion.
- **Outline Material**: material for the generated outline strokes.
- **Target Object**: controls the origin of the generated cyclic strokes.
- Influence filters.

## Uses

- Comic-style outlines around thick strokes.
- Turning stroke perimeters into new strokes that carry their own material.

## Verify

Check that every filtered stroke has a perimeter stroke in the outline material.

## Checked

2026-10-27 against the Blender 5.2 manual (Grease Pencil Outline modifier page). Confirmed Thickness, Keep Shape, Subdivisions, Sample Length, Outline Material and Target Object. Removed unconfirmed claims about a required scene camera and view-dependence, a separate Target Material setting, the Edit Mode Stroke menu alternative and the short-stroke gotcha.
Method: documentation only; no commands were run.
