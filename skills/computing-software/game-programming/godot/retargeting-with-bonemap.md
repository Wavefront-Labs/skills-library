---
id: computing-software.game-programming.godot.retargeting-with-bonemap
name: retargeting-with-bonemap
category: computing-software
field: game-programming
product: godot
tags: [godot, godot4, bonemap, skeletonprofilehumanoid, retargeting, animation-import, game-programming]
level: practitioner
status: docs-checked
description: "Retarget humanoid animations in Godot 4 import using BoneMap and SkeletonProfileHumanoid: bone renaming, rest fixer options, and sharing libraries across models."
sources: ["https://docs.godotengine.org/en/stable/tutorials/assets_pipeline/retargeting_3d_skeletons.html", "https://docs.godotengine.org/en/stable/classes/class_bonemap.html", "https://docs.godotengine.org/en/stable/classes/class_skeletonprofilehumanoid.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Retargeting with BoneMap

**Goal:** humanoid animation clips play on any humanoid model in Godot.

## Import-time retargeting
1. Double-click the model (glTF/FBX) > Advanced Import Settings > select the `Skeleton3D`.
2. **Retarget > Bone Map**: create a new BoneMap, Profile = **SkeletonProfileHumanoid**. Godot
   auto-maps bones by name heuristics; fix red (missing) or wrong entries in the body diagram.
3. Enable options:
   - **Rename Bones**: renames skeleton bones to the profile names (`Hips`, `Spine`, `LeftUpperArm`...).
     This is what makes animations shareable: tracks now use standard bone names.
   - **Unique Node**: makes the Skeleton3D a unique node named by `skeleton_name`, so track paths no longer
     depend on the scene hierarchy.
   - **Remove Tracks** (Except Bone Transform, Unimportant Positions, Unmapped Bones): recommended when
     importing an AnimationLibrary to share; may stop animated accessories when importing scenes.
   - **Rest Fixer**: Apply Node Transform; Normalize Position Tracks (normalised by the `scale_base_bone`
     height, Hips for the humanoid profile, stored as `motion_scale`); Overwrite Axis (overwrites bone
     rests to match the profile's reference pose, the most important option for sharing); Fix Silhouette
     (not needed for T-pose models, enable it for A-pose models).
4. Reimport. Do the same for every model and animation file.

## Sharing animations
After retarget import, any model's AnimationPlayer can use an AnimationLibrary from another file with
the same profile (save animations to files, add the library). Position tracks are normalized (hip
height), so different sized characters work.

## Runtime retargeting
`RetargetModifier3D` (a SkeletonModifier3D) transfers the parent skeleton's pose to child skeletons with
different rests in model space. The retargeting page also points to a separate Realtime Retarget Module
for sharing animations while keeping the original bone rests.

## Gotchas
- Auto-mapping uses name pattern matching, so common English bone names map best; missing, duplicate
  or wrongly parented mappings show in magenta/red and warn without blocking the import.
- Overwrite Axis can give very bad results if the original externally set bone rests matter.
- The humanoid profile reference pose is a T-pose facing +Z in a right-handed Y-up system.
- Root motion: set the root bone (Root in profile) and Root Motion track on AnimationMixer.

## Verify
- [ ] A humanoid walk clip plays on two different humanoid models without twisted wrists or floating feet.

## Checked

Checked 2026-10-25 against the Godot 4.7 documentation (godot-docs stable branch, last commit 2026-10-24; latest engine release 4.7.2). Confirmed: Advanced Import Settings > Skeleton3D > Retarget > `bone_map` with SkeletonProfileHumanoid and auto-mapping; Remove Tracks, Bone Renamer (Rename Bones, Unique Node with `skeleton_name`) and Rest Fixer options (Apply Node Transform, Normalize Position Tracks, Overwrite Axis, Fix Silhouette) and their documented caveats; the humanoid profile root bone `Root`, scale base bone `Hips` and bone names such as `LeftUpperArm`; `RetargetModifier3D` description. Removed the unconfirmed 4.4 version claim, the `GeneralSkeleton` default name, the Mixamo reference and the finger and re-import claims.

Method: documentation only; no commands were run.
