---
id: engineering-technology.electrical-engineering.power-system-analysis.reliability-indices
name: reliability-indices
category: engineering-technology
field: electrical-engineering
product: power-system-analysis
tags: [asai, caidi, electrical-engineering, failure-rate-and-outage-data, feeder-automation-benefit, ieee-1366, power-system-analysis, reliability-indices, saidi, saifi]
level: practitioner
status: draft
description: "Compute SAIFI, SAIDI, CAIDI and ASAI for distribution feeders and evaluate the benefit of sectionalising."
sources:
  - "https://standards.ieee.org/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Distribution reliability assessment

- **Indices (IEEE 1366):** `SAIFI = total customer interruptions / customers served`; `SAIDI = sum(restoration time x customers interrupted) / customers served`; `CAIDI = SAIDI / SAIFI`; `ASAI = 1 - SAIDI / (customers x hours in period)`.
- **Example:** 10,000 customers, one outage of 2,000 customers for 90 min and another of 500 customers for 60 min: `SAIFI = 0.25`, `SAIDI = (2000 x 90 + 500 x 60)/10,000 = 21 min`, `CAIDI = 84 min`.
- **Data:** component failure rates (per km-year), repair and switching times, from utility history; separate major event days (IEEE 1366 uses a 2.5 beta statistical method).
- **Predictive method:** series components add failure rates and outage times (radial feeder); parallel paths use Markov or minimal cut sets.
- **Automation benefit:** with N sectionalising switches, only the faulted section stays out for repair time; the rest are restored in switching time. Recompute SAIDI with the shorter times.

**Verify:** back-cast last year's indices from the same model and compare to reported values.

**Scope note:** Professional guidance only: design, selection, settings and sign-off belong to a qualified engineer or licensed electrician working to the code and standard editions adopted in the project jurisdiction. Standard clause numbers, limits and table values cited from memory are unconfirmed against the paywalled text (gated: unconfirmed, source is paywalled or blocked); worked arithmetic was recomputed.
