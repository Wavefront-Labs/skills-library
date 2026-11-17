---
id: computing-software.game-programming.unity.animator-blend-trees
name: animator-blend-trees
category: computing-software
field: game-programming
product: unity
tags: [unity, unity-animation, mecanim, blend-tree, locomotion-blending, 2d-freeform-directional, game-programming]
level: practitioner
status: docs-checked
description: "Build Mecanim blend trees: when to use a blend tree vs a transition, creating one, the 2D Simple/Freeform Directional, Freeform Cartesian and Direct types, and Compute Positions."
sources: ["https://docs.unity3d.com/Manual/class-BlendTree.html", "https://docs.unity3d.com/Manual/BlendTree-2DBlending.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Animator blend trees

**Goal:** blend similar motions (walk and run, strafes, leans) by numeric Animator parameters.

## Blend tree or transition
- Transitions move from one Animation State to another over a given amount of time; a transition
  between very different motions is usually fine if it is quick.
- Blend Trees blend several animations by incorporating parts of each. A blending parameter, one of
  the Animator Controller's numeric parameters, controls each motion's contribution. A Blend Tree is a
  special type of state in an Animation State Machine.
- For a good blend the motions must be of similar nature and timing, and the movements should happen
  at the same points in normalized time (for example left foot contact at 0.0 and right at 0.5).
  Because normalized time is used, clips of different length are fine.

## Creating one
1. Right-click empty space in the Animator Controller view.
2. Choose Create State > From New Blend Tree.
3. Double-click it to enter the Blend Tree graph.
Add clips with the plus icon in the Inspector's motion field, or right-click a node to add clips or
child blend nodes. Clips imported from a model are read-only in the Inspector. Pick 1D or 2D from the
Blend Type menu; Direct Blending and Common Blend Tree Options have their own manual pages (not
read here).

## 2D blend types
- **2D Simple Directional**: motions represent directions (for example walk forward, backward, left,
  right, or aim up, down, left, right). Optionally one motion at (0, 0) such as idle. There should not
  be multiple motions in the same direction.
- **2D Freeform Directional**: also for directions, but several motions may share a direction (walk
  forward and run forward). The set should always include a single motion at (0, 0), such as idle.
- **2D Freeform Cartesian**: motions that are not directions, where X and Y can be different concepts
  such as angular speed and linear speed.
- **Direct**: you control each node's weight directly; the page lists facial shapes and random idle
  blending as uses.

## Parameters and positions
- Choose the two Animation Parameters first (the manual's example uses `velocityX` and `velocityZ`),
  then add motions with + > Add Motion Field.
- A motion's position (Pos X, Pos Y) plays the role of a 1D threshold: X relates to the first
  parameter, Y to the second. A walk-forward clip might sit at `velocityX` 0, `velocityZ` 1.5.
- The diagram shows motions as blue dots; motions with no clip or tree assigned are grey and have no
  influence. The red dot marks the current parameter values; in the Preview you can drag it to see
  the blend.
- **Compute Positions** sets positions from root-motion data of the clips: Velocity XZ (Pos X from
  velocity.x, Pos Y from velocity.z), or Speed And Angular Speed (Pos X from angular speed in radians
  per second, Pos Y from speed). Per-axis choices (X/Y Position From): Speed, Velocity X/Y/Z, Angular
  Speed (Rad) and Angular Speed (Deg).

## Checked
Date: 2026-11-07

Read in full: "Animation Blend Trees" and "2D Blending" (including both Compute Positions tables and the
diagram text). The 1D Blending, Direct Blending and Common Blend Tree Options pages were not cited or
read.

Removed because neither cited page confirms it: the 1D row and Automate Thresholds advice with m/s
values, Mirror per child, `Animator.StringToHash` and `SetFloat` damping code, "damped SetFloat must be
called every frame", Cycle Offset, Time Scale / Homogeneous Speed, the root-motion cancelling,
nested-tree cost and parameter-sharing gotchas, and the invented Verify list. The original "needs a
clip at (0,0)" and "no speed variation" wording was restated to match the page text.

Method: documentation only; no commands were run.
