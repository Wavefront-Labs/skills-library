---
id: creative-arts.animation.blender.collision-thickness
name: collision-thickness
category: creative-arts
field: animation
product: blender
tags: [blender, collision, collision-thickness, outer-thickness, inner-thickness, cloth-collision-distance]
level: practitioner
status: docs-checked
description: "Fix cloth and soft body penetration in Blender with collision thickness outer and inner, cloth collision distance and collider normals."
sources:
  - https://docs.blender.org/manual/en/latest/physics/collision.html
  - https://docs.blender.org/manual/en/latest/physics/cloth/settings/collisions.html
  - https://docs.blender.org/manual/en/latest/physics/soft_body/collision.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# collision-thickness

## Settings (collider: Physics > Collision > Soft Body and Cloth)

- **Thickness**: a padding distance added to the inside and outside of each face; a soft body comes to rest at this distance from the face. Outside and inside follow the face normal.
  - **Outer**: size of the outer collision zone.
  - **Inner**: size of the inner collision zone.
- Cloth also has **Physics > Cloth > Collisions > Object Collisions > Distance**: how close another object must get before the cloth is repelled.
- Both thickness and distance affect the final gap; tune them together.

## Choosing values

- Visible gap between shirt and body: values too large; reduce them.
- Poke-through on fast motion: raise cloth Quality Steps and collision Quality, or raise the distance (the manual says raising Distance is fastest but less accurate and can look like resting on air).
- Soft body: if a vertex travels fast it can pass through the zone; raise Solver Step Size Min and lower Error Limit (see `soft-body-solver`), and make Outer and Inner large enough without letting zones of opposite faces overlap. Strong forces need large zones.

## Gotchas

- Collider normals must point toward the cloth or soft body; negative object scale can flip them, so recalculate normals after applying scale.
- Soft body collision is vertex-based by default, so too few vertices means too little collision; Edge and Face collision options exist but are slower.
- **Single Sided** on a collider makes it act as a solid boundary and ejects intersecting cloth along its normal.

## Verify

Close-up render of collar and sleeves at final camera distance: no poke-through and no floating gap.

## Checked

Date: 2026-10-27. Blender 5.2 manual (blender-v5.2-release branch). Confirmed: Thickness Outer and Inner meaning, cloth Distance semantics, normal-direction and negative-scale hints, soft body collision troubleshooting. Removed the soft-body-only label for Thickness Inner, the "default 0.015" and typical-value figures and the "Single Sided off for thin colliders" advice, which the manual does not support.
Method: documentation only; no commands were run.
