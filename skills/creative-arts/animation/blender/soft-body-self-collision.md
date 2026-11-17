---
id: creative-arts.animation.blender.soft-body-self-collision
name: soft-body-self-collision
category: creative-arts
field: animation
product: blender
tags: [blender, soft-body, soft-body-self-collision, ball-size, self-collision]
level: practitioner
status: docs-checked
description: "Enable Blender soft body self collision: ball size calculation modes, ball stiffness and damping to stop a soft body passing through itself."
sources:
  - https://docs.blender.org/manual/en/latest/physics/soft_body/settings/self_collision.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# soft-body-self-collision

## How it works

Every vertex is surrounded by an elastic virtual ball, and vertices may not penetrate the balls of other vertices. Self Collision works only when **Edges** (Use Edges) is enabled.

## Settings (Physics > Soft Body > Self Collision)

- **Calculation Type** for ball size:
  - **Manual**: Ball Size directly sets the ball size.
  - **Average**: average length of all edges attached to the vertex, multiplied by Ball Size; works well with evenly distributed vertices.
  - **Minimal / Maximal**: the smallest or largest spring length of the vertex, multiplied by Ball Size.
  - **Average Min Max**: ((Min + Max) / 2) multiplied by Ball Size.
- **Ball Size**: fraction of the attached edge length (computed per the chosen type); a radius within which another vertex of the same mesh makes the vertex deflect. Too high includes too many vertices and slows the calculation; too low lets vertices get too close and possibly intersect.
- **Stiffness**: how elastic the personal-space ball is; high means the vertex reacts immediately.
- **Dampening**: how the vertex reacts; low just slows it as it gets too close, high repulses it.

## When to use

- Long tubes or tentacles that fold onto themselves, rope-like falling soft bodies, a blob squashing into itself.
- Not needed for jiggle with a strong goal.

## Gotchas

- Evenly distributed vertices work best with Average mode; sparse, irregular areas give inconsistent ball sizes, so remesh evenly first.
- Collisions with other objects are not handled here; those need Collision physics on the other object, and the objects must share a layer or collection setup as per the Collision panel.

## Verify

Animate the object folding: no faces pass through each other in the cache; toggling Self Collision off shows interpenetration.

## Checked

Date: 2026-10-27. Blender 5.2 manual (blender-v5.2-release branch). Confirmed: the Edges requirement, all Calculation Type modes and formulas, Ball Size, Stiffness and Dampening semantics. Corrected the mode name AvMiMax to Average Min Max and removed the 0.49-0.6 value, the O(n squared) cost claim and the vertex-count budget, which the manual does not state.
Method: documentation only; no commands were run.
