---
id: engineering-technology.aerospace-engineering.ansys-fluent.fluent-poly-hexcore-volume-mesh
name: fluent-poly-hexcore-volume-mesh
category: engineering-technology
field: aerospace-engineering
product: ansys-fluent
tags: [fluent, ansys, fluent-meshing, poly-hexcore, volume-mesh, hexcore, polyhedral, cell-count]
level: practitioner
status: draft
description: "Choose poly-hexcore for external aerodynamics in Fluent Meshing: when it saves cells versus tetrahedra, its settings, and its failure modes."
sources:
  - "Ansys Fluent Meshing user guide (volume mesh options)"
  - "Ansys documentation on poly-hexcore meshes"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Poly-hexcore volume meshes

**Goal:** fewer, better-shaped cells than tetrahedral fill.

## What it is
A Cartesian hexahedral core in the bulk, polyhedral cells transitioning to the prism-layer region at the wall. Compared with tetrahedral fill it usually gives a lower cell count for equal resolution, better orthogonality, and faster convergence.

## Settings
- Volume Fill: Poly-Hexcore; max cell length sets the core cell size; use size boxes (body of influence) around wake and shock regions.
- Buffer layers and peel layers control the transition thickness; the default gives acceptable results in most cases.
- Growth rate for the volume fill around 1.2 for smooth size change.
- Check that boundary-layer layers remain intact after the fill.

## Practice
1. Create the surface mesh and boundary layers first.
2. Generate poly-hexcore and view cell counts; compare with tetra.
3. Check the quality report (orthogonal quality and skewness) and look at the transition region by sections.

## Gotchas
- Thin gaps or sharp-edged geometry may need local refinement or tetrahedral fill.
- Hanging nodes: some solvers and checks differ; use only with the solver for which it is intended (Fluent handles it).

## Verify
- [ ] Mesh quality report meets guidance (see mesh-quality skill).
- [ ] Mesh-independence study done with at least three refinements.
