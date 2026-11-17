---
id: computing-software.game-programming.unreal-engine.ik-rig-and-ik-retargeter
name: ik-rig-and-ik-retargeter
category: computing-software
field: game-programming
product: unreal-engine
tags: [unreal-engine, ik-retargeter, ik-rig, retargeting, animation, game-programming]
level: practitioner
status: docs-checked
description: "Retarget animations between different Unreal skeletons with IK Rig chains and a retarget root, the IK Retargeter, retarget poses, export, and override sets."
sources: ["https://dev.epicgames.com/documentation/en-us/unreal-engine/ik-rig-animation-retargeting-in-unreal-engine", "https://dev.epicgames.com/documentation/en-us/unreal-engine/unreal-engine-ik-rig", "https://dev.epicgames.com/documentation/en-us/unreal-engine/retargeting-bipeds-with-ik-rig-in-unreal-engine"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# IK Rig and IK Retargeter

**Goal:** animations authored for one skeleton play on a different skeleton, even with different bone counts, names
and orientations, optionally keeping hand and foot contacts via IK.

## 1. IK Rig per character
Content Browser > Add (+) > Animation > IK Rig > IK Rig, choose the skeletal mesh; do it for source and target.
- **Retarget root**: the Bipeds page says right-click the bone in the Hierarchy panel and choose Set Retarget Root
  (typically pelvis or hip) so root motion transfers proportionally. The IK Rig Retargeting page calls the same step
  Set Pelvis; the menu wording varies by engine version.
- **Retarget chains** are joint chains, not single bones, so differing bone counts still work. For the biped example
  create Spine, Left Arm, Right Arm, Neck, Head, Left Leg, Right Leg (fingers optional). Create them with Auto Create
  Retarget Chains in the IK Rig Editor toolbar, or select the chain's bones, right-click and choose New Retarget Chain
  (from Selected Bones). A chain may be one bone (Start Bone and End Bone equal).
- Chain Name is auto-filled from common bone names (for example `arm`, `clavicle`, `shoulder` map to Arm; `leg`, `thigh`,
  `calf` to Leg; plus Head, Neck, Spine, Jaw, Tail, finger names, Root) and prefixed Left or Right from the average X
  position. Names across rigs are matched with a fuzzy string match (`ArmLeft` can match `left_arm`), but try to match them.
- IK goals are optional: the pages say they are typically needed only for extra adjustment such as Speed Planting,
  Stride Warping or Blend to Source. Choose No Goal in the Add Goal dialog otherwise.

## 2. IK Retargeter
Content Browser > Add (+) > Animation > IK Retargeter (the Retargeting page gives the path Animation > IK Rig > IK Retargeter),
select the source IK Rig, then set the Target IKRig Asset in the editor.
Checklist from the Bipeds page:
- Chain Mapping panel: target and source chains match (change the Source Chain dropdown if not).
- Reference poses match. If one is a T-pose and the other an A-pose, adjust a retarget pose: toggle Edit Retarget Pose,
  create a new pose (Create (+) > Create) rather than editing Default Pose, enable Edit Mode and rotate bones. Auto
  Align offers methods Direction, Local Rotation Axes, Global Rotation Axes and Mesh. Poses can be imported from an
  Animation Sequence or Pose Asset and exported as a Pose asset.
- Offset and scale preview settings (Target Mesh Offset, Target Mesh Scale) help you see both characters.
Root Settings include Scale Horizontal and Translate Offset Z, which the page uses to exaggerate vertical bounce.
Newer editors build behaviour from an Op Stack (evaluated top-down, per-op LOD thresholds, ops can be written in C++).

## 3. Preview and export
Double-click assets in the Asset Browser to preview. Select animations and click Export Selected Animations, pick a
folder and optional prefix, suffix or search-and-replace names. The Bipeds page says output gets the
`_Retargeted` postfix.

## 4. Override sets and runtime
Override Sets (retarget editor) change op property values, enable or disable ops, and select a retarget pose per
state. They are applied at runtime through the Retarget Pose From Mesh AnimNode (and UAF nodes) with variables
exposed as input pins; variables are single values only (no arrays, maps or sets), and anim curves can be bound to
properties. For batch export use an existing retargeter, not an auto-generated one, and pick the set from the
Override Set to Apply dropdown. This replaces the former Retarget Profiles workflow.

## Verify
- [ ] Chain Mapping shows every chain matched and the preview animation plays without limb flips.
- [ ] Exported sequences appear in the chosen folder.

## Checked
Date: 2026-11-07.
Read in full: IK Rig Retargeting (all sections including Retarget Pose, Asset Settings and Override Sets), Retargeting
Bipeds with IK Rig (all sections), and the IK Rig landing page (a link list only). From dev.epicgames.com; the pages
describe the current editor (they mention Op Stack and Override Sets), so older engine versions differ.
Removed as unconfirmed: "UE5.4+" auto-create claim, FK rotation modes (Interpolated, One to One, Match Chain), IK goal
blending specifics, Full Body IK advice, the claim about live retargeting cost, finger and twist-bone gotchas, root-motion
and additive-animation gotchas, and the advice to name chains identically (the page describes fuzzy matching).
Method: documentation only; no commands were run.
