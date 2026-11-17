---
id: creative-arts.animation.blender.gp-keyframe-types
name: gp-keyframe-types
category: creative-arts
field: animation
product: blender
tags: [blender, grease-pencil, gp-keyframe-types, gp-extremes, gp-breakdown, dope-sheet]
level: practitioner
status: docs-checked
description: "Mark Grease Pencil drawings by role with keyframe types (keyframe, breakdown, moving hold, extreme, jitter, generated) and filter onion skins by type."
sources:
  - https://docs.blender.org/manual/en/latest/animation/keyframes/introduction.html
  - https://docs.blender.org/manual/en/latest/grease_pencil/properties/onion_skinning.html
  - https://docs.blender.org/manual/en/latest/editors/dope_sheet/modes/grease_pencil.html
  - https://docs.blender.org/manual/en/latest/editors/dope_sheet/editing.html
  - https://docs.blender.org/manual/en/latest/grease_pencil/modes/draw/tools/interpolate.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# gp-keyframe-types

Goal: a dope sheet that reads like an exposure sheet: keys, extremes and inbetweens are distinguishable.

## Types (Dope Sheet, Key > Keyframe Type, shortcut R)
| Type | Meaning in the manual |
|---|---|
| Keyframe | Normal keyframe (white or yellow diamond) |
| Breakdown | Transitions between key poses (small cyan diamond) |
| Moving Hold | Small motion around a holding pose; the Dope Sheet draws a bar between them |
| Extreme | An extreme state, or other purpose as needed (big pink diamond) |
| Jitter | Filler or baked key, for keying on ones (tiny green diamond) |
| Generated | Key made by a tool; tools may safely remove and regenerate them, so do not mark hand-made work with it |

## Using types
- Onion Skinning panel > **Filter by Type** limits ghosts to chosen keyframe types.
- Interpolate and Interpolate Sequence create Breakdown keys; **Exclude Breakdowns** stops them being used as extremes.
- Interpolated keyframes (breakdowns) show as smaller light blue points in the Grease Pencil Dope Sheet.

## Workflow (key-to-key)
1. Draw keys, leave as Keyframe.
2. Mark extremes as Extreme.
3. Breakdowns by hand or Interpolate.
4. Inbetweens last; filter onion skin to the types you are comparing.

## Gotchas
- Type is a label for visualisation and tool behaviour; it does not change timing.
- Changing a Breakdown to Keyframe makes it count as a proper extreme for later interpolation.

## Verify
The Dope Sheet shows a readable pattern of large keys and small breakdowns that matches the timing chart.

## Checked

2026-10-27, Blender 5.2 manual (projects.blender.org blender-manual, branch blender-v5.2-release RST) and Python API docs. Confirmed the six keyframe types and their meanings, onion skin Filter by Type, Exclude Breakdowns and the breakdown display in the Grease Pencil Dope Sheet. Removed a default-keyframe-type header setting and the claim that Interpolate marks frames Generated (it creates breakdowns); the manual source previously cited did not describe types.
Method: documentation only; no commands were run.
