---
id: computing-software.qa-testing-engineering.test-case-design.regression-test-selection
name: regression-test-selection
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [regression-testing, regression-test-selection, regression-suite, suite-minimisation, risk-based-regression, test-prioritization]
level: practitioner
status: draft
description: "Select and maintain a regression suite: risk and change-based selection, tiered suites (smoke, core, full), pruning redundant tests and keeping run time bounded."
sources:
  - https://www.istqb.org/certifications/certified-tester-foundation-level
  - https://testing.googleblog.com/2016/05/flaky-tests-at-google-and-how-we.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Regression test selection and suite maintenance

**Goal:** a regression suite that finds regressions fast, without growing until nobody runs it. ISTQB CTFL v4.0 2.2.3.

## Tiering
| Tier | When | Contents | Target time |
|---|---|---|---|
| Smoke | Every deploy | Critical paths up and running | < 5 min |
| Core / PR | Every merge | Changed-area + high-risk tests | < 15 min |
| Full | Nightly / pre-release | Everything automated | hours OK |
| Manual regression | Release | Checklist of non-automatable risks | timeboxed |

## Selection for a change
1. Impact analysis: what code/config/data changed and what depends on it (`change-impact-analysis`).
2. Tests mapped to those areas (tags, traceability, or coverage-based test impact analysis `test-impact-analysis-selective-runs`).
3. Always add: smoke + tests for high-risk features + tests for recently escaped defects.

## Maintenance
- Every escaped defect gets a regression test at the lowest level that would have caught it.
- Quarterly prune: tests that never failed in a year *and* duplicate coverage of lower-level tests are candidates for removal or demotion to nightly.
- Track suite runtime and flake rate; treat them as budgets.

## Gotchas
- "Run everything always" stops scaling; teams then skip the suite entirely.
- Removing tests just because they never fail ignores that some guard rarely changed but critical code. Check risk before pruning.

## Verify
Release-to-release, escaped regressions trend down while suite runtime stays within budget.
