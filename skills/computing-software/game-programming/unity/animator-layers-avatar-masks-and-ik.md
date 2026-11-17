---
id: computing-software.game-programming.unity.animator-layers-avatar-masks-and-ik
name: animator-layers-avatar-masks-and-ik
category: computing-software
field: game-programming
product: unity
tags: [unity, unity-animation, avatar-mask, animator-ik, animation-layers, onanimatorik, foot-ik, look-at, game-programming]
level: advanced
status: docs-checked
description: "Combine Animator layers (mask, Override vs Additive blending, Sync and Timing) with Mecanim humanoid IK: IK Pass, OnAnimatorIK, SetIKPosition and SetLookAtPosition."
sources: ["https://docs.unity3d.com/Manual/AnimationLayers.html", "https://docs.unity3d.com/Manual/InverseKinematics.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Animator layers, avatar masks and IK

**Goal:** play an upper-body action over locomotion, and reach or look at targets with humanoid IK.

## Layers
- Animation Layers manage complex state machines for different body parts, for example a lower-body
  layer for walking and jumping and an upper-body layer for throwing or shooting.
- Manage layers in the Layers tab at the top left of the Animator Controller; the gear icon shows the
  layer settings; add a layer with +.
- Each layer has a **mask** (the body parts the animation applies to) and a **Blending** type:
  **Override** replaces the animation on previous layers; **Additive** adds on top of previous layers,
  and for additive blending to work the additive layer's animation must contain the same properties as
  the previous layers.
- Example from the page: a mask defining the upper body on the layer that plays a throwing animation,
  so the character can still walk, run or stand. An M symbol in the Layers sidebar means a mask is
  applied.
- **Sync**: tick Sync on a layer and pick the layer to sync with to reuse its state machine with
  different clips (wounded walk/run/jump instead of healthy). A synced layer has no state machine of
  its own; structural edits made in its view apply to the source layer, and only the animations chosen
  per state are unique. An S symbol marks synced layers.
- **Timing** on a synced layer: unselected, the synced layer's animations are stretched to the original
  layer's lengths (original is sole master); selected, lengths are a compromise balanced by weight.

## Humanoid IK (Mecanim)
- IK poses joints from a goal backwards. Per the manual it is supported in Mecanim for a humanoid
  character with a correctly configured Avatar.
- Animator functions listed: `SetIKPositionWeight`, `SetIKRotationWeight`, `SetIKPosition`,
  `SetIKRotation`, `SetLookAtPosition`, `bodyPosition`, `bodyRotation`.
- Setup steps from the page: create a valid Avatar; create an Animator Controller with at least one
  animation; in the Animator window Layers pane click the cog on the layer and enable **IK Pass**,
  which makes Unity send an `OnAnimatorIK` callback; assign the controller to the Animator; add a
  script that uses the callback.
- Page example (abridged): in `OnAnimatorIK()`, when IK is active call
  `animator.SetLookAtWeight(1)` and `SetLookAtPosition(lookObj.position)`, then
  `SetIKPositionWeight(AvatarIKGoal.RightHand, 1)`, `SetIKRotationWeight(AvatarIKGoal.RightHand, 1)`,
  `SetIKPosition(...)` and `SetIKRotation(...)` with the target's position and rotation; when not
  active set those weights back to 0.
- Use an empty child GameObject (the page calls it Cylinder Grab Handle) as the IK target so the hand
  touches but does not pass through the object.

## Checked
Date: 2026-11-07

Read in full: "Animation Layers" and "Inverse Kinematics" including the complete `IKControl` listing.

Removed because neither page confirms it: layer weight via `SetLayerWeight`, "later layers override
earlier ones" as a general ordering rule, additive reference-pose wording, the Generic mask transform
list claim, the foot-IK code (raycasts, animation curves, pelvis lowering via `bodyPosition`), weapon
foregrip and `SetIKHintPosition` elbow hints, "built-in IK is Humanoid only" beyond the page's
"supported in Mecanim for a humanoid character", pointer to the Animation Rigging package, the
`OnAnimatorIK(int layer)` signature (the page's example has no parameter), the three Gotchas and the
invented Verify list.

Method: documentation only; no commands were run.
