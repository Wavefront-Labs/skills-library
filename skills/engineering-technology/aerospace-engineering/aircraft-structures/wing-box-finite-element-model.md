---
id: engineering-technology.aerospace-engineering.aircraft-structures.wing-box-finite-element-model
name: wing-box-finite-element-model
category: engineering-technology
field: aerospace-engineering
product: aircraft-structures
tags: [aircraft-structures, structural-fem, fem, wing-box-fem, shell-elements, rbe3, nastran, model-checks]
level: practitioner
status: draft
description: "Build and check a wing-box finite element model: element types, stiffener idealisation, boundary conditions, load application and the checks that catch modelling mistakes."
sources:
  - "MSC Nastran and NX Nastran user guides (element and quality checks)"
  - "Niu, Airframe Structural Design"
  - "NAFEMS finite element guidelines"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Wing-box finite element model

**Goal:** a model whose internal loads can be trusted.

## Idealisation
- Skins and webs: shell elements (QUAD4 preferred, few TRIA3), about one element between stiffeners or smaller, mesh aligned with ribs and spars.
- Stiffeners, spar caps: beam or rod elements with offsets (or shell if local modelling), correct cross-section properties.
- Ribs: shells; rib posts and fittings: beams.
- Fuel, engine and control surface masses as concentrated or distributed masses (CONM2, RBE3 distribution).
- Aero loads mapped to structure by spline or RBE3; apply at nodes on ribs.

## Boundary conditions
Fix the root with SPC at the wing-fuselage attach or model fuselage stiffness; use inertia relief (`SUPORT`) for free-flight balanced loads.

## Checks (Nastran examples)
1. Free-free modal run: six zero-frequency rigid body modes.
2. Unit gravity and thermal load checks for mass and stiffness.
3. Grid point force balance (GPFORCE) and SPC forces equal applied load sum.
4. Element quality (aspect, warp, skew), duplicate nodes, free edges (shown in plots).
5. Compare shear and bending to the hand-calculated wing loads.

## Gotchas
- Wrong offsets for stiffeners gives wrong bending stiffness.
- Local stress concentrations are mesh-sensitive; use global-local models for details.

## Verify
- [ ] Reaction forces match the load sum and modal check shows six rigid-body modes.
