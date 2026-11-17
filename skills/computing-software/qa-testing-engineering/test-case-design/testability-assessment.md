---
id: computing-software.qa-testing-engineering.test-case-design.testability-assessment
name: testability-assessment
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [testability-assessment, maintainability-testing, analysability, observability-for-testing, controllability, design-for-testability]
level: practitioner
status: draft
description: "Assess and improve testability: controllability, observability, isolatability, test hooks and seams, with concrete requests to the development team."
sources:
  - https://www.istqb.org/certifications/certified-tester-advanced-level-technical-test-analyst-ctal-tta-v4-0
  - https://www.satisfice.com/download/heuristics-of-software-testability
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Testability and analysability assessment

**Goal:** make the system easier to test and diagnose. CTAL-TTA v4.0 4.5 (maintainability: analysability, testability); Bach, *Heuristics of Software Testability*.

## Dimensions and what to ask for
| Dimension | Symptom of poor testability | Request |
|---|---|---|
| Controllability | Can't set state without long UI flows | Test data API, seed endpoints (non-prod only), feature flag overrides |
| Observability | Can't see why something failed | Structured logs with correlation ids, health/version endpoints, events in a queryable store |
| Isolatability | Can't test a part without everything | Dependency injection, configurable endpoints for third parties |
| Determinism | Random/time-dependent results | Injectable clock and random seed |
| Stable identifiers | Selectors break with each UI change | `data-testid` / accessible names |
| Simplicity | Huge functions, unclear contracts | Smaller units, documented APIs |

## Analysability
Can an engineer diagnose a production failure quickly? Check: error messages actionable, logs contain context, traces span services, dashboards for key flows.

## Procedure
Score each dimension 1-5 for the main components, list the top 3 blockers with cost of not fixing (hours of test effort, flaky tests), and raise them as backlog items.

## Gotchas
- Test-only endpoints must be disabled in production by build/config, and tested to be disabled.

## Verify
Track test setup time and flaky-test count before and after the testability items land.
