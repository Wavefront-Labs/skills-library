---
id: creative-arts.animation.blender.root-motion
name: root-motion
category: creative-arts
field: animation
product: blender
tags: [blender, game-animation, root-motion, in-place, root-bone, locomotion, game-export]
level: practitioner
status: docs-checked
description: "Prepare root motion or in-place locomotion in Blender: add a ground root bone, transfer hips XY travel and yaw to the root, or strip it for in-place clips — and check loops for drift."
sources:
  - https://docs.blender.org/manual/en/latest/editors/graph_editor/fcurves/modifiers.html
  - https://dev.epicgames.com/documentation/en-us/unreal-engine/root-motion-in-unreal-engine
  - https://docs.unity3d.com/Manual/RootMotion.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# root-motion

Goal: engine-friendly locomotion — either the root bone carries travel (root motion) or the clip stays in place.

## Requirements

- A **root** bone at the ground at origin, parent of the hips/COG (and of IK foot controls). If the source skeleton has none (check the imported file), add one in Edit Mode and parent the hips to it (keep offset). Unreal Engine requires a skeleton with a Root Bone carrying the motion data.
- Engines turn root motion into character movement: Unreal extracts it from the Root Bone when Enable Root Motion is on for the animation; Unity splits it into Root Transform Rotation, Position (Y) and Position (XZ) settings in the clip inspector.

## Transfer hips motion to root (Blender)

1. Add a helper empty with Copy Location from hips (X/Y only, World) and Copy Rotation Z (optional for turns).
2. Bake the helper (Object > Animation > Bake Action, visual keying).
3. Root bone: Copy Transforms from the baked helper (XY + Z rotation), bake root.
4. Hips: subtract — re-bake hips with the root now carrying travel (hips local XY stays near 0, Z still bobs).


## In-place clips

Remove XY travel from root/hips: delete those F-curves on the root, or use F-curve modifiers (Generator, Envelope) to subtract the linear travel (forward = constant speed × frame; a practice approach).

## Loop check

- For cyclic root motion, first and last frame root positions differ by exactly the stride; poses identical.
- Foot contacts must stay planted in world space when root motion is applied (Unreal drives the character's movement component with the extracted root motion).

## Gotchas

- Root rotated or scaled at rest is a common cause of wrong axes in engines (practice); keep the root's rest transform as identity at the origin.
- Vertical (Z) root motion is handled differently per engine: Unreal ignores the Z axis of root motion while the character is Walking or Falling and applies gravity, and Unity's Bake Into Pose for Position (Y) leaves vertical motion on the body (and sets Animator.gravityWeight to 1 so physics handles it); keep root Z at 0 unless the clip really changes height, such as a jump.

## Verify

In Blender: the root moves at constant speed along +Y; hips XY oscillate around the root. In engine: no sliding with root motion enabled.

## Checked

2026-10-27. Documentation: Unreal Engine 5.8 Root Motion page and Unity 6.6 (6000.6) How Root Motion works page, fetched this date; Blender manual 5.2 (branch blender-v5.2-release) for F-curve modifiers (Generator, Envelope exist). Confirmed: Unreal needs a Root Bone, Enable Root Motion per animation, and ignores root Z while walking or falling; Unity Root Transform Rotation / Position (Y) / Position (XZ) with Bake Into Pose and the gravityWeight behaviour. Removed the claims that Mixamo rigs lack a root bone, that Mixamo offers In Place downloads, and that Rigify or Auto-Rig Pro offer one-click root-motion bakes, which no accessible source confirms. Blender-side bake steps are practice workflow; the manual has no root-motion page.

Method: documentation only; no commands were run.
