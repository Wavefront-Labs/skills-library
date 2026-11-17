---
id: creative-arts.animation.blender.gp-layer-parenting
name: gp-layer-parenting
category: creative-arts
field: animation
product: blender
tags: [blender, grease-pencil, gp-layer-parenting, gp-bone-parent, cutout-animation, layer-transform]
level: practitioner
status: docs-checked
description: "Parent Grease Pencil layers to objects and bones for cut-out rigs and camera-locked layers, and use per-layer transforms and adjustments."
sources:
  - https://docs.blender.org/manual/en/latest/grease_pencil/properties/layers.html
  - https://docs.blender.org/api/current/bpy.types.GreasePencilLayer.html
  - https://docs.blender.org/manual/en/latest/grease_pencil/modifiers/edit/time_offset.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# gp-layer-parenting

Goal: rigid parts (head, hands, props) follow bones or objects while still drawn as layers.

## Setup
Object Data > Layers > select the layer > **Relations** > **Parent**: pick a parent object. The layer inherits that object's transformations; the manual describes this as useful for cut-out rigging. When the parent is an armature, the layer's parent bone is stored in the `parent_bone` property (Python API: GreasePencilLayer.parent, parent_bone, matrix_parent_inverse), so choose the bone in the same panel.

## Typical cut-out rig
- One layer per rigid part: head, torso, arm and hand layers.
- An armature in the drawing plane; each layer parented to its bone.
- Animate the armature in Pose mode; swap drawings by keying layer frames, or use the Time Offset modifier (Fixed Frame) for mouth shapes.

## Camera-locked layers
Parent a layer to the camera object so it stays fixed in frame.

## Layer transform and adjustments
Layers have their own **Transform** (location, rotation, scale), Adjustments (Tint Color, Factor, Stroke Thickness) and a **View Layer** assignment for compositing.

## Gotchas
- Parenting after posing can make a layer jump: the parent inverse matrix exists on the layer (matrix_parent_inverse), so parent with the armature in its rest pose and check the result.
- Layer parenting is rigid. For bendy parts use vertex groups and the Armature modifier (see gp-weight-paint-armature).
- Bones not aligned with the drawing plane move the layer out of plane.

## Verify
Rotate the parent bone: the layer follows it; return to rest pose and the drawing returns to where it was drawn.

## Checked

2026-10-27, Blender 5.2 manual (projects.blender.org blender-manual, branch blender-v5.2-release RST) and Python API docs. Confirmed Relations > Parent, per-layer Transform and Adjustments in the Layers page, and parent, parent_bone and matrix_parent_inverse in the GreasePencilLayer API. Removed the unconfirmed Parent Type: Bone control name and the 4.3 version gate; the armature link source was replaced by the API page.
Method: documentation only; no commands were run.
