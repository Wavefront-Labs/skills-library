---
id: computing-software.qa-testing-engineering.test-case-design.cost-of-quality-and-value-of-testing
name: cost-of-quality-and-value-of-testing
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [cost-of-quality, cost-of-defects, testing-principles, testing-objectives, business-case]
level: practitioner
status: draft
description: "Explain the value and cost of testing with the cost-of-quality model (prevention, appraisal, internal and external failure) and defect cost by phase found."
sources:
  - https://www.istqb.org/certifications/certified-tester-foundation-level
  - https://asq.org/quality-resources/cost-of-quality
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Cost of quality and the value of testing

**Goal:** justify testing investment in money terms stakeholders accept.

## Cost of quality (ASQ / Juran)
| Category | Examples in software |
|---|---|
| Prevention | training, requirement reviews, coding standards, test design early, static analysis setup |
| Appraisal | test execution, reviews, CI runs, test environments, audits |
| Internal failure | rework of defects found before release, re-testing, delayed releases |
| External failure | incidents, hotfixes, support calls, refunds, SLA penalties, churn, reputational and legal cost |

Cost of poor quality = internal + external failure. Shifting spend into prevention and early appraisal usually lowers the total.

## Defect cost by phase
A defect costs more the later it is found (rework of dependent artefacts, release overhead, customer impact). Use your own data where possible:
1. Tag defects with phase introduced and phase found.
2. Estimate fix effort per phase found (hours x rate) plus external costs for production defects (incident hours, credits).
3. Show the ratio, e.g. "average 2 h when found in review, 30 h + customer credits when found in production".

## Making the case
- Express value as risk reduced: probability x impact of failures your testing targets.
- Include testing's other value: information for release decisions, compliance evidence, confidence to refactor.
- Compare scenarios: current spend vs adding N hours of review/automation, with expected reduction in escaped defects.

## Gotchas
- The often-quoted "100x" multiplier is folklore with weak evidence; use internal data or ranges.
- Testing cannot prove absence of defects, so value is probabilistic; say so.
- Over-testing has a cost too: low-risk areas can take light testing.

## Verify
A one-page cost-of-quality table with your own numbers for the last quarter, and a proposal tied to the largest failure-cost category.
