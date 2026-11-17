---
id: creative-arts.animation.blender.animation-cleanup-baking
name: animation-cleanup-baking
category: creative-arts
field: animation
product: blender
tags: [blender, bake-action, animation-baking, key-cleanup, clean-keyframes, animation-export, decimate-keys, visual-keying, clear-constraints, nla-bake, euler-filter, export-prep, game-animation]
level: advanced
status: docs-checked
description: "Prepare Blender animation for export: Bake Action (visual keying, constraints, NLA), cleaning and decimating keys, Euler filter, deform-bone bake, pre-export checklist."
sources:
  - https://docs.blender.org/manual/en/latest/editors/nla/editing/strip.html
  - https://docs.blender.org/manual/en/latest/editors/graph_editor/fcurves/editing.html
  - https://docs.blender.org/manual/en/latest/editors/graph_editor/channels/editing.html
  - https://docs.blender.org/manual/en/latest/animation/actions.html
  - https://docs.blender.org/manual/en/latest/animation/armatures/posing/editing/apply.html
  - https://docs.blender.org/api/current/bpy.ops.nla.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# animation-cleanup-baking

Goal: turn whatever produced the motion (constraints, drivers, NLA layers, IK, mocap) into clean, portable keys on the bones/objects the destination understands.

## Bake Action (`Object → Animation → Bake Action...` in the 3D Viewport header, Object and Pose modes)

The final motion depends on keyframes plus F-curve modifiers, drivers and constraints; Bake Action computes it and creates a key on every scene frame. Options:
- **Start Frame / End Frame**, **Frame Step** (practice: 1 for export).
- **Only Selected Bones** (pose baking only).
- **Visual Keying**: keyframe from the final transformations (constraints applied). Practice: required for anything constraint-driven.
- **Clear Constraints**: removes all constraints from the keyed objects/bones and does visual keying (practice: do this on a *copy* of the rig for export, not the master file).
- **Clear Parents**: bakes the animation onto the object then clears parents (objects only).
- **Overwrite Current Action** (bake into the current action instead of creating a new one; useful for baking only some bones) and **Clean Curves** (removes redundant keys afterwards).
- **Bake Data**: Pose or Object. **Channels**: Location, Rotation, Scale, B-Bone, Custom Properties; pick only what you need.
Result: a key on every frame on every baked channel. Baked actions are heavy but unambiguous.

In the **NLA editor** the same operator is `Strip → Bake Action`; practice: use it to flatten layered animation into one action before export.

One-frame snapshot instead of a bake: `Pose → Apply → Visual Transform to Pose` (Pose Mode, the Apply menu is `Ctrl A`) converts the constrained position, rotation and scale into regular pose transforms so constraints can be removed while keeping the visual result; the manual lists baking constrained poses and preparing rigs for export as uses.

## Rig → deform-skeleton bake (game export)

Control rigs (Rigify, custom) have many non-deform bones. Rigify puts all deforming bones in the *DEF* bone collection, with `ORG-`, `MCH-` and `DEF-` name prefixes. Engines usually want only the deform set (practice):
1. Duplicate the armature; deform bones may have constraints pointing at control bones (Rigify DEF bones are driven through constraints), so bake before removing anything.
2. Select all deform bones (the DEF bone collection, or `Select → Select Pattern...` `DEF-*`), then `Object → Animation → Bake Action...` with *Visual Keying*, *Clear Constraints*, *Only Selected Bones*, *Bake Data: Pose*.
3. Delete the non-deform bones (Edit Mode, `Select Pattern` on `MCH-*`, `ORG-*`, or a script selecting bones with `use_deform == False`) and re-parent deform bones sensibly, or use an export add-on.
4. Check the exporter's deform-bones-only option as a safety net.
Script core (operator signature checked against the Python API: `bpy.ops.nla.bake(frame_start, frame_end, step, only_selected, visual_keying, clear_constraints, clear_parents, use_current_action, clean_curves, bake_types, channel_types)`):
```python
bpy.ops.pose.select_all(action='DESELECT')
for b in arm.pose.bones:
    b.bone.select = b.bone.use_deform
bpy.ops.nla.bake(frame_start=s, frame_end=e, only_selected=True, visual_keying=True,
                 clear_constraints=True, bake_types={'POSE'}, channel_types={'LOCATION','ROTATION','SCALE'})
```

## Cleaning keys (Graph Editor)

- **Clean Keyframes** (`Key → Density → Clean Keyframes`): deletes keys that have the same value as their neighbours, even if the segments around them are not flat. *Threshold* also removes keys that almost match; *Channels* cleans all keys in the selected curves (even unselected ones) and deletes a curve left with one key. The manual notes it is likely to change curve shape, so run it after bulk keying or baking and before hand-tweaking.
- **Decimate** (`Key → Density → Decimate (Ratio)` or `Decimate (Allowed Change)`): removes the keys that influence the shape least. Ratio mode has a *Remove* percentage; Error Margin mode removes as many keys as possible within a *Max Error Margin*. Use it to reduce mocap/baked data to editable keys.
- **Smoothing** (`Key → Smooth`): *Smooth (Gaussian)* (a Gaussian kernel; click the menu item and move the mouse), *Smooth (Legacy)*, and *Butterworth Smooth* (practice: the mocap de-noiser). The interactive blend operators (Breakdown, Blend to Neighbor, Blend to Default Value, Ease, Push Pull, Scale Average, Shear Keys, Time Offset, Match Slope) are in `Key → Blend`.
- **Discontinuity (Euler) Filter** (`Channel → Discontinuity (Euler) Filter`) cleans up Euler rotation channels that suffer from gimbal lock; all three Euler channels must be selected. Practice: prefer quaternion rotation for export.
- **Baking curves**: `Key → Density → Bake Keyframes` (`Shift Alt O`) creates a key at every frame; `Channel → Bake Channels` has Frame Range, Frame Step, Remove Outside Range, Interpolation Type and **Bake Modifiers** (new keys follow the modified curve and the modifiers are deleted).
- **F-curve modifiers** (Cycles, Noise): practice is to bake them into keys before export, since exporters may not evaluate them; use Bake Channels with *Bake Modifiers*, or Bake Action.
- **Channel cleanup:** delete unused channels (for example Scale curves on bones that never scale); `Channel → Revive Disabled F-Curves` fixes disabled (red) curves; `Channel → Un/Group Channels` groups by bone.

## Timing and range

- Trim the action to the export range. In the Dope Sheet or NLA sidebar set the action's **Manual Frame Range** (the range is used by some tools, shown as hashed fill, and can be used by exporters to decide which frames to export; it does not affect animation evaluation).
- The action's **Cyclic Animation** option states intent for a loop: the first and last frames of the range should be the same pose one loop apart, so the range includes the duplicated initial key; it does not make the action cycle by itself. Practice: whether the engine wants the duplicate last frame depends on the engine's loop convention, so check its docs.
- Root motion (practice): bake the root bone's location from the hip/centre of mass via a Copy Location constraint plus bake, or zero it for in-place animations.

## Shape keys and drivers

Driven shape keys (correctives) do not export as animation unless baked. Practice: script it by iterating frames, reading each `key_block.value` and calling `key_block.keyframe_insert("value")`, then remove the drivers; check each exporter's own documentation for what it evaluates.

## Pre-export checklist

1. Fresh file, append or link the character; apply transforms on armature + meshes (scale 1).
2. Bake Action (visual, NLA flattened) → Clean Keyframes → Euler filter on any Euler channels.
3. Delete non-deform bones or export deform bones only; check the deform bone count, hierarchy and names match the engine skeleton (for retargeting).
4. Set the Manual Frame Range; name the action `Walk`, `Idle` (ASCII, practice).
5. Limit vertex-group influences per vertex to what the engine supports (`Object → Clean Up → Limit Total Vertex Groups`) and normalise weights.
6. Export; re-import into a clean Blender to spot-check.

## Gotchas

- Baking without *Visual Keying* on a bone with constraints bakes its *local* keys, so the constraint effect vanishes when you clear it.
- Baking **every bone** on a Rigify rig creates thousands of curves; select deform bones first.
- *Clean Keyframes* judges keys by value against neighbours, so on stepped/constant-interpolated animation it can delete keys that matter (holds); practice: use it on Bezier/linear curves.
- The Euler filter needs X, Y and Z curves of the same bone selected together.
- Practice: purge unused actions before publishing so you do not ship both the original and the baked action.

## Verify

- Scrub the baked action with constraints cleared: motion identical to the original (compare with a duplicate scene or a Motion Path).
- Graph Editor shows no red (disabled) channels and no 360° jumps, and the key count after Clean is far lower than after the bake.
- The exported file re-imported into a fresh file plays the same clip with deform bones only.
- Engine import shows the right clip length (frames at the scene fps) and loops without a hitch.

## Checked

Date: 2026-10-27. Documentation release: Blender 5.2 manual (blender-v5.2-release RST) and the current Python API docs.
Confirmed: Bake Action location (Object > Animation > Bake Action... in Object and Pose modes; Strip > Bake Action in the NLA) and all dialog options; `bpy.ops.nla.bake` signature; Visual Transform to Pose under Pose > Apply (`Ctrl A`); Rigify DEF bone collection and prefixes; Clean Keyframes, Decimate, Bake Keyframes (`Shift Alt O`), Smooth (Gaussian/Legacy), Butterworth Smooth under Key; Euler filter, Bake Channels, Revive Disabled F-Curves, Un/Group Channels under Channel; Manual Frame Range and Cyclic Animation behaviour. Fixed: wrong menu paths for Bake Action, NLA bake, Clean Keyframes, Decimate, Euler filter; "Smooth Keys" is Smooth (Legacy); Decimate Ratio removes (not keeps) a percentage. Removed: 50-90% and 0.1-0.3 figures, version gates, Unity/Unreal loop claims, "Bake Curve/Unbake", exporter-behaviour claims for FBX/glTF, the "Clear Pose Constraints" path and the NLA double-bake claim (no doc coverage).
Method: documentation only; no commands were run.
