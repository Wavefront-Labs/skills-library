---
id: creative-arts.animation.blender.cloth-pinning
name: cloth-pinning
category: creative-arts
field: animation
product: blender
tags: [blender, cloth, cloth-pinning, pin-group, pin-stiffness, shape-pinning, hooks, garment-attachment]
level: practitioner
status: docs-checked
description: "Pin Blender cloth with vertex groups: Pin Group weights and Stiffness, pinning to deforming characters via modifier order, soft gradients and hooks."
sources:
  - https://docs.blender.org/manual/en/latest/physics/cloth/settings/shape.html
  - https://docs.blender.org/manual/en/latest/physics/cloth/introduction.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# cloth-pinning

## Setup

1. Make a vertex group (for example `pin`) on the cloth: waistband, collar, flag pole edge. Per-vertex weight controls how strongly that vertex is pinned.
2. Physics > Cloth > **Shape > Pin Group** = that group. **Stiffness** (target position stiffness) sets how firmly pinned vertices hold their target.
3. Pinned vertices follow whatever deforms the mesh before the Cloth modifier in the stack.

## Pinning to a character

- Put the **Armature** modifier (or other deformers) above Cloth in the stack, so the pinned area follows the skinned body and the rest simulates.
- Surface Deform bound to the body, above Cloth, is an alternative for the pinned area.
- Gradient weights (high at the waist fading toward zero) give softer transitions than a hard 0/1 edge.

## Animating pin points

- Hook modifiers above Cloth (hook the pinned vertices to an Empty) and move the Empty.
- Shape keys and modifiers above Cloth also move pinned vertices.
- Dynamic Mesh and Rest Shape Key are other ways to drive the rest shape (see `cloth-sewing-shape`).

## Gotchas

- Cloth above Armature in the stack leaves pins at the rest pose; order matters.
- Do not let the cloth start penetrating colliders; that makes the sim unstable.
- Moving or editing the cloth after simulating means clearing the cache.

## Verify

Play from the cache start: pinned regions follow the rig; free regions drape and swing.

## Checked

Date: 2026-10-27. Blender 5.2 manual (blender-v5.2-release branch). Confirmed: Shape panel Pin Group and Stiffness (the UI label is Stiffness, not Pin Stiffness), per-vertex weight strength, modifier-order behaviour in the Cloth introduction and the Dynamic Mesh description. Removed the unconfirmed default stiffness value and hook shortcut.
Method: documentation only; no commands were run.
