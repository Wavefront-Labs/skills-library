---
id: computing-software.it-governance-risk-compliance.risk-assessment-methods.risk-matrix-scoring
name: risk-matrix-scoring
category: computing-software
field: it-governance-risk-compliance
product: risk-assessment-methods
tags:
- risk-assessment-methods
- risk-matrix-scoring
- risk-quant-qual
level: practitioner
status: draft
description: Design a likelihood-by-impact matrix with defined scales and avoid common scoring errors such as range compression and ordinal arithmetic.
sources:
- https://csrc.nist.gov/pubs/sp/800/30/r1/final
- https://www.fairinstitute.org/
- https://www.isaca.org/credentialing/crisc
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Risk matrix design and pitfalls
**Goal:** a matrix that ranks risks sensibly.
- Define each likelihood level (frequency per year bands) and impact level (financial, operational, legal, safety, reputational) in measurable terms.
- 5x5 is common; assign colours to match appetite; document risk score = L x I only as a ranking aid.
- Pitfalls: multiplying ordinal ranks, rating clustering in the middle, ignoring uncertainty, summing scores across risks.

## Self-check
Check that two risks with the same score differ only in ways management accepts.
