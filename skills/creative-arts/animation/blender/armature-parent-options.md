---
id: creative-arts.animation.blender.armature-parent-options
name: armature-parent-options
category: creative-arts
field: animation
product: blender
tags: [blender, rigging, skinning, envelope-weights, with-envelope-weights, empty-groups, with-empty-groups, deform-bones-only, selected-bones-weights]
level: practitioner
status: docs-checked
description: "Choose how to bind a mesh to a Blender armature: Ctrl P with Empty Groups, Envelope Weights or Automatic Weights, plus Assign Automatic from Bones for selected/deform bones only."
sources:
  - https://docs.blender.org/manual/en/5.2/animation/armatures/skinning/parenting.html
  - https://docs.blender.org/manual/en/5.2/sculpt_paint/weight_paint/editing.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# armature-parent-options

## Ctrl P (child meshes selected, armature active) options

- **Armature Deform** sets the armature as parent and adds an Armature modifier on each child.
- **With Empty Groups**: creates empty vertex groups named after each *deform* bone (only bones with Deform enabled), for manual assignment; choose it when the vertex groups already exist and are weighted. Vertices are then assigned to a group by hand.
- **With Automatic Weights**: weights from the bone heat algorithm, based on the distance from vertices to bones; easy but can mis-assign on complex meshes and armatures, and then needs manual weight edits.
- **With Envelope Weights**: weights from the Bone Envelope settings (see `bone-deform-envelope`); calculated once, so re-parent after changing envelopes or geometry.

## Re-weighting subsets (Weights menu in Weight Paint and Edit Mode)

- **Assign Automatic from Bone** and **Assign from Bone Envelopes** apply the auto-weighting or envelope weights of the selected bone(s) to the selected vertex group. In the redo panel, the **Subset** option restricts a tool to Active Group, Selected Pose Bones, Deform Pose Bones or All Groups, so one limb can be redone without touching other groups.
- The tools also respect Vertex and Face Selection Masking.

## Rigid parts recipe (robots, props)

With Empty Groups, then in Edit Mode select each part's vertices and assign them to the bone's group at weight 1.0. No blending, no paint needed.

## Gotchas

- With Automatic or Envelope Weights, existing vertex groups with the same names as bones are completely overridden; use With Empty Groups to keep them.
- Control bones with Deform on get vertex groups too; turn Deform off first.

## Verify

Vertex groups list exactly the deform bones; pose test shows each part following the intended bone.

## Checked

2026-10-27, Blender 5.2 manual (blender-v5.2-release). Confirmed on the Armature Deform Parent and Editing Weight Paint pages: With Empty Groups, Automatic Weights, Envelope Weights behaviour, deform-bone-only groups, overwrite warning, Assign Automatic from Bone, Assign from Bone Envelopes and the Subset options. Corrected the "Selected bones only" option name; removed unconfirmed shortcut and modifier-order claims.

Method: documentation only; no commands were run.
