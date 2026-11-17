---
id: engineering-technology.aerospace-engineering.computational-fluid-dynamics.mesh-quality-metrics
name: mesh-quality-metrics
category: engineering-technology
field: aerospace-engineering
product: computational-fluid-dynamics
tags: [cfd, meshing, mesh-generation, mesh-quality, skewness, orthogonal-quality, aspect-ratio, expansion-ratio, non-orthogonality]
level: practitioner
status: draft
description: "Read skewness, orthogonality, aspect ratio and expansion ratio, set acceptable limits per solver, and fix the worst cells instead of just reporting them."
sources:
  - "Ansys Fluent user guide (mesh quality)"
  - "OpenFOAM checkMesh documentation"
  - "Blazek, Computational Fluid Dynamics Principles and Applications"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Mesh quality metrics

**Goal:** a mesh that will not degrade accuracy or stability.

## Metrics
- **Skewness:** deviation of a cell from its ideal shape (0 good, 1 degenerate). Fluent guidance: maximum skewness below about 0.95 for solving, with most cells much lower.
- **Orthogonal quality:** 1 best, 0 worst; Fluent guidance: minimum above about 0.01, average well above 0.1.
- **Non-orthogonality (OpenFOAM `checkMesh`):** angle between face normal and the line joining cell centres; values above about 70 degrees are flagged and above 85 severe; correct with non-orthogonal correctors.
- **Aspect ratio:** high is acceptable in boundary layers aligned with the flow, harmful elsewhere.
- **Expansion/volume change ratio:** neighbouring cell size ratio, keep under about 1.2-1.5.

## Procedure
1. Run the solver's mesh check or report (for example Fluent `Report Quality` or `mesh/check`; OpenFOAM `checkMesh -allGeometry -allTopology`).
2. Identify the worst cells by location (usually trailing edges, junctions, tips).
3. Repair: local refinement, smoothing, remeshing, changing surface mesh, or modifying CAD slivers.
4. Re-check after every change; one bad cell in a sensitive spot can stall convergence.

## Gotchas
- Good average metrics hide a few bad cells; look at the worst.
- Metrics thresholds are solver-specific guidance, not laws; compression of the metric does not replace a grid convergence study.

## Verify
- [ ] Reported minimum orthogonal quality and maximum skewness meet the solver's guidance.
- [ ] Solution is not sensitive to local mesh repairs.
