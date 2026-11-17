---
id: engineering-technology.aerospace-engineering.ansys-fluent.grid-sequencing-and-restarts
name: grid-sequencing-and-restarts
category: engineering-technology
field: aerospace-engineering
product: ansys-fluent
tags: [grid-sequencing, restarts, fmg-initialization, convergence-acceleration, case-and-data-files, fluent]
level: practitioner
status: draft
description: "Speed up hard Fluent cases with FMG initialisation and coarse-to-fine starts, and restart runs from saved case and data files without losing the solution."
sources:
  - "Ansys Fluent user guide (initialization and file chapters)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Grid sequencing and restarts

**Goal:** get a good starting solution cheaply and resume long runs safely.

## Grid sequencing and FMG
- Full multigrid (FMG) initialisation builds coarse levels, solves them and interpolates to the fine mesh. It is available under Solution Initialization (and as a text command under `/solve/initialize/`); its settings are in the FMG initialization options.
- FMG uses first-order inviscid solves on the coarse levels, so it suits Euler-like starts for compressible cases; it is not a substitute for converging the real RANS problem.
- A manual alternative: converge a coarse mesh, then read its data into the fine mesh using `File > Interpolate`, then continue.

## Restarts
1. Save case and data together (`.cas.h5` and `.dat.h5` in current releases); the case holds settings, the data holds the solution.
2. Turn on autosave every N iterations so a crash costs minutes, not hours.
3. To resume: read case and data, check the iteration counter, confirm monitors continue, then run.
4. When changing a boundary value for a polar sweep, start each new angle of attack from the previous solution.

## Gotchas
- Changing the solver family, turbulence model or number of equations invalidates old data; reinitialise.
- A restart with different partitioning on a different core count is fine; a different mesh is not, unless interpolated.
- Monitor files are overwritten or appended depending on setup; keep a copy of the residual history.

## Verify
- [ ] The first residual after the restart is close to the last before it (no jump).
