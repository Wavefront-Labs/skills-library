---
id: engineering-technology.aerospace-engineering.computational-fluid-dynamics.iterative-vs-discretisation-error
name: iterative-vs-discretisation-error
category: engineering-technology
field: aerospace-engineering
product: computational-fluid-dynamics
tags: [cfd, convergence, solver-convergence, iterative-convergence, iterative-error, discretisation-error, numerical-uncertainty, verification]
level: advanced
status: draft
description: "Separate iterative, discretisation and modelling errors, and set iterative convergence tight enough that mesh studies mean something."
sources:
  - "Roache, Verification and Validation in Computational Science and Engineering"
  - "ASME V&V 20"
  - "Eca and Hoekstra, iterative error estimation papers"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Iterative vs discretisation error

**Goal:** make sure mesh-study differences reflect discretisation error, not leftover iterative error.

## Error sources
- **Iterative:** the solution has not finished converging.
- **Round-off:** rarely dominant in double precision, but can limit tight convergence in single precision.
- **Discretisation:** mesh and scheme error; what grid convergence studies measure.
- **Modelling:** turbulence model, boundary conditions, geometry: assessed by validation.

## Practice
1. Converge each mesh until the quantity of interest stops changing; a rule of thumb is iterative error at least one order of magnitude below the expected discretisation difference between grids.
2. Estimate iterative error by monitoring the change per 100 iterations and extrapolating the convergence rate, or by running extra iterations and comparing.
3. Use double precision for external aerodynamics where possible.
4. Document the final residual level and force variation for every mesh in a study.

## Gotchas
- Different residual levels per grid contaminate the order-of-convergence estimate.
- Unsteadiness (buffet, vortex shedding) means there is no iterative convergence; treat as a statistical problem.

## Verify
- [ ] Each grid's quantity of interest is flat to well below the difference between grids.
