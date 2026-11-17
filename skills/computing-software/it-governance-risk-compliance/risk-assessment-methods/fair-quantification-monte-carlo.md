---
id: computing-software.it-governance-risk-compliance.risk-assessment-methods.fair-quantification-monte-carlo
name: fair-quantification-monte-carlo
category: computing-software
field: it-governance-risk-compliance
product: risk-assessment-methods
tags:
- risk-assessment-methods
- fair-quantification-monte-carlo
level: advanced
status: draft
description: Produce FAIR estimates as calibrated min / most likely / max ranges and simulate loss distributions with Monte Carlo to report annualised loss exposure.
sources:
- https://csrc.nist.gov/pubs/sp/800/30/r1/final
- https://www.fairinstitute.org/
- https://www.isaca.org/credentialing/crisc
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Calibrated estimates and Monte Carlo
**Goal:** ranges with defensible inputs.
- Elicit calibrated ranges from SMEs (90% confidence intervals); use PERT or lognormal distributions; use data (incident history, industry loss data) where available.
- Simulate thousands of trials: sample frequency and magnitude per trial; report mean, median and 90th percentile of annual loss, and loss exceedance curve.
- Document sources and assumptions per input; sensitivity analysis shows which inputs drive the result.
- Tools: open FAIR-based spreadsheets or scripts; any language works for the simulation.

## Self-check
Re-run with a different seed and confirm headline numbers are stable to the reported precision.
