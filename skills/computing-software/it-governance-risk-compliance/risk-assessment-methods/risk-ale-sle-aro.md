---
id: computing-software.it-governance-risk-compliance.risk-assessment-methods.risk-ale-sle-aro
name: risk-ale-sle-aro
category: computing-software
field: it-governance-risk-compliance
product: risk-assessment-methods
tags:
- risk-assessment-methods
- risk-ale-sle-aro
level: intro
status: draft
description: Calculate single loss expectancy, annualised rate of occurrence and annualised loss expectancy and use them in a control cost-benefit comparison.
sources:
- https://csrc.nist.gov/pubs/sp/800/30/r1/final
- https://www.fairinstitute.org/
- https://www.isaca.org/credentialing/crisc
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# SLE, ARO and ALE calculations
**Goal:** a simple quantitative baseline.
- SLE = asset value x exposure factor. ALE = SLE x ARO.
- Control worth: ALE before minus ALE after minus annual control cost. Example: SLE 200000, ARO 0.25, ALE 50000; control reducing ARO to 0.05 saves 40000 a year, so it pays if it costs less.
- These exam-style formulas are point estimates; use ranges (FAIR) for decisions with high uncertainty.

## Self-check
Recompute the example by hand and state the break-even control cost.
