---
id: creative-arts.animation.blender.soft-body-edges
name: soft-body-edges
category: creative-arts
field: animation
product: blender
tags: [blender, soft-body, soft-body-edges, soft-body-springs, soft-body-bending, plastic]
level: practitioner
status: docs-checked
description: "Configure Blender soft body Edges springs: pull, push, damp, plasticity, bending, length and stiff quads to control stretch and shape retention."
sources:
  - https://docs.blender.org/manual/en/latest/physics/soft_body/settings/edges.html
  - https://docs.blender.org/manual/en/latest/physics/soft_body/forces/interior.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# soft-body-edges

## Settings (Physics > Soft Body > Edges)

Enable the Edges checkbox so mesh edges act as springs.

- **Springs**: vertex group giving per-vertex spring strength.
- **Pull**: stiffness against stretching. Low is elastic; high resists being pulled apart. The manual's scale: 0.5 latex, 0.9 sweater, 0.999 starched napkin or leather; the sim tends to become unstable at 0.999, so lower it if that happens.
- **Push**: resistance to being scrunched together, like a compression spring. Low for fabric, high for inflated objects and stiff material.
- **Damp**: friction of the edge springs; high values (maximum 50) calm the Push and Pull effect.
- **Plasticity**: permanent deformation after a collision; vertices take a new position without applying the modifier.
- **Bending**: virtual connections between a vertex and the vertices connected to its neighbours, including diagonal edges; damping also applies.
- **Length**: shrink or blow up edges, in percent; 0 disables it and 100 means no change.
- **Collision Edge / Face**: check edges, or any portion of faces, for collision rather than only vertices. Face is computationally intensive and has no damping setting, so parts near a collider can jitter; Edge has damping.
- **Stiffness** subpanel: **Stiff Quads** adds diagonal springs on quads so they do not collapse; **Shear** is their stiffness (see `soft-body-aerodynamics`).

## Recipes (starting points to tune)

- **Bouncy rubber ball**: high Pull and Push, Bending above zero, Goal off, Collision Face on if it must pass thin colliders.
- **Jelly**: Pull and Push around the middle of the range, low Damp, small Bending.

## Gotchas

- Soft bodies lose volume easily; for blob shapes consider Cloth with Pressure (`cloth-pressure-internal-springs`).
- Stiff springs need a smaller step: raise Solver Step Size Min (see `soft-body-solver`).
- Dense meshes simulate slowly; sim a lower-poly cage or use a Lattice and drive the render mesh from it.

## Verify

Drop the object on a plane: it compresses, rebounds and recovers its shape (unless Plasticity is on).

## Checked

Date: 2026-10-27. Blender 5.2 manual (blender-v5.2-release branch). Confirmed: Edges panel fields and their descriptions, the Pull value scale and 0.999 instability note, Damp maximum of 50, Length semantics and the Edge and Face collision notes. Corrected the "vertex group" label (it is called Springs) and removed the unconfirmed 0-0.999 range and 50-100 plasticity guidance.
Method: documentation only; no commands were run.
