---
id: computing-software.qa-testing-engineering.test-case-design.mapping-risk-to-test-depth
name: mapping-risk-to-test-depth
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [risk-mitigation, test-depth-by-risk, risk-based-testing, test-strategy, coverage-targets]
level: practitioner
status: docs-checked
description: "Turn risk levels into test effort: map each level to techniques, coverage, tester skill, independence and test types, then execute in risk order."
sources:
  - https://www.istqb.org/certifications/certified-tester-foundation-level
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Mapping risk levels to test depth and techniques

**Goal:** high risks get rigorous, early and independent testing; low risks get just enough. This is risk control in ISTQB CTFL 5.2.4.

## What the risk level drives
Risk level is likelihood times impact (quantitative) or read from a risk matrix (qualitative). Product risk analysis results are used to set, per risk:
- test scope, and the test levels and test types to perform;
- the test techniques and the coverage to be achieved;
- the estimated test effort per task;
- test priority, so critical defects are found as early as possible;
- whether activities other than testing could reduce the risk.

Write your own table with the techniques and coverage you choose for each level; the syllabus gives no numeric targets.

## Mitigation by testing (CTFL 5.2.4)
- Select testers with the right experience and skills for the risk type.
- Apply an appropriate level of independence of testing.
- Perform reviews and static analysis.
- Apply appropriate techniques and coverage levels.
- Apply test types addressing the affected quality characteristics.
- Perform dynamic testing, including regression testing.
Other responses to a risk are risk acceptance, risk transfer or a contingency plan. Risk monitoring checks that mitigation is effective and identifies emerging risks.

## Traceability
Each test case/charter is tagged with risk ids (`@risk-R12`). Report coverage by risk: tests planned, run, passed, open defects. This becomes the residual risk report.

## Ordering
Risk-based prioritisation: the order of test execution follows the risk analysis, and test cases covering the most important risks run first.

## Verify
Every high risk has named tests at the depth you chose, tests are tagged with risk ids, and the run order follows risk level.

## Checked
2026-11-01. Confirmed against ISTQB CTFL Syllabus v4.0.1 (2024-09-15), sections 5.2.3, 5.2.4 and 5.1 (risk-based prioritisation): uses of risk analysis, quantitative and qualitative risk level, mitigation-by-testing list, risk monitoring, response options. Removed (not in the syllabus): the numeric coverage targets and per-level table, security/performance mitigations, ISO and test-manager sources.
Method: documentation only; no commands were run.
