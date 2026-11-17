---
id: creative-arts.animation.blender.line-art-occlusion
name: line-art-occlusion
category: creative-arts
field: animation
product: blender
tags: [blender, line-art, line-art-occlusion, occlusion-levels, material-mask, hidden-lines]
level: practitioner
status: docs-checked
description: "Show hidden lines and selective visibility with Line Art: occlusion level ranges, material masks with exact match, intersection masks and transparency."
sources:
  - https://docs.blender.org/manual/en/latest/grease_pencil/modifiers/generate/line_art.html
  - https://docs.blender.org/manual/en/latest/render/materials/line_art.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# line-art-occlusion

Goal: draw hidden lines, or lines only where certain faces occlude them.

## Occlusion levels

Line Art modifier → **Occlusion** subpanel. *Range* enabled: the modifier selects lines whose occlusion level lies between the start and end values; *Level* is the desired occlusion level. 0 means visible lines (no occlusion), 1 means lines occluded by exactly one layer of faces. For hidden-line drawing, use a second Line Art modifier with a higher level or range and its own layer and material (each Line Art modifier runs its own full calculation).

## Material masks

1. Material Properties → **Line Art** panel on the occluding material: enable *Material Mask*, choose *Masks* (the layers that include faces of this material) and optionally *Levels* (faces with this material behave as if they had that many layers in occlusion).
2. Line Art modifier → Occlusion → **Material Mask**: enable it and pick *Masks*; with *Exact Match* only lines occluded with the exact mask bit combination are selected, otherwise occlusion by any one of the chosen masks is enough.

Edges occluded by those faces can then get a different style.

## Intersection masks

Collection Properties → Line Art → *Collection Mask* (custom intersection mask for faces in the collection). Line Art modifier → **Intersection** subpanel: *Collection Mask* bits and *Exact Match* (require all masks instead of just one) select which intersections produce lines.

## Gotchas

- Masks belong to materials, so objects sharing a material share the behaviour.
- Material *Intersection Priority* takes precedence over the Object and Collection priority values.

## Verify

The hidden-line modifier draws lines only behind surfaces in its own material, and the visible modifier is unaffected.

## Checked

2026-10-27 against the Blender 5.2 manual (Line Art Modifier page, Material Line Art page, Collections page). Confirmed Occlusion Range and Level semantics, Material Mask and Exact Match, intersection masks and material panel fields. Removed the unconfirmed 8-bit mask count, Start 1 / End 128 example, Invert option, occlusion effectiveness wording and the computation-cost claim for high ranges.
Method: documentation only; no commands were run.
