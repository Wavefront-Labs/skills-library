---
id: computing-software.game-programming.unity.animator-culling-and-animation-performance
name: animator-culling-and-animation-performance
category: computing-software
field: game-programming
product: unity
tags: [unity, unity-animation, animator-culling, animation-performance, optimize-game-objects, game-programming]
level: practitioner
status: docs-checked
description: "Cut Unity Animator cost: AnimatorCullingMode values, scale curves, layer weight, Humanoid vs Generic root motion, hashed parameter queries and the manual's culling advice."
sources: ["https://docs.unity3d.com/Manual/MecanimPeformanceandOptimization.html", "https://docs.unity3d.com/ScriptReference/AnimatorCullingMode.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Animator culling and animation performance

**Goal:** keep many animated characters within the CPU budget, using what the manual documents.

## Culling mode (`Animator.cullingMode`, enum `AnimatorCullingMode`)
- `AlwaysAnimate`: always animates the entire character, even when offscreen.
- `CullCompletely`: animation is completely disabled when renderers are not visible.
- `CullUpdateTransforms`: retarget, IK and write of Transforms are disabled when renderers are not
  visible.
- The reference example switches the mode by distance to the main camera: `AlwaysAnimate` within a
  threshold, `CullCompletely` beyond it (set from `Update`).
- The performance manual page says to optimize animations by setting the animator Culling Mode to
  `Cull Completely` and disabling the skinned mesh renderer's Update When Offscreen property, so Unity
  does not update animations when the character is not visible. Whether that fits depends on whether
  gameplay needs the offscreen animation, which the page does not discuss.

## Other costs the manual names
- With no Controller set, the Animator does not spend time processing.
- Playing a single Animation Clip with no blending can be slower than the legacy animation system,
  because the current system uses temporary buffers for blending and extra copying.
- Scale curves are more expensive than translation and rotation curves; avoid scale animation. This
  does not apply to constant curves, which are optimized; constant curves equal to the default scene
  values do not write to the scene every frame.
- Layers: the cost of another layer, synchronized or not, depends on the animations and blend trees it
  plays; at layer weight zero Unity skips the layer update.
- Humanoid: use an Avatar Mask to remove IK Goals or finger animation if not needed. Generic: root
  motion is more expensive than not using it; if animations do not use root motion, do not specify a
  root bone.
- Scene-level tips: use hashes instead of strings to query the Animator; a small AI layer that
  controls the Animator with callbacks; State Tags to match an AI state machine to the Unity one;
  additional curves to simulate events or mark up animations (for example for target matching).

## Checked
Date: 2026-11-07

Read in full: the "Performance and optimization" manual page and the `AnimatorCullingMode` reference
with its example and fields table.

Corrections: the original said Cull Update Transforms still runs the state machine and root motion and
Cull Completely stops root motion and events; the page only says retarget, IK and transform writes are
disabled (Cull Update Transforms) or animation is completely disabled (Cull Completely). Removed
because neither page confirms it: Optimize Game Objects and Extra Transforms to Expose, "Humanoid costs
more than Generic", compression settings, Profiler marker names (`WriteTransforms`, `ProcessGraphJob`
etc.), the manual `anim.Update(dt)` throttling trick, Write Defaults guidance and the invented Verify
list.

Method: documentation only; no commands were run.
