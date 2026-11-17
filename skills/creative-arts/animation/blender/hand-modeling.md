---
id: creative-arts.animation.blender.hand-modeling
name: hand-modeling
category: creative-arts
field: animation
product: blender
tags: [blender, hand-modeling, finger-topology, character-modeling, hands, edge-flow]
level: advanced
status: docs-checked
description: "Model hands and fingers for animation: palm blockout, three segments per finger with knuckle loops, thumb placement, nails, loop counts and joining to the arm."
sources:
  - https://docs.blender.org/manual/en/latest/modeling/meshes/editing/face/extrude_faces.html
  - https://docs.blender.org/manual/en/latest/modeling/meshes/editing/face/inset_faces.html
  - https://docs.blender.org/manual/en/latest/modeling/meshes/structure.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# hand-modeling

Goal: a hand that reads well and bends at every knuckle.

## Blockout

1. Box for the palm: 4 faces across the front edge for the four fingers (with a face gap between each optional for webbing).
2. Extrude each finger face three times for the phalanges, each shorter toward the tip.
3. Thumb from the side of the palm near the wrist, angled down and forward; two visible segments plus the thenar (palm) mass.
4. Round fingers: keep the edge count around each finger low and add more only for hero close-ups.

## Knuckle loops

Each knuckle gets three loops like any joint (`creative-arts.animation.blender.joint-topology`). Add a small wedge on the back for the knuckle bump and a crease loop on the palm side.

## Details

- Nails: inset the top face of the last segment, extrude slightly down, then up; add a support loop for the cuticle.
- Palm creases and pads by moving loops, not by adding geometry, for stylised characters.
- Webbing between fingers: keep the edges between finger bases close so fingers do not look like separate sausages.

## Joining to the arm

Wrist loop count must match the forearm. Reduce from the hand's higher count with triangles or poles placed on the back of the hand, not on the palm.

## Gotchas

- Fingers modelled straight and parallel are hard to rig; pose them slightly curved and spread (relaxed pose).
- Too many loops on fingers multiply weight-painting work.

## Verify

Rig a quick finger chain and curl each finger fully at all knuckles: no collapsing knuckles; making a fist shows no intersections that topology could fix.

## Checked

2026-10-27, Blender manual 5.2 (blender-v5.2-release RST). Confirmed: Inset on I, Extrude Faces and mesh structure pages exist as cited. Removed: finger length ratios, the thumb angle, edge counts and the middle-finger proportion rule. The loop-flow guidance is modelling practice from experience and is not stated in the manual; the numeric counts, ratios and angles that no documentation covers were removed.

Method: documentation only; no commands were run.
