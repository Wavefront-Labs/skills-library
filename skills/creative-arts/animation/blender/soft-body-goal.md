---
id: creative-arts.animation.blender.soft-body-goal
name: soft-body-goal
category: creative-arts
field: animation
product: blender
tags: [blender, soft-body, soft-body-goal, goal-strength, goal-vertex-group, jiggle]
level: practitioner
status: docs-checked
description: "Use Blender soft body Goal to pin or partially follow animation: goal vertex group, min/max/default strength, goal stiffness and damping."
sources:
  - https://docs.blender.org/manual/en/latest/physics/soft_body/settings/goal.html
  - https://docs.blender.org/manual/en/latest/physics/soft_body/forces/exterior.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# soft-body-goal

## What Goal is

A goal is the shape a soft body tries to conform to. Enabling **Goal** makes the sim use the motion from animation (F-Curves, armatures, parents, lattices) as the desired end position of each vertex. A goal of 1.0 means no simulation (the vertex stays at its animated position); 0.0 or no goal means fully simulated; values between blend the two. This is how you add jiggle to an animated part such as a belly, antenna or cheeks.

## Settings (Physics > Soft Body > Goal)

- **Vertex Group**: per-vertex goal weights, multiplied by the **Default** goal. For non-mesh objects the control-point weight is used instead.
- **Strengths > Default**: goal for all vertices when no group is assigned.
- **Strengths > Min / Max**: clamp the vertex-group weights; the lowest weight becomes Min and the highest becomes Max.
- **Settings > Stiffness**: goal spring stiffness (low is a floppier attachment, high is stiffer).
- **Settings > Damping**: goal friction (higher gives less jiggle and the motion stops sooner).

## Recipe: belly jiggle

1. Vertex group (for example `jiggle_goal`) with high weight on the parts that should follow the animation and lower weight on the belly.
2. Soft Body on the mesh with the **Armature** modifier above it, so the sim receives the posed shape.
3. Goal on with that group; tune Stiffness and Damping; Edges on to keep volume.
4. If the belly sags, reduce Gravity in Soft Body > Field Weights.

## Gotchas

- Armature must come before Soft Body in the stack; otherwise the sim works on the rest pose.
- Vertices with goal 0 and no edges just fall away, so enable Edges for jiggle.
- Changing the animation means clearing the cache.

## Verify

Play the walk: the belly overshoots on foot plants and settles; the root attachment does not drift.

## Checked

Date: 2026-10-27. Blender 5.2 manual (blender-v5.2-release branch). Confirmed: Goal panel fields (Vertex Group, Default, Min/Max, Stiffness, Damping), the weight-times-Default rule, the 0 to 1 blend semantics, and Field Weights Gravity. Removed unconfirmed example weights and settle-time figures.
Method: documentation only; no commands were run.
