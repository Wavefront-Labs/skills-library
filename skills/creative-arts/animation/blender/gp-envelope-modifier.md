---
id: creative-arts.animation.blender.gp-envelope-modifier
name: gp-envelope-modifier
category: creative-arts
field: animation
product: blender
tags: [blender, grease-pencil, gp-envelope-modifier, gp-envelope, sketch-lines, gp-modifiers]
level: practitioner
status: docs-checked
description: "Create sketchy hatching and filled envelopes from Grease Pencil strokes with the Envelope modifier: deform/segments/fills modes, spread, thickness, skip."
sources:
  - https://docs.blender.org/manual/en/latest/grease_pencil/modifiers/generate/envelope.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# gp-envelope-modifier

Goal: stylised construction-line and loose-sketch looks generated from clean strokes.

## Modes

- **Deform**: replaces the original stroke with the envelope shape.
- **Segments**: adds segments that create the envelope shape while keeping the original stroke.
- **Fill**: adds segments to create the envelope without the original stroke.

The envelope connects all points that have n points between them.

## Settings

- **Spread Length**: number of points skipped when creating the straight segments of the envelope.
- **Thickness** and **Strength** (opacity) of the generated segments.
- **Skip Segments**: number of generated segments to skip, to reduce complexity.
- **Material Index**: material for the generated segments.
- Influence filters (layer, layer pass, material, material pass, vertex group, custom curve; availability varies by modifier).

## Recipe

Sketch look on Line Art strokes: Line Art, then Envelope in Segments mode with a thin grey material, then a Noise modifier for wobble.

## Gotchas

- Dense strokes generate many segments; raise Skip Segments or restrict with influence filters.

## Verify

Toggle the modifier and check the extra connecting strokes appear only where intended.

## Checked

2026-10-27 against the Blender 5.2 manual (Grease Pencil Envelope modifier page). Confirmed the three modes, Spread Length, Thickness, Strength, Material Index and Skip Segments. Removed the unconfirmed "Fills" naming (the mode is Fill), example numeric values and the resampling and viewport interactivity remarks.
Method: documentation only; no commands were run.
