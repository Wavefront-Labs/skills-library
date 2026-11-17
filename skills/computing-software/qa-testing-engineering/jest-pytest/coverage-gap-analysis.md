---
id: computing-software.qa-testing-engineering.jest-pytest.coverage-gap-analysis
name: coverage-gap-analysis
category: computing-software
field: qa-testing-engineering
product: jest-pytest
tags: [coverage-gap-analysis, code-coverage, white-box-testing, branch-coverage, untested-code, coverage-report]
level: practitioner
status: verified
description: "Use coverage reports to find what is untested: read missing branches, prioritise gaps by risk and churn, and decide which gaps deserve tests and which are noise."
sources:
  - https://coverage.readthedocs.io/en/latest/branch.html
  - https://martinfowler.com/bliki/TestCoverage.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Coverage gap analysis

**Goal:** use coverage to find important untested code, not to chase a percentage. Fowler, *TestCoverage*.

## Produce useful reports
- Python: `pytest --cov=src --cov-branch --cov-report=html --cov-report=term-missing:skip-covered`.
- JS: `jest --coverage` or `vitest run --coverage` (V8/Istanbul) -> Jest writes `coverage/lcov-report/index.html`; Vitest's default html reporter writes `coverage/index.html` (both run).
- Java: JaCoCo HTML (`mvn verify` with jacoco plugin) showing instruction and branch coverage per line (JaCoCo counters page: red diamond = no branch executed, yellow = only some branches executed, green = all).
Branch coverage matters more than lines: a covered `if` line can hide an untested `else`.

## Prioritise gaps
1. Sort files by missed branches, then overlay **risk** (payments, auth, data deletion), **churn** (`git log --since=6.months --name-only`), and **defect history**.
2. Look inside for: error handling (`except`/`catch` blocks never run), boundary branches, feature-flag off paths, fallback code, permission denials.
3. Ignore or exclude deliberately: generated code, trivial getters, debug-only code (`# pragma: no cover`, `/* istanbul ignore next */`, JaCoCo excludes) with a reason.

## Write the right test
For each important gap, design a test from the *requirement* that the branch implements (not "call the function to turn the line green"), and assert behaviour.

## Gotchas
- 100% coverage with weak assertions finds nothing; mutation testing (for example Stryker for JS, mutmut for Python) checks assertion strength.
- Coverage from E2E tests is broad but shallow; measure per test level if you can.
- Unreachable code found by coverage may be dead code: delete it instead of testing it.

## Verify
The top-10 risk-weighted gaps each have a test or a documented decision; branch coverage of critical modules rises.
