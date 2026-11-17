---
id: computing-software.qa-testing-engineering.test-case-design.reliability-growth-and-mtbf
name: reliability-growth-and-mtbf
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [mtbf, reliability-growth, reliability-testing, mttr, availability-measurement, operational-profile, istqb-tta]
level: practitioner
status: docs-checked
description: "Measure reliability: MTBF/MTTR and availability from test and production data, operational-profile-based testing, and reliability growth tracking across releases."
sources:
  - https://sre.google/sre-book/embracing-risk/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Reliability growth and MTBF

**Goal:** quantify reliability and show whether it improves.

## Measures
- **MTBF** = total operating time / number of failures. **MTTR** = mean time to restore. **Availability** = MTBF / (MTBF + MTTR), or successful requests / total (SRE style).
- Failure intensity (failures per hour of operation) over time.

## Operational profile testing
1. Build the usage profile: which operations, how often (from production logs/analytics).
2. Run long tests that execute operations in those proportions (soak-style load with realistic mix).
3. Record every failure with timestamp and operation; compute MTBF and failure intensity.

## Reliability growth
- Track failure intensity per build during system test; plot cumulative failures vs test time. A flattening curve indicates growth; a straight line means you are still finding failures at a constant rate, so stopping now is risky.
- In production: incidents per month, SLO error budget burn, MTTR trend.

## Gotchas
- MTBF from a test environment with a non-representative profile says little about production.
- Counting all failures equally hides severity; track by severity class.

## Verify
A reliability report with the profile used, test hours, failure counts by severity, MTBF/availability and the trend vs previous release.

## Checked

2026-10-28. Confirmed: SRE Book embracing-risk: request-based availability is the proportion of successful requests over a window; error budgets. MTBF/MTTR/availability formulas are standard arithmetic definitions. Removed: Syllabus section number and the named growth models (Musa, Goel-Okumoto).

Method: documentation only; no commands were run.
