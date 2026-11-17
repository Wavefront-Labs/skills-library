---
id: engineering-technology.aerospace-engineering.ansys-fluent.fluent-hybrid-initialization
name: fluent-hybrid-initialization
category: engineering-technology
field: aerospace-engineering
product: ansys-fluent
tags: [fluent, ansys, fluent-solver, hybrid-initialization, solution-initialization, fmg-initialization, restart, alpha-sweep]
level: practitioner
status: draft
description: "Initialise Fluent solutions with hybrid initialisation, set farfield-based values, and restart from earlier solutions to cut convergence time for angle-of-attack sweeps."
sources:
  - "Ansys Fluent user guide (solution initialization)"
  - "Fluent TUI reference"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Fluent: initialisation

**Goal:** a good starting field.

## Options
- **Standard initialization:** uniform values from a boundary (for example the far-field): simple, can start badly for complex geometry.
- **Hybrid initialization:** solves Laplace equations for velocity and pressure over the domain and sets other variables by patching, giving a smooth, physically plausible starting flow. In the TUI use `/solve/initialize/hyb-initialization`.
- **FMG initialization:** solves on coarsened meshes first (full multigrid) for faster start; TUI `/solve/initialize/fmg-initialization`.

## Procedure
1. Initialise from the far-field boundary values (standard) or use hybrid.
2. For angle-of-attack sweeps, update the flow direction at the boundary and report definitions, then continue from the previous converged solution without re-initialising.
3. After large changes (for example a Mach step), re-initialise with hybrid or lower the Courant number for a few iterations.

## Gotchas
- Re-initialising between alpha steps discards the converged field: wasteful.
- Hybrid initialization needs the boundary conditions defined before running.

## Verify
- [ ] The initial residuals are moderate and the first 50 iterations do not diverge.
