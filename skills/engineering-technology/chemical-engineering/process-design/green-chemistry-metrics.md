---
id: engineering-technology.chemical-engineering.process-design.green-chemistry-metrics
name: green-chemistry-metrics
category: engineering-technology
field: chemical-engineering
product: process-design
tags: [chemical-engineering, process-design, pd-sustainability-and-lca, green-chemistry-metrics, green-chemistry, e-factor, process-mass-intensity, atom-economy]
level: practitioner
status: gated
description: "Calculate E-factor, process mass intensity and atom economy for a process, with clear system boundaries."
sources:
  - "Trost, B.M. (1991) The atom economy, a search for synthetic efficiency, Science 254(5037):1471-1477, https://doi.org/10.1126/science.1962206"
  - "Sheldon, R.A. (2017) The E factor 25 years on, Green Chemistry 19(1):18-43, https://doi.org/10.1039/c6gc02157c"
  - "Jimenez-Gonzalez, C. et al. (2011) Using the right green yardstick: why process mass intensity is used in the pharmaceutical industry, Org. Process Res. Dev. 15(4):912-917, https://doi.org/10.1021/op200097d"
  - "https://www.epa.gov/greenchemistry/basics-green-chemistry"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Green chemistry metrics

**Goal:** Calculate E-factor, process mass intensity and atom economy for a process, with clear system boundaries.

## Steps
1. E-factor = total waste mass / product mass (Sheldon); define whether process water and solvent recovery are included (gated: unconfirmed, source is paywalled or blocked).
2. Process mass intensity (PMI) = total mass of inputs / product mass; PMI = E-factor + 1 when the same boundary is used.
3. Atom economy = molecular weight of the desired product / sum of molecular weights of the reactants x 100 (Trost 1991, Science 254:1471; EPA lists it as green chemistry principle 2) (gated: unconfirmed, source is paywalled or blocked).
4. Report with the boundary (gate-to-gate), basis and water treatment; compare routes on the same boundary.
5. Combine with hazard and energy to avoid shifting burdens.

## Gotchas
- Metrics from different companies are only comparable with the same boundary.
- Whether process water is counted can change PMI strongly; state the treatment.

## Verify
- [ ] PMI minus 1 equals E-factor for the same boundary.
- [ ] Mass balance of inputs and outputs closes.
