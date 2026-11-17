---
id: creative-arts.animation.blender.gp-array-modifier
name: gp-array-modifier
category: creative-arts
field: animation
product: blender
tags: [blender, grease-pencil, gp-array-modifier, gp-array, gp-modifiers, motion-graphics]
level: practitioner
status: docs-checked
description: "Repeat Grease Pencil strokes with the Array modifier: count, relative/constant/object offsets, random offset/rotation/scale, and material overrides."
sources:
  - https://docs.blender.org/manual/en/latest/grease_pencil/modifiers/generate/array.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# gp-array-modifier

Goal: repeated strokes (fences, rain streaks, pattern borders, motion-graphic repeats) from one drawing.

## Settings (Grease Pencil Array modifier)

- **Count**: total number of copies.
- **Material Override**: index of the material for duplicated strokes (0 keeps the original materials).
- **Relative Offset** (*Factor X, Y, Z*): translation equal to the bounding box size times the factor.
- **Constant Offset** (*Factor X, Y, Z*): constant translation per copy.
- **Object Offset** (*Distance X, Y, Z*): adds a transformation taken from an object (relative to the current object); the manual recommends an empty centred on or near the initial object.
- **Randomize**: *Offset*, *Rotation*, *Scale* (X, Y, Z each), *Uniform Scale* (same seed for every scale axis) and *Seed*.
- Influence filters (see the Grease Pencil modifier introduction).

## Recipes

- Radial pattern: give the empty a rotation and use Object Offset with the Relative Offset factors set to zero.
- Rain: one streak with a large random offset.

## Gotchas

- The object's *Depth Order* setting changes how the copies are displayed (manual note).
- Several Array modifiers can be active at once for complex constructs.

## Verify

Toggle the modifier: one original versus the expected copies and random spread.

## Checked

2026-10-27 against the Blender 5.2 manual (Grease Pencil Array modifier page). Confirmed Count, Material Override semantics, the offset groups and Randomize fields. Removed the unconfirmed default offset of 1,0,0, the cumulative-scale claim, specific recipe numbers, parenting advice and render cost remarks.
Method: documentation only; no commands were run.
