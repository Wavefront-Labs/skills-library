---
id: creative-arts.animation.blender.mouth-interior
name: mouth-interior
category: creative-arts
field: animation
product: blender
tags: [blender, mouth-interior, teeth-modeling, tongue, mouth-bag, character-modeling, facial-rig]
level: practitioner
status: docs-checked
description: "Build the inside of a character's mouth: mouth bag from the inner lip, teeth and gums as separate objects, tongue with bones, parenting to jaw and avoiding clipping."
sources:
  - https://docs.blender.org/manual/en/latest/modeling/meshes/editing/face/extrude_faces.html
  - https://docs.blender.org/manual/en/latest/animation/armatures/skinning/parenting.html
  - https://docs.blender.org/manual/en/latest/scene_layout/object/editing/parent.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# mouth-interior

Goal: open-mouth shots that look right: dark cavity, teeth that move with the jaw, tongue that can be animated.

## Mouth bag

1. From the inner lip edge loop, extrude inward a few times to form a pocket reaching back toward the throat (it stays part of the head mesh).
2. Shape it wider than the lips, closed at the back; add a darker material (vertex colour or separate material) inside so it reads as shadow.
3. Weight the lower half to the jaw bone, upper half to the head.

## Teeth and gums

- Separate objects: upper teeth + upper gum, lower teeth + lower gum. Model one tooth type per shape (incisor, canine, molar), duplicate along a curve with Array + Curve modifiers or place by hand.
- Parent upper set to the head bone, lower set to the jaw bone (`Ctrl P → Bone`), no skinning needed.
- Stylised characters: a single strip of teeth with a few cuts often reads better than individual teeth.

## Tongue

Separate object with a handful of loops along its length, rigged with a short bone chain parented to the jaw; weights from Automatic Weights, then smoothed.

## Avoiding clipping

- Animate the jaw open and check teeth do not poke through lips; adjust bag shape and lip corners.
- Use a corrective shape key on lips for wide open if needed.

## Gotchas

- Mouth bag not parented to the jaw stretches badly when the jaw opens.
- Subdivision on the head can shrink the inner lips away from the teeth; check with subdivision on.

## Verify

With the jaw open: teeth move with the jaw, the cavity is dark with no holes to the back of the head, tongue poses (up, out) are possible without penetrating the teeth.

## Checked

2026-10-27, Blender manual 5.2 (blender-v5.2-release RST). Confirmed: Ctrl P offers Bone parenting (child follows one bone) and armature parenting With Automatic Weights; Extrude Faces page exists. Removed: loop and bone counts, the jaw angle and the teeth-flicker claim. The loop-flow guidance is modelling practice from experience and is not stated in the manual; the numeric counts, ratios and angles that no documentation covers were removed.

Method: documentation only; no commands were run.
