---
id: computing-software.qa-testing-engineering.test-case-design.coverage-and-defect-exit-thresholds
name: coverage-and-defect-exit-thresholds
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [exit-thresholds, exit-criteria, test-completion, coverage-thresholds, istqb, ctfl]
level: practitioner
status: draft
description: "Define measurable exit criteria: requirement and risk coverage, pass rates, open defect limits by severity, code coverage floors, and how to evaluate them at the gate."
sources:
  - https://www.istqb.org/certifications/certified-tester-foundation-level
  - https://www.istqb.org/certifications/certified-tester-advanced-level-test-management-ctal-tm
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Coverage and defect thresholds as exit criteria

**Goal:** "testing is done" becomes a measurable check agreed before testing starts (ISTQB CTFL 5.1.3), not a mood on release day.

## Typical exit criteria set

| Criterion | Example threshold |
|---|---|
| Requirement coverage | 100% of committed requirements have executed tests |
| Risk coverage | all high risks tested to planned depth; medium at least core tests |
| Execution | 100% of planned tests executed; pass rate >= 95% with every failure triaged |
| Open defects | 0 critical, 0 high; medium <= 5 each with an agreed workaround |
| Regression | full regression suite green on the release candidate build |
| Code coverage | changed-line coverage >= 80% (overall coverage as trend, not gate) |
| Non-functional | performance SLO tests passed; no high accessibility or security findings |
| Defect trend | arrival rate flattening: fewer new defects than closed for the last N days |

## Writing good criteria
- Measurable from a tool report, not judgement ("most tests passed" fails this).
- Tied to risk: thresholds stricter for high-risk components.
- Agreed and signed by product owner, dev and QA in the test plan.
- Includes which build/environment the measurements must come from.

## At the gate
Produce a one-page evaluation: each criterion, actual value, met/not met, evidence link. Unmet criteria go to a waiver decision, not silent acceptance.

## Gotchas
- Pass-rate thresholds invite deleting or skipping failing tests; count skipped and quarantined tests separately.
- Severity inflation/deflation near release: audit severity changes in the last week.

## Verify
The test plan lists measurable criteria with thresholds, and the gate evaluation shows actual vs threshold with evidence for each.
