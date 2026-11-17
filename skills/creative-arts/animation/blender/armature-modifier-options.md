---
id: creative-arts.animation.blender.armature-modifier-options
name: armature-modifier-options
category: creative-arts
field: animation
product: blender
tags: [blender, armature-modifier, rigging, skinning, preserve-volume, multi-modifier, envelopes]
level: practitioner
status: docs-checked
description: "Blender's Armature modifier options: Object, Vertex Group, Preserve Volume, Multi Modifier and Bind To (Vertex Groups, Bone Envelopes), and how to blend two armature results."
sources:
  - https://docs.blender.org/manual/en/latest/modeling/modifiers/deform/armature.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# armature-modifier-options

## Options

- **Object**: the armature object used by the modifier. Parenting an object to an armature quickly adds the modifier.
- **Vertex Group** (+ Invert): its weights set the influence of this modifier's result when mixed with other Armature modifiers. Only meaningful with at least two Armature modifiers on the object and *Multi Modifier* enabled.
- **Preserve Volume**: uses quaternions. Without it, rotations at joints scale neighbouring geometry down, up to nearly zero at 180 degrees from rest. With it, geometry is not scaled down, but there is a gap (discontinuity) when passing 180 degrees from rest.
- **Multi Modifier**: uses the same input data as a previous modifier (usually also an Armature one), so several armatures can deform the same object from the non-deformed data instead of the second deforming the first's result. Results are mixed using the Vertex Group weights.
- **Bind To**:
  - *Vertex Groups* (meshes and lattices only): a bone deforms vertices in the vertex group of the same name, with strength by weight. More precise than envelopes but slower to set up.
  - *Bone Envelopes*: bones deform vertices or control points near them, by each bone's envelope radius and distance.

## Dependencies tip

With envelopes disabled, Blender uses the existing vertex group names to decide which bones are needed to evaluate the modifier. Removing empty vertex groups reduces dependencies, which can matter when the mesh is used while evaluating other bones in the same armature (for example as a Shrinkwrap constraint target).

## Verify

Twist a joint 90 to 180 degrees and compare Preserve Volume on and off; for mixed setups paint the Vertex Group on the second modifier and confirm the blend per region.

## Checked

Date: 2026-10-27. Documentation release: Blender manual, 5.2 release branch (Armature modifier page). Confirmed: all options above and their stated behaviour. Corrected: Preserve Volume does not "cause bulging at bends" per the manual (its trade-off is a discontinuity at 180 degrees); the Vertex Group is for mixing, not general influence limiting. Removed unconfirmed stack-order, export and game-engine claims.
Method: documentation only; no commands were run.
