---
id: creative-arts.animation.blender.bone-deform-envelope
name: bone-deform-envelope
category: creative-arts
field: animation
product: blender
tags: [blender, rigging, bone-deform-settings, bone-envelope-settings, envelope-radius, envelope-distance, connected-bones, bone-head-tail, deform-bones]
level: practitioner
status: verified
description: "Configure Blender bone Deform settings: the Deform toggle, envelope distance, weight and multiply, head/tail radius, connected bones, and envelope weights on parenting."
sources:
  - https://docs.blender.org/manual/en/5.2/animation/armatures/bones/properties/deform.html
  - https://docs.blender.org/manual/en/5.2/animation/armatures/bones/properties/relations.html
  - https://docs.blender.org/manual/en/5.2/animation/armatures/bones/editing/transform.html
  - https://docs.blender.org/manual/en/5.2/animation/armatures/skinning/parenting.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# bone-deform-envelope

Goal: only the right bones deform the mesh, and envelope-based influence (when used) covers the intended volume.

## Deform toggle (Bone Properties > Deform)

- The panel header checkbox: off prevents the bone from deforming geometry at all, overriding any weights it has, and excludes the bone from automatic weight calculation when parenting with Armature Deform > With Automatic Weights. Turn it off for control bones (IK targets, poles, mechanism bones).

## Envelope settings (per bone)

- Envelopes work with meshes, lattices, curves, surfaces and texts. Each bone has an inner area (controlled by the root and tip radius) and an outer area (controlled by Distance).
- Bone API: `use_deform`, `envelope_distance` (new bone 0.25), `envelope_weight` (1.0), `use_envelope_multiply` (off), `head_radius` (0.1), `tail_radius` (0.05).
- **Envelope Distance**: the range within which the bone influences vertices; influence decays quadratically with distance.
- **Envelope Weight**: global influence of the bone under the envelope method; only matters where geometry is shared by several bones. 0.0 has the same effect as disabling Deform.
- **Envelope Multiply**: with both vertex groups and envelopes active, vertices in at least one vertex group are normally deformed only by the vertex groups and "orphan" vertices by envelopes; with Multiply, the envelope influence is multiplied with the vertex group weight.
- **Radius Head/Tail**: radius at each end; geometry inside is fully affected. Edit them in the Deform panel, or in Edit Mode with Scale Radius (Alt-S); Scale Envelope Distance is Shift-Ctrl-Alt-S. Resizing a bone also adjusts its end radii proportionally, so place bones first and edit properties after.
- Visualize with Armature > Viewport Display > Display As > **Envelope**.

## Head, tail, connected

- **Connected**: the child's head is connected to the parent's tail, so a connected bone cannot be moved on its own, only rotated. Use for FK chains; leave bones unconnected where they need to translate.
- **Set Roll** (Edit Mode, Ctrl-R) tweaks the roll of selected bones.

## When envelopes are useful

Quick proxy skinning for blocking rigs, mechanical parts, or as the starting point before painting weights (Parent with Envelope Weights converts envelopes to vertex groups — see `envelope-weights`).

## Gotchas

- Armature Deform With Envelope Weights is a one-off calculation: new envelope settings or newly included vertices are not picked up until you parent again. To use envelope settings live, enable Bone Envelopes on the Armature modifier (`use_bone_envelopes`, off by default; `use_vertex_groups` is on by default).
- With Automatic or Envelope Weights, existing vertex groups with the same names as the bones are overwritten.

## Verify

Envelope display shows capsules covering intended regions; Outliner/vertex groups list only deform bone names.

## Checked

2026-10-27, Blender 5.2 manual (blender-v5.2-release). Confirmed on the Bone Deform, Relations, Edit Mode Transform and Armature Deform Parent pages: Deform toggle behaviour, Envelope Distance, Weight, Multiply, Radius Head/Tail, Alt-S, Shift-Ctrl-Alt-S, Ctrl-R, one-off envelope weights and the Bone Envelopes modifier tip. Removed the unconfirmed Rigify convention, default-off claim for the modifier envelopes and double-transform remark.

Run check, 2026-11-01, Blender 4.5.14 LTS headless (bpy, factory settings): Bone properties use_deform, envelope_distance 0.25, envelope_weight 1.0, use_envelope_multiply False, head_radius 0.1, tail_radius 0.05, use_connect; Armature modifier use_bone_envelopes False and use_vertex_groups True; parent_set type enum includes ARMATURE_ENVELOPE, ARMATURE_AUTO, ARMATURE_NAME; Armature display_type has ENVELOPE. Not run (confirmed from the manual only): quadratic decay, shortcuts (Alt-S, Shift-Ctrl-Alt-S, Ctrl-R), the vertex-group overwrite and one-off envelope weight calculation.

Method: manual text and shipped UI scripts confirmed from documentation; the listed behaviour run headless in Blender 4.5.14.
