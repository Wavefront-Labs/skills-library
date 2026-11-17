---
id: creative-arts.animation.blender.mask-modifier
name: mask-modifier
category: creative-arts
field: animation
product: blender
tags: [blender, mask-modifier, modifiers, vertex-groups, armature, hide-geometry]
level: practitioner
status: docs-checked
description: "Hide part of a Blender mesh non-destructively with the Mask modifier: Vertex Group and Armature modes, Invert, Threshold and Smooth, for hiding body under clothing."
sources:
  - https://docs.blender.org/manual/en/latest/modeling/modifiers/generate/mask.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# mask-modifier

Goal: show only part of a mesh (hide the body under a costume, isolate a limb while checking weights) without deleting geometry.

## Modes

- **Vertex Group**: hides all vertices not in the chosen vertex group.
- **Armature**: in Pose Mode, vertices belonging to the vertex group with the same name as the active bone are visible; the rest are hidden.
- **Invert**: shows only vertices that do *not* belong to the group (or active bone's group). This is the usual way to hide a body region under clothing.
- **Threshold**: hides vertices with weights less than or equal to the value.
- **Smooth** (Vertex Group mode): uses weights to cut faces at the weight contour, giving a smoother mask edge instead of sharp edges.

## Uses

- Hide body under clothing: group the covered area, enable Invert.
- Weight checking: Armature mode while posing, so only the active bone's region shows.
- Outfit swaps: the modifier's visibility toggles can be driven from rig properties (standard Blender drivers; not covered on the manual page).

## Verify

Toggle the modifier: the hidden region disappears and reappears.

## Checked

Date: 2026-10-27. Documentation release: Blender manual, 5.2 release branch (Mask modifier page). Confirmed: two modes and their behaviour, Invert, Threshold comparison, Smooth. Corrected: Armature mode shows the active bone's group, not all selected bones. Removed the unconfirmed 4.x version tag, default threshold, stack-order and export advice.
Method: documentation only; no commands were run.
