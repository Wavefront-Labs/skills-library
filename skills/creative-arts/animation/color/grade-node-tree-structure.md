---
id: creative-arts.animation.color.grade-node-tree-structure
name: grade-node-tree-structure
category: creative-arts
field: animation
product: color
tags: [node-tree, node-structure, resolve, serial-nodes, parallel-nodes, layer-mixer, colour-grading, look-and-matching, fixed-node-tree]
level: practitioner
status: draft
description: "Build a fixed, reusable node tree for grading an animated show in Resolve: balance, contrast, secondaries, look and output nodes in a set order that copies across shots."
sources:
  - https://documents.blackmagicdesign.com/UserManuals/DaVinci_Resolve_19_Reference_Manual.pdf
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Node tree structure for a grade

**Goal:** every shot uses the same node order and labels, so grades copy cleanly, notes map to a node, and any
colourist can pick up a shot.

## A standard tree (serial unless noted)

```
01 IN-CST     colour space transform in (if not using RCM/ACES project settings)
02 BALANCE    offset / printer lights exposure + white balance
03 CONTRAST   contrast + pivot, soft clip
04 SAT        global saturation
05 SEC-1      qualifier or window fix (skin, sky)          [parallel or layer mixer for multiple]
06 SEC-2      power window relight                        (see power-windows)
07 SHOT LOOK  per-shot creative tweak
-- group post-clip --
08 SEQ LOOK   sequence look from colour script
-- timeline --
09 SHOW LOOK  show LUT / LMT
10 OUT-CST    output transform, then limiter
```

Label nodes (right-click > Node Label); Resolve shows labels in thumbnails and copy operations.

## Why this order

- Corrections before looks: balancing after a creative LUT fights its curve.
- Secondaries after primaries so qualifiers key on a stable image.
- Group and timeline levels (see `creative-arts.animation.color.group-and-timeline-grading`) carry sequence and show
  looks, so a director's "warmer for the whole act" is one change.

## Parallel vs layer

- **Parallel mixer:** several secondaries each on the same input, blended; good for independent fixes.
- **Layer mixer:** lower nodes win where they overlap; used when one fix should override another.
- **Outside node:** the inverse of a qualifier/window, for "everything except the character".

## Copying

- Save the empty tree as a still in the Gallery (`creative-arts.animation.color.gallery-stills-and-grade-reuse`) and
  apply to all clips at start (*Apply Grade*, or append node graph).
- Copy a specific node across shots with middle-click on a still in the gallery or by selecting the target clips and
  using *Apply Grade - Keep Node Graph* variants.

## Verify

Every clip in the timeline shows the same labelled nodes in the same order (spot-check ten) and disabling node 07
(shot look) on a matched sequence leaves shots still matching each other.
