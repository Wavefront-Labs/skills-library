---
id: creative-arts.animation.blender.rigify-metarig-types
name: rigify-metarig-types
category: creative-arts
field: animation
product: blender
tags: [blender, rigify, rigify-metarig-types, rigify-quadruped, rigify-human, metarig]
level: practitioner
status: docs-checked
description: "Pick and fit the right Rigify metarig in Blender: Basic Human, Basic Quadruped, Human, Cat, Wolf, Horse, Shark, plus fitting bones to the mesh."
sources:
  - https://docs.blender.org/manual/en/latest/addons/rigify/basics.html
  - https://docs.blender.org/manual/en/latest/addons/rigify/bone_positioning.html
  - https://docs.blender.org/manual/en/latest/addons/rigify/introduction.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# rigify-metarig-types

Goal: start from the closest template so generation needs minimal custom work.

## Enable and add
Preferences > Add-ons: search "Rigify" and tick *Enable Add-on*. In Object Mode: Add > Armature (Shift-A) > pick a meta-rig. The predefined meta-rigs are:

| Metarig | Note |
|---|---|
| Basic Human | Biped without face and fingers |
| Basic Quadruped | Generic four-legged |
| Human | Full biped |
| Cat, Wolf, Horse | Specific quadrupeds |
| Shark | Fish-like |

For anything else, add a Single Bone and build from samples or rig types (see the rigify-rig-types skill).

## Fitting
1. Rigify assumes 1 unit = 1 metre, so a human is about 2 units tall. Scale the character to that size in Object Mode and apply scale (Apply Scale) before positioning the metarig.
2. Match bones to the mesh in Pose Mode (then Apply > Apply Pose As Rest Pose) or Edit Mode. Connected bones cannot be translated in Pose Mode.
3. Keep legs and spine straight in the front view, and give knees and elbows a slight bend: Rigify evaluates bone roll from the bend axis and needs to know which way the joint points. The last spine bone is the head; by default the two bones below it are the neck.
4. Finger rolls: select the finger bones and Recalculate Roll > Global -Z Axis (thumb often starts from Global +Y Axis); if fingers curl on the wrong axis, change Bend Rotation Axis under Rigify Type.
5. Face: all face bones are in the *Face* bone collection by default; delete them all if you do not need a face.

## Gotchas
- Rigify only builds controls and bones; it does not attach the rig to a mesh.
- Each sub-rig needs a required number of bones; add a sample to see the expected layout.

## Verify
Armature properties > **Generate Rig** succeeds; pose the IK legs and arms and check knees and elbows bend the expected way.

## Checked
Date: 2026-10-27. Documentation: Blender manual (Rigify), branch blender-v5.2-release. Confirmed: enabling steps, the list of predefined meta-rigs (Basic Human, Basic Quadruped, Human, Cat, Wolf, Horse, Shark), unit scale and Apply Scale advice, Pose Mode matching, bend-angle requirement, neck and head defaults, Face collection, and the roll-recalculation tips. Removed the Bird metarig (not in the manual list), the "unapplied scale breaks generation" claim and other unconfirmed gotchas.
Method: documentation only; no commands were run.
