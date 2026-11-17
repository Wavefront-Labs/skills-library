---
id: engineering-technology.chemical-engineering.aspen.wegstein-and-broyden-convergence-methods
name: wegstein-and-broyden-convergence-methods
category: engineering-technology
field: chemical-engineering
product: aspen
tags: [chemical-engineering, aspen, aspen-flowsheet-convergence, wegstein-and-broyden-convergence-methods, wegstein, broyden, newton, convergence-method]
level: practitioner
status: draft
description: "Choose and tune the Wegstein, Direct, Broyden and Newton convergence methods in Aspen Plus and fix loops that oscillate or stall."
sources:
  - "Aspen Plus and Aspen HYSYS user guides and help (AspenTech), Seider et al. Product and Process Design Principles"
  - "https://www.aspentech.com"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Wegstein and broyden convergence methods

**Goal:** Choose and tune the Wegstein, Direct, Broyden and Newton convergence methods in Aspen Plus and fix loops that oscillate or stall.

## Steps
1. Start with Wegstein (the usual default for tear streams) for mildly nonlinear recycles; it accelerates successive substitution per variable.
2. If Wegstein oscillates, tighten its acceleration bounds to damp it, or run Direct substitution first to get close; confirm the default bounds in the help for your version.
3. Use Broyden for strongly coupled loops or when design specs sit inside the loop; use Newton for tightly coupled nonlinear sets when the other methods fail.
4. Raise the maximum iterations only after the trend is converging; a flat or diverging error needs a different tear or method, not more iterations.
5. Set tolerance relative to flowsheet scale (confirm the default in the help) and never loosen it just to claim convergence.

## Gotchas
- Different methods can converge to slightly different results at loose tolerance.
- The order of convergence blocks (convergence sequence option) matters as much as the method.

## Verify
- [ ] Error history shows steady decay.
- [ ] Results are unchanged when re-run from a different initial guess.
