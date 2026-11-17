---
id: computing-software.qa-testing-engineering.test-case-design.risk-matrix-likelihood-impact
name: risk-matrix-likelihood-impact
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [risk-matrix, risk-assessment, risk-based-testing, likelihood-impact, risk-scoring]
level: practitioner
status: draft
description: "Score product risks on a likelihood x impact matrix: define scales with concrete anchors, calibrate as a group, compute risk levels and keep scores current."
sources:
  - https://www.istqb.org/certifications/certified-tester-foundation-level
  - https://www.istqb.org/certifications/test-manager
  - https://www.iso.org/standard/72140.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Risk assessment with a likelihood x impact matrix

**Goal:** comparable risk levels, so the team agrees which risks get the most testing (ISTQB CTFL 5.2.3 product risk analysis).

## Define the scales with anchors
**Likelihood** (technical factors): 1 low ... 5 very high
- Anchors: complexity, new technology, team experience, size of change, defect history, number of integrations.
- 5 = "new component, new team, many integrations, history of defects here".

**Impact** (business factors): 1 low ... 5 very high
- Anchors: users affected, financial loss, legal/regulatory, safety, reputation, workaround available.
- 5 = "all customers cannot pay, no workaround, regulatory breach".

Write the anchors down; unanchored scales produce arguments, not scores.

## Score
- Each participant scores privately (planning-poker style), then discuss outliers, then agree.
- Level = likelihood x impact (1-25), or use a 3x3/5x5 lookup grid so 1x5 and 5x1 are treated deliberately.

| | Impact 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|
| L5 | M | M | H | H | H |
| L4 | L | M | M | H | H |
| L3 | L | M | M | M | H |
| L2 | L | L | M | M | M |
| L1 | L | L | L | M | M |

## Qualitative alternative
High/medium/low on each axis is fine for small teams; the discipline of anchors still applies.

## Keep it current
- Rescore when scope changes, after each test cycle (defects found raise likelihood), and before release.
- Show trend: risks moving down as mitigation completes is the release story.

## Gotchas
- Impact is a business call; do not let testers alone score it.
- Multiplying ordinal scales overstates precision; treat the number as a sort key, not a measurement.
- Everything "high" means nothing is; force a distribution if needed.

## Verify
Scales have written anchors, every risk has both scores and a level, and the top 10 risks are agreed by product and engineering.
