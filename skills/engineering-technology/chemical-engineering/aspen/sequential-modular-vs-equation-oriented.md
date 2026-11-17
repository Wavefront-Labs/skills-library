---
id: engineering-technology.chemical-engineering.aspen.sequential-modular-vs-equation-oriented
name: sequential-modular-vs-equation-oriented
category: engineering-technology
field: chemical-engineering
product: aspen
tags: [chemical-engineering, aspen, aspen-flowsheet-convergence, sequential-modular-vs-equation-oriented, sequential-modular, equation-oriented, eo-mode]
level: practitioner
status: draft
description: "Decide between Aspen Plus sequential-modular and equation-oriented solving, and move a flowsheet to EO safely for optimisation."
sources:
  - "Aspen Plus and Aspen HYSYS user guides and help (AspenTech), Seider et al. Product and Process Design Principles"
  - "https://www.aspentech.com"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Sequential modular vs equation oriented

**Goal:** Decide between Aspen Plus sequential-modular and equation-oriented solving, and move a flowsheet to EO safely for optimisation.

## Steps
1. Sequential-modular (SM) solves block by block with tear streams: robust, good for building and debugging models and the default for most work.
2. Equation-oriented (EO) solves all equations simultaneously: faster for large recycle-heavy models, optimisation and data reconciliation, but needs a good starting point.
3. Converge the model in SM first, then switch the run mode to EO so the SM solution seeds EO; confirm the supported blocks and property options in your version.
4. In EO, design specs become specifications on variables and constraints; fix degrees of freedom exactly (a count mismatch gives a singular or infeasible problem).
5. Fall back to SM to diagnose if EO fails; EO messages list the offending equations.

## Gotchas
- Not every unit model or property option is EO-compatible in every version; confirm in the documentation.
- Starting EO from a poor point is the main failure cause.

## Verify
- [ ] EO and SM give the same solution to tolerance.
- [ ] Degrees of freedom equal zero before solving.
