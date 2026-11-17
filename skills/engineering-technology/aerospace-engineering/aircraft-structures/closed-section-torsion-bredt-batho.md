---
id: engineering-technology.aerospace-engineering.aircraft-structures.closed-section-torsion-bredt-batho
name: closed-section-torsion-bredt-batho
category: engineering-technology
field: aerospace-engineering
product: aircraft-structures
tags: [closed-section-torsion, bredt-batho, torsion, shear-flow, torsion-constant, thin-walled-structures]
level: practitioner
status: verified
description: "Compute shear flow and twist in thin-walled closed and multicell sections with the Bredt-Batho relations, and handle the equal-twist condition in multicell boxes."
sources:
  - "Megson, Aircraft Structures for Engineering Students"
  - "Niu, Airframe Structural Design"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Torsion of closed thin-walled sections

**Goal:** shear flow `q` and twist rate for a wing box or fuselage section under torque `T`.

## Single cell (Bredt-Batho)
- `q = T / (2 A)`, where `A` is the area enclosed by the wall mid-line. Shear stress in a wall of thickness `t` is `q/t`.
- Twist rate `dtheta/dz = (q / (2 A G)) * contour_integral(ds / t)`.
- Torsion constant `J = 4 A^2 / contour_integral(ds/t)`, so `dtheta/dz = T/(G J)`.

## Multicell
1. Give each cell a closed shear flow `q_i`; shared webs carry the difference.
2. Torque equilibrium: `T = sum(2 A_i q_i)`.
3. Compatibility: every cell twists at the same rate: `(1/(2 A_i G)) * contour_integral(q ds/(t))` equal for all cells.
4. Solve the linear system for the `q_i` and `dtheta/dz`.

## Combined with bending shear
Superpose the torsion shear flow on the flexural shear flow (see box-beam-shear-flow); apply the shear load through the shear centre to separate the two.

## Gotchas
- Open sections are far less stiff: `J` is about `sum(b t^3)/3`, orders of magnitude lower.
- Axial restraint (warping) at the root raises stiffness and adds direct stress; Bredt-Batho assumes free warping.
- Use mid-line dimensions for `A`.

## Verify
- [ ] A thin circular tube of radius `r`, thickness `t` gives `J = 2 pi r^3 t`.
