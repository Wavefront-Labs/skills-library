---
id: computing-software.game-programming.unity.animation-rigging-constraints
name: animation-rigging-constraints
category: computing-software
field: game-programming
product: unity
tags: [unity, animation-rigging, rig-builder, two-bone-ik, multi-aim, procedural-animation, game-programming]
level: practitioner
status: docs-checked
description: "Set up Unity Animation Rigging (1.3): Animator, Rig Builder, Rig layers and constraint components, evaluation order by hierarchy, rig weight, Bone Renderer and Rig Transform."
sources: ["https://docs.unity3d.com/Packages/com.unity.animation.rigging@1.3/manual/index.html", "https://docs.unity3d.com/Packages/com.unity.animation.rigging@1.3/manual/ConstraintComponents.html", "https://docs.unity3d.com/Packages/com.unity.animation.rigging@1.3/manual/RiggingWorkflow.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Animation Rigging constraints

**Goal:** add procedural motion (secondary animation, targeting, correction) on top of animated
characters with rigs made of constraints.

## What it is for
Per the package manual, an animation rig is a set of constraints adding procedural motion to animated
objects. Examples: deformation rigs for secondary animation of armor, props and accessories, and
World Interaction rigs (sets of IK and Aim constraints) for targeting or for correcting animation
compression artifacts. Version 1.3 of the package documents compatibility with Unity 2023.2 and
later.

## Core components
1. **Animator** on a root GameObject; Animation Rigging works on top of Unity's animation system and
   requires it.
2. **Rig Builder** on the same GameObject as the Animator; it must affect the same hierarchy. It
   creates a Playable Graph appended to the existing Animator state machine and assembles Rigs into
   layers. Rig Layers let you stack several Rigs and enable or disable them at any time.
3. **Rig** on a child GameObject (for example "Rig Setup") of the root, assigned to a Rig Layer on
   the Rig Builder. It is the container for source objects and constraints.
4. **Constraints** on Rig GameObjects or their children. Source objects such as Target Effectors or
   Hint Effectors can sit under the Rig GameObject (the manual's example is a Left Leg IK object with
   a Two Bone IK Constraint, parent of foot effector and leg hint objects).

## Evaluation and weights
- The Rig collects constraint components in its hierarchy with `GetComponentsInChildren` and
  builds an ordered list of `IAnimationJob`s applied to the Animator's pose after its normal
  evaluation. Depth-first order of components in the hierarchy sets evaluation order, so grouping
  constraints under a GameObject lets you manage order.
- The manual says there should be only one Rig component per control rig hierarchy. To use several
  control rigs on one hierarchy, assign each Rig to a different Rig Layer.
- Place the control rig hierarchy root beside the skeleton root, both under the GameObject holding
  the Animator, not inside the skeleton hierarchy.
- Rig and constraint components have a Weight property that can be used, animated or scripted to
  enable, disable or ease an entire control rig in or out.

## Constraint components (built in)
Blend Constraint, Chain IK Constraint, Damped Transform, Multi-Aim Constraint, Multi-Parent
Constraint, Multi-Position Constraint, Multi-Referential Constraint, Multi-Rotation Constraint,
Override Transform, Twist Chain Constraint, Twist Correction and Two Bone IK Constraint. They are
based on the C# Animation Jobs API. The overview page only lists them; per-constraint pages were not
read.

## Utilities
- **Bone Renderer**: draws a transform hierarchy as bones in the Scene view for visualization and
  selection (not visible in the Game view); size, shape (Line, Pyramid, Box) and colour are
  adjustable, and local axis tripods can be shown.
- **Rig Effectors**: gizmos on transforms in the same hierarchy as a Rig Builder or Rig; not visible
  in the Game view.
- **Rig Transform** (Animation Rigging/Setup): required when a GameObject in the rig hierarchy is
  manipulated but not referenced by any constraint; the manual's example is moving two foot IK
  targets through their parent transform.

## Checked
Date: 2026-11-07

Read in full: package manual index (including requirements), Constraint Components (a list only) and
Rigging Workflow (Core Components, Rig Builder, Rig, Bone Renderer, Rig Effectors, Rig Transform).
Pages were fetched as text; the illustrations and the video were not seen.

Removed because the cited pages do not confirm it: the install command and the Animation Rigging >
Rig Setup menu path, the constraint "Use" table (Two Bone IK Root/Mid/Tip/Hint, Multi-Aim axes and
limits, Chain IK for tentacles, etc.), the C# runtime snippet and `rigBuilder.Build()` advice, and
all four Gotchas (cull mode, flipping elbows, worker threads, authored IK targets) plus the Verify
list.

Method: documentation only; no commands were run.
