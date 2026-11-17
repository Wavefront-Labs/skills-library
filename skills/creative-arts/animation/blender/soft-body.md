---
id: creative-arts.animation.blender.soft-body
name: soft-body
category: creative-arts
field: animation
product: blender
tags: [blender, soft-body, softbody, jiggle, jelly, goal-weights, edge-springs, self-collision, physics, secondary-motion, bake, cache]
level: advanced
status: docs-checked
description: "Blender Soft Body for jelly, jiggle and springy props: goal vs edge springs, key settings, collision and self-collision, baking, and when cloth or bones fit better."
sources:
  - https://docs.blender.org/manual/en/latest/physics/soft_body/introduction.html
  - https://docs.blender.org/manual/en/latest/physics/soft_body/settings/index.html
  - https://docs.blender.org/manual/en/latest/physics/soft_body/collision.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# soft-body

Goal: make a mesh wobble, sag or bounce convincingly with the Soft Body solver, and know when not to use it.

## When to use what

| Need | Use |
|---|---|
| Jelly, rubber, gelatin, ropes, branches in wind, jiggle on a moving character | **Soft Body** (designed for secondary motion such as jiggle) |
| Fabric, flags, capes | Cloth (`creative-arts.animation.blender.cloth-simulation`); the manual says Cloth does fabric better with a dedicated solver |
| Jiggle on a rigged character where control matters | jiggle bones, or Soft Body on a cage with Goal and a deform bound to the cage (`creative-arts.animation.blender.advanced-deformation`) |
| Hard objects colliding | Rigid Body (`creative-arts.animation.blender.destruction-rbd`) |
| Procedural, controllable | Geometry Nodes simulation zone (`creative-arts.animation.blender.simulation-nodes`) |

Soft Body works on objects with vertices or control points (meshes, curves, surfaces, lattices). A Lattice or Curve Guide soft body instead of the object itself can be far faster.

## Setup (Physics tab, Soft Body)

Start playback with Alt+A (stop with Esc or Alt+A); scrub the Timeline to see the sim at any frame.

- **Object**: **Friction** (friction of the surrounding medium), **Mass** (per vertex; larger mass slows acceleration, except gravity), **Control Point** (a vertex group painted for per-vertex mass).
- **Simulation > Speed**: internal timing; relates frame rate to simulation tempo.
- **Solver**: **Step Size Min / Max**, **Auto-Step**, **Error Limit**, **Choke**, **Fuzzy**, diagnostics **Print Performance to Console** and **Estimate Transforms**.
- **Goal** (checkbox): vertices are pulled toward their animated position (F-Curves, armatures, parents, lattices). **Vertex Group** weights multiply the **Default** goal; **Min/Max** clamp the weights. **Stiffness** is the goal spring, **Damping** its friction. Goal 1.0 means no simulation; 0.0 means fully simulated.
- **Edges** (checkbox): edges act as springs. **Springs** (vertex group for strength), **Pull**, **Push**, **Damp** (max 50), **Plasticity**, **Bending**, **Length** (percent; 0 disables, 100 means no change), **Collision Edge / Face**, **Aerodynamics** (Type Simple or Lift Force, Factor), and the **Stiffness** subpanel with **Stiff Quads** and **Shear**.
- **Self Collision** (checkbox, needs Edges): **Calculation Type** (Manual, Average, Minimal/Maximal, Average Min Max), **Ball Size**, **Stiffness**, **Dampening**.
- **Cache**: frame range, Disk Cache, Bake.
- **Field Weights**: **Effector Collection**, **Gravity**, **All**; force fields such as wind act on soft bodies.

## Colliders

Other objects need **Physics > Collision** (mesh objects only; a collider may itself be a soft body). If a soft body's **Collision Collection** is set, colliders must belong to it. See `collision-thickness` for Outer and Inner padding. Collisions are vertex-based by default, so too few vertices means too little collision. A simplified, slightly larger, invisible collision mesh speeds things up.

## Recipes (starting points to tune)

- **Jelly cube**: subdivide a cube, Soft Body with Goal off, Edges on with high Pull and Push, Bending above zero, Stiff Quads Shear on, Self Collision on, a floor with Collision.
- **Antenna or floppy ear**: goal vertex group gradient from high at the base to lower at the tip, tune Goal Stiffness and Damping, Edges on with some Bending.
- **Sealed balloon**: Cloth has a Pressure panel for this (`cloth-pressure-internal-springs`); use Soft Body only for a swaying one.
- **Secondary jiggle on a rigged mesh**: low-poly cage with Armature above Soft Body, goal weights lower where it should jiggle, then drive the high-res mesh from the cage.

## Baking and caching

Scrubbing without a bake recomputes. Bake once settings are final; the manual notes you can also bake-edit (edit intermediate results and resume). Applying the Soft Body modifier makes the current deformation permanent. Start the cache before the shot so the mesh settles from rest first.

## Stability troubleshooting

- Fast collider missed: raise Step Size Min; lower Error Limit (manual: start at half the average edge length, decrease if you see jitter or exaggerated responses).
- Vertices fire off colliders: raise Choke.
- Thin collider slipped through: enable Collision Face or Edge (slower, and Face tends to jitter); enlarge Outer and Inner.
- Collapses flat: add Bending and Stiff Quads Shear.
- Too slow: fewer vertices (sim a cage), larger Fuzzy (faster, less accurate), avoid Face collision.

## Gotchas

- Modifier order: put Soft Body after Armature when using Goal (the goal follows the animated shape) and before Subdivision Surface.
- Soft Body vertices react to Force Fields on a shared layer; check Field Weights if the object drifts.
- Self Collision only works with Edges on.

## Verify

- The object settles under gravity within the lead-in, then responds to the collider with no interpenetration.
- Changing Bending visibly changes firmness; a goal gradient keeps the base pinned while the tip lags.

## Checked

Date: 2026-10-27. Blender 5.2 manual (blender-v5.2-release branch). Confirmed: panel and field names (Object, Simulation Speed, Solver, Goal, Edges, Self Collision, Field Weights), goal semantics (vertex group multiplies Default), Control Point as a mass vertex group, collision prerequisites and troubleshooting list. Corrected: Control Point is a vertex group, not a driving object; AvMiMax is Average Min Max. Removed all default values, performance and vertex-count figures, the Wiggle 2 and cache-folder claims and the old balloon claim.
Method: documentation only; no commands were run.
