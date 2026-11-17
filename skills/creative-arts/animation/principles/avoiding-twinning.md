---
id: creative-arts.animation.principles.avoiding-twinning
name: avoiding-twinning
category: creative-arts
field: animation
product: principles
tags: [animation, solid-drawing, twinning, asymmetry, posing, symmetry, natural-poses, cg, mirroring]
level: intro
status: draft
description: "Spot and fix twinning (both sides of the body mirroring each other in pose or timing) in drawings and CG, where mirror tools make it a constant risk."
sources:
  - https://books.google.com/books?vid=ISBN9780786860708
  - https://en.wikipedia.org/wiki/Twelve_basic_principles_of_animation
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Avoiding twinning

Goal: no pose or motion where left and right sides are identical. Thomas and Johnston list
twinning as a solid-drawing fault: it makes characters look stiff and lifeless.

## Where twinning appears
- **Pose**: both arms at the same angle, both hands on hips identically, both feet level and
  parallel, both brows raised equally.
- **Timing**: both arms moving in sync, both eyes blinking on the same frame in a close-up,
  both hands arriving at the same frame.
- **Camera**: a perfectly frontal view that makes the body symmetrical.

## Fixes
1. Shift weight to one leg (contrapposto): hips tilt, shoulders tilt opposite.
2. Offset arm angles and heights; one hand open, the other relaxed or holding something.
3. Tilt the head; break symmetry in the brows and mouth corners.
4. Offset timing by 1-3 frames between left and right parts.
5. Move the camera off-axis to three-quarter.

## CG specifics
- Mirror pose tools (Blender: Copy Pose / Paste X-Flipped Pose; Maya: mirror pose scripts) and
  symmetric rigs encourage twinning. After mirroring, always offset and adjust.
- Symmetrical facial controls: break the default symmetric blendshape with per-side adjustments.

## When symmetry is right
Deliberate: military attention, a robot, a formal or comic "stiff" pose, or a graphic
symmetrical composition. Mark it as intentional.

## Verify
- [ ] Mirror-check: flip the frame; it should look different.
- [ ] Left and right limbs differ in angle or timing on every key.
- [ ] Symmetric poses, if any, are marked intentional.

Related: `creative-arts.animation.character-design.character-design-craft`,
`creative-arts.animation.principles.form-construction`.
