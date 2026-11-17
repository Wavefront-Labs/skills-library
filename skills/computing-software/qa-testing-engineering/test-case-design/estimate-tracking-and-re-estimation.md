---
id: computing-software.qa-testing-engineering.test-case-design.estimate-tracking-and-re-estimation
name: estimate-tracking-and-re-estimation
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [estimate-tracking, re-estimation, test-estimation, earned-value, test-control]
level: practitioner
status: draft
description: "Track test effort actuals against estimates, compute variance and earned value, re-estimate remaining work and feed accuracy back into future estimates."
sources:
  - https://www.istqb.org/certifications/certified-tester-foundation-level
  - https://www.istqb.org/certifications/certified-tester-advanced-level-test-management-ctal-tm
  - https://www.pmi.org/learning/library/earned-value-management-systems-analysis-8026
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Tracking actuals and re-estimating

**Goal:** know early when the test estimate is wrong, re-forecast honestly, and make the next estimate better.

## Track
- Log effort against the estimate's work breakdown items (test design, environment setup, execution, retest, reporting), not one bucket.
- Weekly: planned vs actual hours, test cases designed/executed vs plan, defects found and retests.

## Measure variance
- Effort variance % = (actual - estimate) / estimate per item.
- Simple earned value for testing: planned value (PV) = planned tests executed by today, earned value (EV) = tests actually executed and passed or completed, actual cost (AC) = hours spent. Schedule performance SPI = EV/PV, cost performance CPI = EV/AC.
- Estimate at completion: EAC = budget / CPI when current performance is expected to continue.

## Re-estimate
- Trigger: variance beyond a threshold (e.g. 15%), scope change, an assumption broken (environment late, defect rates above plan).
- Re-estimate remaining work bottom-up using observed rates (hours per test case, retests per defect), not the original assumptions.
- Communicate the new range, the cause and options (cut scope by risk, add people, move date); record the decision.

## Learn
At completion, store estimate vs actual per item with the factors (team, domain, tooling). Use the ratio to calibrate future productivity factors and analogy estimates.

## Verify
Weekly reports show variance and SPI/CPI, every re-estimate states its trigger and new range, and the project closure record holds estimate vs actual per item.
