---
id: engineering-technology.aerospace-engineering.ansys-fluent.fluent-design-points-parametric
name: fluent-design-points-parametric
category: engineering-technology
field: aerospace-engineering
product: ansys-fluent
tags: [fluent, ansys, fluent-hpc, design-points, parametric-study, workbench, input-parameters, output-parameters]
level: practitioner
status: draft
description: "Run Fluent parametric studies in Workbench with input and output parameters and design points, such as Mach or angle-of-attack sweeps with convergence checks."
sources:
  - "Ansys Workbench user guide (parameters and design points)"
  - "Fluent user guide (parameters)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Fluent parametric studies and design points

**Goal:** sweep flow conditions or geometry with a clean record.

## Steps
1. In Fluent define **input parameters** (for example boundary values such as Mach number, angle of attack) and **output parameters** (report definitions: CL, CD, Cm).
2. In Workbench, the **Parameter Set** shows input/output parameters; add design points in the Table of Design Points.
3. **Update All Design Points**; Workbench opens Fluent for each, applies inputs, and runs the number of iterations stored in the setup (or a convergence condition).
4. Use a consistent initialisation strategy (initialise from a solved case or data for each point to save time).
5. Export the table of results to a spreadsheet and plot CL-alpha, drag polar, etc.

## Practice
- Include convergence criteria in the report definitions to stop each point automatically.
- Use Design Exploration tools for response surfaces if needed.

## Gotchas
- A design point that fails to converge still produces numbers: add a convergence flag as an output parameter.
- Geometry parameters need re-meshing; keep the mesh controls robust.

## Verify
- [ ] Each design point's residuals and force convergence are saved or flagged.
