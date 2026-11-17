---
id: computing-software.qa-testing-engineering.test-case-design.test-metrics-and-defect-escape-rate
name: test-metrics-and-defect-escape-rate
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [test-metrics, defect-escape-rate, defect-density, test-coverage-metrics, quality-metrics, gqm]
level: practitioner
status: draft
description: "Choose and compute test metrics that drive decisions: pass rate, requirement and code coverage, defect density, escape rate (DDE), and avoid vanity numbers."
sources:
  - https://www.istqb.org/certifications/certified-tester-foundation-level
  - https://www.istqb.org/certifications/test-manager
  - https://www.cs.umd.edu/~basili/publications/technical/T89.pdf
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Test metrics

**Goal:** a handful of metrics that answer real questions about progress and quality (ISTQB CTFL 5.3.1). Start from Goal-Question-Metric: name the decision, then the metric.

## Core metrics and formulas
| Metric | Formula | Answers |
|---|---|---|
| Test execution progress | executed / planned | Are we on track? |
| Pass rate | passed / executed | Is the build healthy? |
| Requirement/risk coverage | requirements with passing tests / total | What is verified? |
| Code coverage (branch) | from coverage tools | What code is unexercised? |
| Defect density | defects / size (KLOC, story points, components) | Where do defects cluster? |
| Defect detection effectiveness (DDE) | found before release / (before + after release) | How good is our testing? |
| Defect escape rate | 1 - DDE, or escaped defects per release | What reaches customers? |
| Defect find/fix rate | new vs closed per day | Are we converging? |
| Mean time to detect / repair | | How fast is the feedback? |
| Flaky rate | tests with mixed results on same commit / total | Can we trust the suite? |

## Escape rate in practice
- Tag each production defect with the release and the phase it should have been caught in.
- Measure per quarter; split by severity (escaped critical defects is the number that matters).
- Example: 46 found in test, 4 in production -> DDE = 46/50 = 92%.

## Rules
- Pair metrics to avoid gaming: pass rate with coverage; velocity with escaped defects.
- Trend over time beats single values.
- Never use metrics to rate individual testers; behaviour will optimise the number.

## Vanity metrics to avoid
Number of test cases, number of bugs raised by person, 100% pass rate on a suite that tests nothing new.

## Verify
Each metric on the report has a named decision it informs, a definition with a formula, and a data source that is automated.
