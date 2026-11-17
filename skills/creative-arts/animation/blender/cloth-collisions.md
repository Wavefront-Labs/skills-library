---
id: creative-arts.animation.blender.cloth-collisions
name: cloth-collisions
category: creative-arts
field: animation
product: blender
tags: [blender, cloth, cloth-collisions, cloth-self-collision, collision-quality, collision-distance, collision-modifier]
level: practitioner
status: docs-checked
description: "Get clean Blender cloth collisions: collider setup, cloth object and self collision settings (quality, distance, impulse clamping) and fixing pass-through."
sources:
  - https://docs.blender.org/manual/en/latest/physics/cloth/settings/collisions.html
  - https://docs.blender.org/manual/en/latest/physics/collision.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# cloth-collisions

## Colliders

- Body and props get **Physics > Collision**. In its **Soft Body and Cloth** section: **Damping**, **Thickness** (**Outer** and **Inner**, a padding distance added outside and inside each face, where outside and inside follow the face normal), **Friction**, **Single Sided** (treat the collider as the boundary of a solid and eject intersecting cloth along its normal) and **Override Normals** (cloth collision impulses act along the collider normals).
- Colliders must be mesh objects; convert curves, text and NURBS first (Object > Convert).
- A low-poly, smoothed body proxy as the collider is usually faster than the dense render mesh.
- The Collision modifier must come after any shape keys or Armature on the collider, so cloth sees the true posed shape.

## Cloth settings (Physics > Cloth > Collisions)

- **Quality**: collision iterations; higher is slower but gives fewer tears and penetrations.
- **Object Collisions**: **Distance** (how close another object may get before the cloth is repelled; too small can error, too large looks wrong and is slow), **Impulse Clamping** (limits movement after a collision to prevent explosions), **Vertex Group** (faces whose vertices are all in the group are excluded from object collision), **Collision Collection** (only objects in this collection collide, and they still need Collision physics).
- **Self-Collisions**: **Friction**, **Distance**, **Impulse Clamping**, **Vertex Group** (faces fully in the group are excluded). It adds compute time; a distant flag does not need it, a close-up cape or blouse does.

## Fixing pass-through

1. Raise **Quality Steps** (main Cloth panel) and the Collisions **Quality**.
2. Raise Object or Self Collision **Distance** (fastest, least accurate; cloth can look like it rests on air).
3. Check collider normals face the cloth.
4. If the cloth is torn by a deforming mesh, raise its stiffness settings.
5. Last resort: edit the baked result in Edit Mode.

## Gotchas

- Cloth must not start penetrating a collider, or the sim is unstable.
- Changing collision settings does not update a cached sim: Delete Bake and re-run.

## Verify

Inspect in X-ray at fast-motion frames: no body poking through; a render with the real body confirms.

## Checked

Date: 2026-10-27. Blender 5.2 manual (blender-v5.2-release branch). Confirmed: Cloth Collisions panel names and meanings (Quality, Distance, Impulse Clamping, Vertex Group exclusion rule, Collision Collection, self-collision settings), the Collision panel's Soft Body and Cloth fields, the modifier-order note and the troubleshooting list. Removed unconfirmed default and typical values.
Method: documentation only; no commands were run.
