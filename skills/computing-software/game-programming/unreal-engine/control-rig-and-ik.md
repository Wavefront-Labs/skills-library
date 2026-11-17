---
id: computing-software.game-programming.unreal-engine.control-rig-and-ik
name: control-rig-and-ik
category: computing-software
field: game-programming
product: unreal-engine
tags: [unreal-engine, ue5, unreal-animation, control-rig, full-body-ik, fbik, ik-rig, ik-retargeter, procedural-animation, game-programming]
level: advanced
status: docs-checked
description: "Set up Control Rig Full Body IK in Unreal: plugin, FBIK node, effectors, bone settings, limits, excluded bones and node settings, plus what IK Rig is for, per Epic's pages."
sources: ["https://dev.epicgames.com/documentation/en-us/unreal-engine/control-rig-in-unreal-engine", "https://dev.epicgames.com/documentation/en-us/unreal-engine/control-rig-full-body-ik-in-unreal-engine", "https://dev.epicgames.com/documentation/en-us/unreal-engine/unreal-engine-ik-rig"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Control Rig and IK

**Goal:** add procedural adjustment such as ground alignment or arm reaching with Control Rig Full Body IK, and know what
IK Rig is for.

## Where each tool fits (overview pages)
- Control Rig lets you rig and animate in-engine. Its overview links to, among others, Full-Body IK, Control Rig in
  Animation Blueprints ("procedurally affect your Control Rig by using it in Animation Blueprints"), Control Rig Component
  (use Control Rig in Blueprints), Pose Caching and Solve Directions. The overview is an index; those pages were not read.
- IK Rig: interactively create solvers that edit the pose of a skeletal mesh; the asset can be embedded in animation
  systems such as Animation Blueprints. The IK Retargeting system transfers animations between characters of different
  proportions, at runtime or offline to author new sequences.

## Full Body IK (FBIK page)
- Built on a Position Based IK framework (page: faster performance, per-bone settings, preferred angles, squash and
  stretch). Designed as a procedural adjustment tool such as ground alignment or arm reaching.
- Prerequisites: enable the FullBodyIK plugin (Edit > Plugins), restart the editor; have a Control Rig asset with controls.
- Create: right-click the Control Rig graph > Hierarchy > Full Body IK; connect to the Forwards Solve node; set Root (likely
  hips or pelvis in full-body setups); add one Effector per control with + next to Effectors, set each Bone and connect
  its Transform pin from a Get Transform node.
- Bone Settings (+ next to Bone Settings, one bone each; any bone between effectors and Root):
  - Rotation/Position Stiffness: 0 free, 1 locked (page example: pelvis at 0.8).
  - Limits per axis: Free, Limited (Min/Max), Locked (example: ankle Z Limited, -70 to 70).
  - Preferred Angles need Use Preferred Angles enabled (example: knee Z 45).
- Excluded Bones (+ next to Excluded Bones) is recommended over setting bones fully stiff or locked via Bone Settings.
- Effector pins: Position Alpha, Rotation Alpha (1 reaches target, 0 stays at input pose), Strength Alpha, Pull Chain Alpha
  (above 0 partitions the skeleton into chains; helps sparse chains, may hurt complex constrained ones), Pin Rotation.
- Settings: Iterations (raise until effectors converge; increases CPU cost), Mass Multiplier (typical 0.0 to 5.0; higher
  needs more iterations), Allow Stretch, Root Behavior (Pre Pull, Pin to Input, Free), Start Solve from Input Pose.
  Debug: Draw Scale, Draw Debug.

## Checked
Date: 2026-11-07. Read in full: the Full-Body IK page (all sections incl. Node Reference), the Control Rig overview page
and the IK Rig overview page (both short index pages; two embedded topic links on the IK Rig page did not render in the
fetch). Unversioned en-us pages with no engine version stated.
Removed as not on those pages: the Control Rig asset creation path, the Anim BP node and thread-safety claims, the
"Forward Solve runs on worker threads / RigVM" statement, the foot IK pseudo-code and pelvis offset algorithm, solver
list (Two Bone IK, FABRIK, CCDIK, Aim), Anim graph IK node alternatives, LOD/performance and Insights advice, and the
Verify checklist.
Method: documentation only; no commands were run.
