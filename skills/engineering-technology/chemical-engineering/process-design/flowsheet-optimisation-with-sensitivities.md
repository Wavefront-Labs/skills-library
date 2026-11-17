---
id: engineering-technology.chemical-engineering.process-design.flowsheet-optimisation-with-sensitivities
name: flowsheet-optimisation-with-sensitivities
category: engineering-technology
field: chemical-engineering
product: process-design
tags: [chemical-engineering, process-design, pd-debottlenecking-and-optimisation, flowsheet-optimisation-with-sensitivities, flowsheet-optimisation, sensitivity, economic-optimum]
level: practitioner
status: draft
description: "Optimise a flowsheet by choosing decision variables, scanning sensitivities and then optimising the objective with constraints."
sources:
  - "Towler and Sinnott Chemical Engineering Design, Turton et al. Analysis Synthesis and Design of Chemical Processes, Peters Timmerhaus and West Plant Design and Economics"
  - "https://www.aiche.org"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Flowsheet optimisation with sensitivities

**Goal:** Optimise a flowsheet by choosing decision variables, scanning sensitivities and then optimising the objective with constraints.

## Steps
1. Pick an objective (profit or cost per unit product) and decision variables (reflux, conversion, pressure, recycle).
2. Scan one variable at a time to find sensitive variables and the shape of the trade-off.
3. Run the multi-variable optimisation with constraints (purity, flooding, equipment limits).
4. Check the optimum is flat enough to be robust to price and feed changes.
5. Round to practical setpoints and re-verify feasibility.

## Gotchas
- Optimum conditions can sit on a constraint; the constraint is the real result.
- Optimise on a calibrated model.

## Verify
- [ ] Constraints are satisfied.
- [ ] The result is tested against price changes.
