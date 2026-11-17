---
id: computing-software.qa-testing-engineering.test-case-design.ratio-and-extrapolation-estimation
name: ratio-and-extrapolation-estimation
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [ratio-based-estimation, extrapolation-estimation, test-estimation, metrics-based-estimation, historical-data, istqb]
level: practitioner
status: draft
description: "Estimate test effort from data: ratio-based (test-to-dev effort from past projects) and extrapolation (measure early iterations and project forward)."
sources:
  - https://www.istqb.org/certifications/certified-tester-foundation-level
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Ratio-based and extrapolation estimation

**Goal:** metrics-based estimates grounded in your own history. ISTQB CTFL v4.0 5.1.4.

## Ratio-based
1. From past similar projects, compute ratios: test effort / dev effort (e.g. 3:5), test cases per requirement, defects per KLOC or per story point, retest cycles per release.
2. Apply to the new project's known size: dev estimate 500 days x 3/5 = 300 test days.
3. Adjust for known differences (new technology, higher regulatory need) and state the adjustment.

## Extrapolation
1. Measure the first iterations: test effort per story point, defects found per day, test cases executed per tester-day.
2. Project the rest: remaining points x measured rate.
3. Re-estimate after each iteration (agile velocity is extrapolation).

Example: first 3 sprints, 18 test hours per 10 points; remaining 240 points -> ~430 hours.

## Data to keep
Per release: effort by activity, test counts, defect counts by phase found, scope size. Without this, ratio estimation is guesswork.

## Gotchas
- Ratios from a different context (team, domain, tooling) mislead.
- Early iterations are often unrepresentative (setup work, easy stories); use a rolling window.

## Verify
Compare the estimate with an expert-based one; large differences mean assumptions need discussion.
