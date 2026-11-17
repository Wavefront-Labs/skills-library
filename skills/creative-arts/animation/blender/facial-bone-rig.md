---
id: creative-arts.animation.blender.facial-bone-rig
name: facial-bone-rig
category: creative-arts
field: animation
product: blender
tags: [blender, facial-rig, facial-bone-rig, face-bones, jaw-rig, eye-rig, bendy-bones]
level: advanced
status: docs-checked
description: "Build a bone-based face rig in Blender: jaw, eyes with aim targets, eyelids, lips with bendy bones, brows and cheeks, weighting and correctives."
sources:
  - https://docs.blender.org/manual/en/latest/animation/armatures/bones/properties/bendy_bones.html
  - https://docs.blender.org/manual/en/latest/animation/constraints/tracking/damped_track.html
  - https://docs.blender.org/manual/en/latest/animation/armatures/skinning/index.html
  - https://docs.blender.org/manual/en/latest/files/import_export/usd.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# facial-bone-rig

Goal: a deformation-bone face that works with game export and layered controls.

## Core bones (parented under head)
- **Jaw**: pivot just below/in front of the ear; rotate X opens. Lower teeth/tongue parent to it.
- **Eyes**: one bone per eye at eyeball centre, **Damped Track** to an `eye_target.L/R` parented to a master `eyes_target` (in front of the face, switchable parent: head/world).
- **Eyelids**: upper/lower lid bones rotating from eye centre; drive part of lid rotation from eye rotation (driver; a factor around 0.2-0.3 is a practice starting value) for fleshy eyes.
- **Lips**: corner, upper and lower mid bones; a **B-Bone** chain (increase *Segments* in the Bendy Bones panel and assign the corner bones as the *Start/End Handle* under Custom Handles) for smooth lip curves. The segment count is a practice choice; start low and raise it only if the curve looks faceted.
- **Brows**: 3 per side (inner, mid, outer); **Cheeks**, **nose** (sneer), **chin**.

## Controls layer
Deform bones driven by control bones (Copy Transforms or parenting) so animators never key DEF bones; MCH bones handle jaw follow for lip corners (Copy Rotation from the jaw at partial influence, for example 0.5 as a practice value).

## Weighting
Start with Automatic Weights, then paint: lips and lids need clean separation (mouth must open without pulling upper lip). Lock head/neck groups while painting.

## Correctives
Shape keys driven by jaw rotation (open jaw corrective) and lid rotation for volume preservation.

## Gotchas
- Jaw pivot wrong -> chin slides instead of rotates; check from the side.
- Eye bones not exactly centred in the eyeball -> eyes swim out of the socket.
- Bendy-bone shape is not carried by every exporter (the USD exporter documents that bendy bones are not supported), so check the exporter's documentation; for game targets bake the B-Bone channels (Bake Action can bake the B-Bone channel type) or use more discrete bones.

## Verify
Expression test animation: jaw open, smile, blink, look around - no intersections, eyes stay in sockets.

## Checked

2026-10-27. Documentation release: Blender manual 5.2 (branch blender-v5.2-release). Confirmed: Bendy Bones Segments and Custom Handles Start/End Handle (animation/armatures/bones/properties/bendy_bones.rst); Damped Track constraint exists (damped_track.rst); the USD exporter states bendy bones are not supported (files/import_export/usd.rst); Bake Action channel types include B-Bone (API reference for bpy.ops.nla.bake). Wrong in the old text: the blanket claim that B-bone lips export poorly because engines lack support is not documented; replaced with exporter-specific advice. Marked segment counts and driver and influence factors as practice values; no numeric rig value here comes from documentation.

Method: documentation only; no commands were run.
