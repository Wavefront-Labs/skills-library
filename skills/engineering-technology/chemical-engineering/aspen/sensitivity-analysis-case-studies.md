---
id: engineering-technology.chemical-engineering.aspen.sensitivity-analysis-case-studies
name: sensitivity-analysis-case-studies
category: engineering-technology
field: chemical-engineering
product: aspen
tags: [chemical-engineering, aspen, aspen-sensitivity-and-optimisation, sensitivity-analysis-case-studies, sensitivity-analysis, case-study, parametric-study]
level: practitioner
status: draft
description: "Run Aspen Plus Sensitivity blocks and case studies: define varied inputs, sampled results and tabulate outputs for design decisions."
sources:
  - "Aspen Plus and Aspen HYSYS user guides and help (AspenTech), Seider et al. Product and Process Design Principles"
  - "https://www.aspentech.com"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Sensitivity analysis case studies

**Goal:** Run Aspen Plus Sensitivity blocks and case studies: define varied inputs, sampled results and tabulate outputs for design decisions.

## Steps
1. Create the Sensitivity block (Model Analysis Tools): Vary the input (for example reflux ratio or reactor temperature) over a range or a list of values.
2. Define the sampled results (flows, duties, purity) and optionally a Fortran expression for derived values such as cost or yield.
3. Tabulate the results and plot the table columns against the varied variable.
4. Keep the base case converged, and use a moderate step so each point starts from a nearby solution.
5. Use several blocks or multiple varied variables to build a grid; keep the number of points manageable.

## Gotchas
- A failed point does not stop the rest; check each row for convergence status.
- Sensitivity does not change the base case; use a Design Spec to fix a target.

## Verify
- [ ] All table rows are converged.
- [ ] Trends look physically consistent (for example duty rises with reflux).
