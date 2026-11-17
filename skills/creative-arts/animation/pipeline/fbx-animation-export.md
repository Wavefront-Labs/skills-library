---
id: creative-arts.animation.pipeline.fbx-animation-export
name: fbx-animation-export
category: creative-arts
field: animation
product: pipeline
tags: [fbx, interchange-formats, skeletal-animation, bake-animation, game-engine-export, unreal, unity, blender-fbx, maya-fbx, takes]
level: advanced
status: draft
description: "Export skeletal animation and rigs as FBX for engines and other DCCs: baking, deformation-only skeletons, scale/axis, takes/clips, and checking imports."
sources:
  - https://help.autodesk.com/view/MAYAUL/2025/ENU/
  - https://dev.epicgames.com/documentation/en-us/unreal-engine/fbx-animation-pipeline-in-unreal-engine
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# FBX animation export

**Goal:** a character's animation arrives in Unreal/Unity/another DCC playing exactly as animated, on a skeleton
the receiving side accepts.

## Prepare

- Export a **deformation skeleton** only (joints that skin the mesh), not controls, IK handles or constraint
  helpers. Many rigs have a separate export skeleton driven by the control rig.
- **Bake animation** to the export joints (every frame, or keys only where needed): constraints and IK do not
  transfer.
- Single root joint at origin; root motion on the root (or none) per the engine's convention.
- Mesh with skin weights, max influences per vertex (4 or 8 for engines), frozen transforms.

## Maya FBX settings (FBX Export options)

Animation: Bake Animation on, start/end, step 1; Deformed Models: Skins, Blend Shapes; Constraints off;
Units: centimetres (Unreal expects cm); Axis: Y-up (Unreal converts); FBX version matching the importer.

## Blender FBX settings

Apply Scalings: "FBX Units Scale"; Forward -Y / Up Z defaults work for many engines, but Unreal often wants
Forward X; Armature: "Only Deform Bones", uncheck "Add Leaf Bones"; Bake Animation on, "NLA Strips"/"All
Actions" to export clips.

## Clips/takes

One FBX per clip (common for engines), or several takes in one file (Maya time editor/clips, Blender actions).
Name clips the way the engine's import expects (`hero_walk_fwd`).

## Gotchas

- Scale 100x off (cm vs m) is the classic error: fix units on export, not by scaling in the engine.
- Euler flips from baking: run a Euler filter before export.
- Blend shapes require consistent topology and name matching on the engine side.
- Leaf bones and extra root nodes ("Armature") from Blender confuse skeleton retargeting in engines.

## Verify

Import into the target with the intended settings; play the clip next to a playblast: same poses at the same
frames, no scale/axis issues, skeleton hierarchy as expected.
