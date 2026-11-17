---
id: computing-software.qa-testing-engineering.test-automation.flaky-test-detection
name: flaky-test-detection
category: computing-software
field: qa-testing-engineering
product: test-automation
tags: [flaky-test-detection, flaky-tests, test-reliability, rerun-analysis, ci-analytics]
level: practitioner
status: gated
description: "Detect flaky tests systematically: rerun-on-failure signals, repeat runs on unchanged code, CI history flip rates, and dashboards that rank tests by flakiness."
sources:
  - https://playwright.dev/docs/test-retries
  - https://docs.pytest.org/en/stable/explanation/flaky.html
  - https://testing.googleblog.com/2016/05/flaky-tests-at-google-and-how-we.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Detecting flaky tests

**Goal:** know which tests are flaky before people learn to ignore red builds. A flaky test passes and fails on the same code.

## Signals
1. **Retry passes**: test failed then passed on retry in the same run. Playwright reports these as `flaky`; pytest-rerunfailures marks `RERUN`; Jest `jest.retryTimes(n, { logErrorsBeforeRetry: true })`; Cypress `retries` with Cloud flake flags.
2. **Repeat on unchanged code**:
```bash
npx playwright test --repeat-each=50 --workers=8 tests/checkout.spec.ts
pytest --count=50 -p no:randomly tests/test_sync.py          # pytest-repeat
pytest -p randomly --flake-finder --flake-runs=50            # pytest-flakefinder
mvn -Dsurefire.rerunFailingTestsCount=2 test                 # Surefire reports flakes
```
Run checks: with `--retries=2` Playwright's summary printed `1 flaky` for a test that failed once and passed on retry; pytest-rerunfailures 16.7 (`--reruns 2 -rR`) printed `RERUN rr/test_fl.py::test_flaky` and `1 passed, 1 rerun`; `jest.retryTimes(2, { logErrorsBeforeRetry: true })` made a first-attempt failure pass in Jest 30.5.2 (`Tests: 1 passed`). The Surefire line was not run (gated: unconfirmed, source is paywalled or blocked); reason: no Maven here.
3. **History flip rate**: from stored JUnit XML per commit, `flip rate = state changes / runs` on the same test over a window; or failures on commits that later pass without code change.

## Tooling
Datadog CI Test Visibility, BuildPulse, Buildkite Test Engine, Gradle Develocity, Cypress Cloud, Allure history and TeamCity all flag flaky tests from history (vendor feature claims, not checked here: gated: unconfirmed, source is paywalled or blocked). Self-hosted: store JUnit XML in a table `(test, commit, status, run_id)` and query.

## Nightly flake hunt
Scheduled job runs the full suite N times on main HEAD with random order and parallel workers, publishes a ranked list with owners.

## Policy
- New tests run e.g. 20x in CI before merge (`--repeat-each` on changed spec files).
- Any test flagged flaky gets a ticket and owner; quarantine if it blocks others (see quarantine skill).

## Gotchas
- Retries hide flakiness if nobody reads the flaky count; publish it.
- Infra failures (runner died) are not test flakiness; classify separately.

## Verify
A ranked flaky list exists and refreshes automatically, and the flaky rate (flaky tests / total) is tracked over time.
