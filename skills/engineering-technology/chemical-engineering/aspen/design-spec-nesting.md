---
id: engineering-technology.chemical-engineering.aspen.design-spec-nesting
name: design-spec-nesting
category: engineering-technology
field: chemical-engineering
product: aspen
tags: [chemical-engineering, aspen, aspen-flowsheet-convergence, design-spec-nesting, design-spec, calculator-block, nested-loops]
level: practitioner
status: verified
description: "Nest design specifications and Calculator blocks in Aspen Plus so each manipulated variable has one owner and loops converge."
sources:
  - "Aspen Plus and Aspen HYSYS user guides and help (AspenTech), Seider et al. Product and Process Design Principles"
  - "https://www.aspentech.com"
  - "AspenTech Aspen Plus certification study guide AT-05198 (learning objectives, aspentech.com)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Design spec nesting

**Goal:** Nest design specifications and Calculator blocks in Aspen Plus so each manipulated variable has one owner and loops converge.

## Steps
1. List every spec (purity, recovery, duty) and its manipulated variable; each design spec pairs with exactly one varied input within sensible bounds.
2. Keep specs inside the loop they affect, with inner loops (column specs) converging before outer loops (recycle tears); set the convergence order explicitly.
3. Use Calculator blocks (Fortran or Excel, per AspenTech's study guide) for derived inputs (for example set a solvent flow to a multiple of feed) and declare Import and Export variables with the right execution order (before or after the block).
4. Bound the manipulated variable tightly around the expected value and provide a good initial guess; use a step size suited to the variable.
5. If two specs fight each other, reformulate one as a ratio in a Calculator block or move to an Optimization block.

## Gotchas
- A design spec with its variable at a bound shows as converged-but-unmet; read the status message.
- Avoid adding the same variable to two design specs.

## Verify
- [ ] Spec error is within tolerance and the manipulated variable is inside its bounds.
- [ ] The execution order lists inner loops first.
