---
id: creative-arts.animation.blender.soft-body-aerodynamics
name: soft-body-aerodynamics
category: creative-arts
field: animation
product: blender
tags: [blender, soft-body, soft-body-aerodynamics, stiff-quads, aerodynamics, shear]
level: practitioner
status: docs-checked
description: "Use Blender soft body aerodynamics (simple and lift force) and Stiff Quads shear springs for leaves, paper and sails reacting to air."
sources:
  - https://docs.blender.org/manual/en/latest/physics/soft_body/settings/edges.html
  - https://docs.blender.org/manual/en/latest/physics/soft_body/forces/exterior.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# soft-body-aerodynamics

## Aerodynamics (Physics > Soft Body > Edges > Aerodynamics)

- **Type**: **Simple** (edges receive a drag force from the surrounding medium) or **Lift Force** (edges receive a lift force when passing through it).
- **Factor**: how much aerodynamic force to use; the manual suggests trying 30 first.
- The force acts on edges, not vertices: perpendicular to the edge, scaled by the relative speed projected on the edge. An edge moving along its own direction feels no force; one moving perpendicular feels the maximum. The force is the same whether wind blows or the edge is dragged through still air.
- Vertices with fewer connecting edges (the front of a plane) fall faster than vertices with more, so uneven topology gives uneven drift; equal edge counts fall evenly.
- Needs Edges enabled; pair with wind force fields.

## Stiffness (Stiff Quads and Shear)

- The **Stiffness** subpanel of Edges has **Stiff Quads**: for quad faces, the diagonal edges are used as springs so quads do not collapse completely on collisions.
- **Shear**: stiffness of those virtual diagonal springs.
- Triangle faces get no diagonals from this option.

## Recipe: falling leaf

1. Low-poly leaf of quads, Soft Body with Goal off and Edges on.
2. Stiff Quads on, Aerodynamics Type Lift Force, Factor starting near the manual's 30.
3. Add a weak Wind force field with noise for flutter.

## Gotchas

- For hanging fabric Cloth is the better tool; use soft body aerodynamics for small sheets.

## Verify

The leaf drifts and side-slips instead of falling straight; disabling aerodynamics makes it fall like a stone.

## Checked

Date: 2026-10-27. Blender 5.2 manual (blender-v5.2-release branch). Confirmed: Aerodynamics Type (Simple, Lift Force) and Factor, the edge-based force description, Stiff Quads and Shear. Removed the unconfirmed 5-30 and 0-1 ranges and the leaf recipe values.
Method: documentation only; no commands were run.
