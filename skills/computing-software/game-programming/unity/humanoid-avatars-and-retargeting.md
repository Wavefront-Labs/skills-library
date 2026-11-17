---
id: computing-software.game-programming.unity.humanoid-avatars-and-retargeting
name: humanoid-avatars-and-retargeting
category: computing-software
field: game-programming
product: unity
tags: [unity, humanoid-retargeting, avatar, mecanim, animation-import, game-programming]
level: practitioner
status: docs-checked
description: "Configure Unity Humanoid avatars (bone mapping, T-pose, muscle limits) and retarget animation between humanoid models; know how Generic rigs differ."
sources: ["https://docs.unity3d.com/Manual/ConfiguringtheAvatar.html", "https://docs.unity3d.com/Manual/Retargeting.html", "https://docs.unity3d.com/Manual/MuscleDefinitions.html", "https://docs.unity3d.com/Manual/FBXImporter-Rig.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Humanoid avatars and retargeting

**Goal:** reuse one set of humanoid clips on different humanoid models.

## Humanoid vs Generic
- A Humanoid model has at least 15 bones organised to loosely match a human skeleton (two legs, two arms and a head).
  Everything else is Generic.
- Humanoid uses an Avatar that maps the file's bones to a simplified humanoid structure. Generic animation does not use
  Avatars like Humanoid does; you specify a Root node so Unity can separate bone movement from motion of the root in the
  world (driven from `OnAnimatorMove`).

## Import as Humanoid
Select the model, open the **Rig** tab, set **Animation Type** to **Humanoid**. **Avatar Definition** defaults to
**Create From This Model**; Unity tries to map the bones, and on Apply a check mark appears next to Configure plus an
Avatar sub-asset on the model. A cross means it failed. A successful match only means the required bones matched; for
better results map the optional bones and use a proper T-pose. Always check the Avatar even when automatic creation
works.
- **Copy From Other Avatar** (set **Source**): reuse an Avatar for files with the same bone structure, for example one
  FBX for the mesh and one per animation.
- **Skin Weights**: Standard (4 Bones) is the default and recommended for performance; Custom exposes Max Bones/Vertex
  (1 to 32; more bones cost more performance) and Max Bone Weight.
- **Strip Bones** and **Optimize Game Object** (only with Create From This Model; Extra Transforms to Expose lists
  Transforms Unity should keep when optimizing) are also on the Rig tab.

## Configure the Avatar
Click **Configure...** (or select the Avatar sub-asset and click Configure Avatar). In the Avatar window check the
mapping; name bones for the body parts they represent (for example "LeftArm", "RightForearm") to help matching.
Bones show green when Unity thinks they fit, red otherwise. If mapping fails:
1. Mapping > Clear to reset.
2. Pose > Sample Bind-pose to approximate the initial pose.
3. Mapping > Automap.
4. Pose > Enforce T-Pose; the message "Character not in T-Pose" means bones are assigned but the pose is wrong, and you
   can rotate the remaining bones into a T-pose manually. T-pose is the recommended modelling pose; Pose > Reset is the
   option if the character was not modelled in a T-pose.
You can save the bone mapping as a Human Template (.ht) file.

## Muscles & Settings tab
Tweak range of motion so the character deforms without artifacts. Per-muscle ranges can be narrowed (for Head-Nod and
Head-Tilt the default range is -40 to 40 degrees); sliders preview in the Scene view; a Reset tool restores defaults.
Apply or Revert before switching tabs. **Translate DoF** (Additional Settings) enables translation animation for Chest,
UpperChest, Neck, LeftUpperLeg, RightUpperLeg, LeftShoulder and RightShoulder; otherwise bones animate by rotation only.
It can increase performance requirements, so enable it only if the animation contains animated bone translations.

## Retarget to a new humanoid model
Each humanoid model must use the Humanoid animation type and have a configured Avatar. To replace an animated model:
1. Select the replacement model, Rig tab, Animation Type Humanoid, Apply (this adds an Animator component).
2. Avatar Definition Create From This Model, Configure (model must be in a T-stance), Done.
3. Drag it into the scene, adjust Transform, then in its Animator select the same Animator Controller as the old model
   and the Avatar you configured.
4. Copy over any extra components or scripts from the old model, adjusting property values as needed, then delete the old
   model.

## Avatar Masks
Masks discard part of a clip's animation. Import-time masking is preferable: the discarded data is left out of the build
(smaller files, less memory) and there is less to blend at runtime. A runtime mask is an Avatar Mask asset (Assets >
Create > Avatar Mask) used in an Animator Controller layer.

## Checked
Date: 2026-11-07.
Read in full: "Importing a model with humanoid animations", "Retarget humanoid animation", "Avatar Muscle & Settings tab
reference" and "Rig tab Import Settings reference" (6000.6 docs). Linked pages (Avatar Mapping tab, Human Template,
Avatar Mask window) were not opened.
Removed as unconfirmed: the list of required and optional bone names, the claim that bad rest pose is the top cause of
twisting, normalized muscle space, Foot IK / root motion advice, the Humanoid vs Generic cost/precision table, twist-bone
and Animation Rigging remarks, Avatar Mask transform-list and root-transform bake claims, IK Pass, and the invented Verify
checklist.
Method: documentation only; no commands were run.
