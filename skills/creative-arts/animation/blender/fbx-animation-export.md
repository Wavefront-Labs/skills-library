---
id: creative-arts.animation.blender.fbx-animation-export
name: fbx-animation-export
category: creative-arts
field: animation
product: blender
tags: [blender, fbx, fbx-animation-export, fbx-unity, fbx-unreal, fbx-armature-export, export-nla-strips, fbx-actions, game-export, bake-animation, unity, unreal]
level: practitioner
status: verified
description: "Export character animation from Blender to FBX for Unity/Unreal: Bake Animation options, All Actions vs NLA Strips, key all bones, simplify, leaf bones, axis/scale, frame ranges."
sources:
  - https://docs.blender.org/manual/en/latest/files/import_export/fbx_legacy.html
  - https://docs.blender.org/manual/en/latest/files/import_export/fbx.html
  - https://projects.blender.org/blender/blender/src/branch/blender-v5.2-release/scripts/addons_core/io_scene_fbx/__init__.py
licence: Apache-2.0
version: 5
updated: 2026-11-17
aliases: []
---

# fbx-animation-export

Goal: every clip arrives in the engine as a correctly named take, at the right scale, without drift or missing bones. Mesh/rig export settings are in `import-export-formats`.

## Exporter settings (File > Export > FBX (.fbx), the FBX add-on's exporter)

- **Object Types**: Armature + Mesh (or Armature only for animation-only files).
- **Transform**: Scale 1.0 (the default), **Apply Unit** on (default), and **Apply Scalings** chosen to suit the target (the options are All Local, FBX Units Scale, FBX Custom Scale and FBX All; the tooltip notes Blender uses FBX scale to detect units on import but many other applications do not). Leave **Apply Transform** off for armatures and animation: its own description says it is experimental and known to be broken with armatures/animations. Forward -Z / Up Y are the exporter's defaults; confirm the axes your engine's importer expects. If the rig imports 100x too big or small, the scene Unit Scale or Apply Scalings is the likely cause (practice).
- **Armature**: **Add Leaf Bones** is ON by default — turn it OFF if you do not want the extra end bone on each chain; **Only Deform Bones** (default off) writes only deforming bones and non-deforming ones with deforming children, useful for Rigify-style rigs; Primary/Secondary Bone Axis default to Y and X; **Armature FBXNode Type** defaults to Null (use it unless the other application has issues).
- **Baked Animation** ON (default):
  - **Key All Bones** (default on): forces at least one key for every bone.
  - **NLA Strips** (default on): each non-muted NLA strip is exported as a separate FBX AnimStack (take).
  - **All Actions** (default on): each action is exported as a separate AnimStack instead of the global scene animation; the manual notes that with it off only the currently assigned action is exported (in a 4.5.14 run with NLA Strips on and All Actions off, only the NLA strip take was written and the assigned action was not, so check the takes after exporting).
  - **Force Start/End Keying** (default on): always adds a key at the start and end of actions for animated channels.
  - **Sampling Rate** 1.0 frames (default); **Simplify** 1.0 by default, 0.0 disables simplification (the higher the more simplified), so use 0 for exact keys.

## Clip hygiene

- Actions named `Hero_Walk`; each with a Manual Frame Range set (Action properties) so takes have the intended length — the exporter reads each action's `frame_range`, which uses the manual range when one is set.
- Root motion: keep or strip at the root bone consistently (see `root-motion`).
- Constraints are not saved in the FBX; their result is exported as keyframe animation (manual, Compatibility > Export).

## Gotchas

- Armature object scale not 1 → scaled bones in engine; apply scale before animating, or Apply Scalings.
- The armature object is written as an FBX node (Armature FBXNode Type); if the target application shows an extra root node, try the other node types or rename the armature object to what your pipeline expects (practice).
- Shape key animation is written by the exporter's baked animation path; verify it in a re-import (the manual's Compatibility list is out of date on shape keys).

## Verify

Import the FBX back into a clean Blender scene: takes listed as actions, correct length, no extra leaf bones; engine preview plays each clip without foot drift.

## Checked

2026-10-27. Documentation release: Blender manual 5.2 (branch blender-v5.2-release) plus the FBX add-on source (io_scene_fbx __init__.py and export_fbx_bin.py, same branch), which holds the property names and defaults because the manual's export sections are marked todo. Confirmed from source: Scale 1.0, Apply Unit on, Apply Scalings options, Apply Transform described as experimental and broken with armatures/animations, Forward -Z / Up Y defaults, Add Leaf Bones default on, Only Deform Bones default off, Armature FBXNode Type default Null, Baked Animation, Key All Bones, NLA Strips, All Actions and Force Start/End Keying default on, Sampling Rate 1.0, Simplify 1.0 (0 disables), and that action frame_range (manual range when set) is used. Manual: constraints are exported as keyframes, All Actions off exports only the assigned action. Wrong in the old text: advising Apply Transform on for Unity, and the claim that leaf bones are off by default. Removed the Shape Keys-enabled and Mixamo root-node claims.

Run check, 2026-11-01, Blender 4.5.14 LTS headless (bpy, factory settings): operator defaults of export_scene.fbx: global_scale 1.0, apply_unit_scale on, apply_scale_options FBX_SCALE_NONE/UNITS/CUSTOM/ALL, bake_space_transform off, axis_forward -Z, axis_up Y, primary_bone_axis Y, secondary_bone_axis X, armature_nodetype NULL (also ROOT, LIMBNODE), add_leaf_bones on, use_armature_deform_only off, bake_anim, bake_anim_use_all_bones, bake_anim_use_nla_strips, bake_anim_use_all_actions and bake_anim_force_startend_keying on, bake_anim_step 1.0, bake_anim_simplify_factor 1.0. Exported a two-bone rig with two actions, an NLA strip and a shape key, and re-imported it: with defaults the bones were Bone, Bone2 and a leaf bone Bone2_end; with add_leaf_bones off the leaf bone was gone; with NLA Strips off and All Actions on each action became a take (Hero_Walk, Hero_Run); with NLA Strips on and All Actions off only the strip take (RunStrip) appeared; with bake_anim off no actions were written; the shape key animation also arrived as actions. Not run (confirmed from the manual and add-on source only): Apply Transform effects on armatures, scale in a real engine, constraints baked to keys, frame_range use, root motion.

Method: manual text confirmed from documentation; the listed behaviour run headless in Blender 4.5.14.
