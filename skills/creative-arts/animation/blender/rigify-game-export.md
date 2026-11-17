---
id: creative-arts.animation.blender.rigify-game-export
name: rigify-game-export
category: creative-arts
field: animation
product: blender
tags: [blender, rigify, rigify-game-export, rigify-deform-bones, game-rig, fbx-export, unreal, unity]
level: advanced
status: docs-checked
description: "Export Rigify characters to game engines: DEF bones, FBX Only Deform Bones and leaf bones, baking to a clean skeleton, and root bone notes."
sources:
  - https://docs.blender.org/manual/en/latest/addons/rigify/basics.html
  - https://docs.blender.org/manual/en/latest/addons/rigify/rig_features.html
  - https://projects.blender.org/blender/blender/src/branch/main/scripts/addons_core/io_scene_fbx/__init__.py
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# rigify-game-export

Goal: a clean deform skeleton with animation that Unity, Unreal or Godot import correctly.

## Problems with raw export
- The generated rig has many ORG, MCH and control bones; engines only need the deform bones (collection *DEF*).
- Rigify advises against significantly modifying a generated rig, so do clean-up on a copy and keep the metarig for regeneration.
- Every Rigify rig has a `root` bone that parents all bones of the rig.

## Approach A: FBX export of deform bones
In the FBX export operator (File > Export > FBX), Armature section: **Only Deform Bones** writes deforming bones and also non-deforming bones that have deforming children, so intermediate parents are kept. **Add Leaf Bones** appends an extra end bone to each chain and is on by default; turn it off for engines that do not want them. **Primary Bone Axis** / **Secondary Bone Axis** default to Y and X. Enable **Baked Animation** to write keyframes. Check the exported hierarchy by reimporting.

## Approach B: separate game skeleton
1. Duplicate the generated rig; delete non-DEF bones you do not want and re-parent the DEF bones into the tree your engine expects.
2. Add Copy Transforms constraints from each game bone to the matching DEF bone of the control rig.
3. Bake the action (Object/Pose Animation menu > Bake Action, visual keying) onto the game skeleton, then export the skeleton and mesh.

## Scale
The FBX exporter has **Scale**, **Apply Unit** and **Apply Scalings** (All Local, FBX Units Scale, FBX Custom Scale, FBX All). Which combination matches an engine depends on the engine; check the engine's import documentation and test with a one-bone object of known size.

## Gotchas
- Leaf bones add `_end` bones if left on.
- Rigify rigs rely on B-Bones and stretch mechanisms; most engines read plain bones, so bake the result to a plain skeleton.

## Verify
Reimport the FBX into an empty Blender scene and into the engine: bone count as expected, animation plays with no flipping.

## Checked
Date: 2026-10-27. Documentation: Blender manual (Rigify), branch blender-v5.2-release, and the FBX exporter source (io_scene_fbx) on the Blender main branch. Confirmed: DEF collection, root bone, advice not to modify generated rigs, the FBX export option names and defaults (Only Deform Bones keeps non-deforming parents of deforming bones, Add Leaf Bones default on, axes Y and X, Baked Animation, Scale, Apply Unit, Apply Scalings values), and the Bake Action menu entry. Removed unconfirmed engine-specific claims (Unreal axis and unit settings, Unity Humanoid mapping, third-party game-rig add-ons) and the claim that deform-only export breaks parenting, which the exporter description contradicts.
Method: documentation only; no commands were run.
