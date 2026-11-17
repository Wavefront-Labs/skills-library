---
id: creative-arts.animation.blender.keying-sets
name: keying-sets
category: creative-arts
field: animation
product: blender
tags: [blender, animation, keying-sets, keying-set, whole-character, available-keying-set, keyframes]
level: practitioner
status: docs-checked
description: "Use and build Blender keying sets: built-ins (Location, LocRotScale, Whole Character, Available, Visual), the active keying set, custom absolute keying sets, and adding custom properties with K."
sources:
  - https://docs.blender.org/manual/en/latest/animation/keyframes/keying_sets.html
  - https://docs.blender.org/manual/en/latest/animation/animation_editors.html
  - https://projects.blender.org/blender/blender/src/branch/blender-v5.2-release/scripts/startup/keyingsets_builtins.py
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# keying-sets

Goal: one keypress keys exactly the channels you want — the whole rig for blocking, or a fixed set of props for a shot.

## Built-in keying sets (K in the 3D Viewport lists them and keys with the one you pick)

- **Location**, **Rotation**, **Scale**, **Location & Rotation**, **Location & Scale**, **Rotation & Scale**, **Location, Rotation & Scale**, **Location, Rotation, Scale & Custom Properties**, and **B-Bone Shape**.
- **Available**: only channels that already have F-curves.
- **Visual** variants (Visual Location, Visual Rotation, Visual Scale and the combined ones): key the constraint-evaluated transform (e.g. after IK/Child Of).
- **Whole Character**: all properties likely to be animated in a character rig — the standard blocking key in Pose Mode. It skips bones whose names start with COR, DEF, GEO, MCH, ORG or VIS (technical bones, as Rigify generates). **Whole Character (Selected Bones Only)** is the variant limited to selected bones.
- **Delta Location / Rotation / Scale** for delta transforms.

## Active keying set

Set it in Timeline > Keying popover > Active Keying Set, with **Shift-K** in the 3D Viewport, or by selecting one in Scene Properties > Keying Sets. When set, **I** (while not hovering an input field) keys with it directly. The Set Active Keying Set menu also offers Clear Active Keying Set.

## Custom (absolute) keying set

1. Scene Properties > Keying Sets > **+** (Add Empty Keying Set) → name it (e.g. `ShotProps`).
2. Hover any property (light energy, camera focal length, a custom prop) and press **K** → adds it to the active keying set (a new one is created if none exist); or right-click > Add All to Keying Set / Add Single to Keying Set. Built-in keying sets cannot be edited.
3. In the Active Keying Set panel each path has a Data Path, *Array All Items* or a single index, and *F-Curve Grouping* (Keying Set Name, None, Named Group).
4. Keyframing settings overrides: Needed and Visual.
Now I keys all those properties at once from anywhere.

## Gotchas

- Absolute keying sets reference specific data paths/objects; renaming objects breaks them.
- Whole Character keys every bone — fine for blocking, noisy for polish (switch to Available).
- Auto Keying can be restricted to the active keying set (Auto Keying options > Only Active Keying Set).

## Verify

Press I with the set active, then Dope Sheet shows keys exactly on the listed channels.

## Checked

2026-10-27. Documentation release: Blender manual 5.2 (branch blender-v5.2-release) and keyingsets_builtins.py from the same release branch. Confirmed: built-in keying set names (Location, Rotation, Scale, Location & Rotation, Location & Scale, Rotation & Scale, Location, Rotation & Scale, ... & Custom Properties, B-Bone Shape, Visual variants, Available, Whole Character, Whole Character (Selected Bones Only), Delta variants); the Whole Character skipped-prefix list, K to list keying sets, Shift-K to set the active set, Add All/Single to Keying Set, Keying Set panels and Needed/Visual overrides (animation/keyframes/keying_sets.rst); Only Active Keying Set (animation/animation_editors.rst). Wrong in the old text: Shift-K (not K) sets the active set, XYZ to RGB is not a keying set option, and the auto keying option is Only Active Keying Set. Removed the claim that Whole Character ignores selection beyond what the source states.

Method: documentation only; no commands were run.
