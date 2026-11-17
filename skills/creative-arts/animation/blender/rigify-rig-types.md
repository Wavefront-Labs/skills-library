---
id: creative-arts.animation.blender.rigify-rig-types
name: rigify-rig-types
category: creative-arts
field: animation
product: blender
tags: [blender, rigify, rigify-rig-types, rigify-samples, rigify-bone-type, custom-metarig]
level: practitioner
status: docs-checked
description: "Assign Rigify rig types per bone (limbs, spines, basic copies, tentacles, skin) and add sample chains to build custom metarigs."
sources:
  - https://docs.blender.org/manual/en/latest/addons/rigify/metarigs.html
  - https://docs.blender.org/manual/en/latest/addons/rigify/rig_types/limbs.html
  - https://docs.blender.org/manual/en/latest/addons/rigify/rig_types/spines.html
  - https://docs.blender.org/manual/en/latest/addons/rigify/rig_types/basic.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# rigify-rig-types

Goal: build metarigs for any creature or prop by marking chain roots with the right rig type.

## How it works
A meta-rig is an assembly of bone chains; a chain is a run of *Connected* bones. Chains join by parenting without Connect (Keep Offset). The first bone of each chain carries the Rigify type property, and Rigify processes each chain from first to last bone.

## Where
Pose Mode, select a bone > Bone properties > **Rigify Type** panel: a rig type dropdown (filterable by feature set) with the options below it.

## Useful types
| Type | For |
|---|---|
| limbs.arm (3 connected bones) / limbs.leg (4 connected bones plus an unconnected heel child) / limbs.paw, front_paw, rear_paw | IK/FK limbs |
| limbs.super_finger | Finger with a master control that bends all joints through its scale |
| limbs.simple_tentacle / limbs.spline_tentacle | Tentacles, tails, antennae |
| spines.super_spine (wraps basic_spine, super_head and basic_tail) / spines.basic_spine / spines.super_head / spines.basic_tail | Torso, head with follow controls, tail |
| basic.super_copy | Single bone copy with optional control, widget and deform |
| basic.raw_copy | Copies the bone without the ORG- prefix, for fully custom rigging |
| basic.copy_chain | Copies a chain of at least two connected bones |
| basic.pivot | Custom pivot control for its child sub-rigs |
| skin.*, face.skin_eye, face.skin_jaw, face.basic_tongue | Modular face and skin rigs |

Single-bone types (the basic.* single-bone rigs) must be applied to every bone, even inside a connected chain. Chain-based types consume the whole connected chain.

## Samples
In Armature Edit Mode: Armature properties > **Rigify** panel > pick a sample in the list > **Add sample**; then position the bones. Samples show how each type is meant to be used.

## Options matter
- Limbs: Limb Segments, B-Bone Segments, Rotation Axis (Automatic, X, Z), plus Assign FK/Tweak Layers options that reference bone collections.
- super_copy: Control, Widget Type, Deform, and Relink Constraints (constraint name prefixes `CTRL:` and `DEF:` move constraints to the control or deform bone).
- raw_copy Relink Constraints: add `@bone_name` to a constraint name to retarget it to a generated bone.
- A bone named `root` with no parent and type raw_copy (or none) becomes the rig's root control.

## Gotchas
- Each sub-rig needs its required bone count; add a sample to see it.
- Preserved metarig bone properties (parenting, bendy bone settings, rotation mode, custom properties, custom widget) are copied to generated bones in a pattern that depends on the sub-rig.

## Verify
Generate Rig; each chain produces its expected controls.

## Checked
Date: 2026-10-27. Documentation: Blender manual (Rigify, Creating Meta-rigs and Rig Types pages), branch blender-v5.2-release. Confirmed: rig type ids and requirements, Rigify Type panel location, the Add sample workflow (Armature properties, not Shift-A), option names for limbs, basic and spines, Relink Constraints syntax, custom root bone rule. Removed Shift-A sample menu claim, `basic.super_copy` "jaw, eyelid" examples, and unconfirmed version-rename note.
Method: documentation only; no commands were run.
