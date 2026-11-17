---
id: computing-software.qa-testing-engineering.test-case-design.risk-monitoring-and-reassessment
name: risk-monitoring-and-reassessment
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [risk-monitoring, risk-reassessment, risk-based-testing, residual-risk, test-control]
level: practitioner
status: draft
description: "Monitor product risks during testing: reassess likelihood from defect data and changes, adjust test depth, track risk burndown and report residual risk."
sources:
  - https://www.istqb.org/certifications/certified-tester-foundation-level
  - https://www.istqb.org/certifications/certified-tester-advanced-level-test-analyst-ctal-ta
  - https://www.istqb.org/certifications/certified-tester-advanced-level-test-management-ctal-tm
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Risk monitoring and re-assessment

**Goal:** the risk analysis stays true while testing runs, so test effort moves to where risk actually is (ISTQB CTFL 5.2.4 risk monitoring).

## Triggers to re-assess
- Defect clusters in an area (more or more severe defects than expected raise likelihood).
- Code churn or late changes in an area (from Git or release notes).
- New requirements, architecture changes, new integrations.
- Production incidents or support tickets in similar features.
- An area passing cleanly with good coverage (may lower likelihood).

## Routine
1. At a fixed cadence (each sprint or week) review the register with the product owner and dev lead.
2. Update likelihood/impact with the evidence; note the reason.
3. Adjust tests: add depth or techniques to rising risks, reduce for falling ones; schedule re-testing.
4. Track **risk burndown:** sum of open risk scores (or count of open high risks) over time; it should fall toward the release.
5. Identify emerging risks and add them.

## Residual risk reporting
For the release decision list: risks not fully tested, open defects mapped to risks, and accepted risks with who accepted them.

## Verify
The register shows dated re-assessments with evidence, test changes trace to them, and the risk burndown chart and residual risk list appear in status and completion reports.
