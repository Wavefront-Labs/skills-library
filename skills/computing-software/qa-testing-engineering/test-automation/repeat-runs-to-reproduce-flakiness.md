---
id: computing-software.qa-testing-engineering.test-automation.repeat-runs-to-reproduce-flakiness
name: repeat-runs-to-reproduce-flakiness
category: computing-software
field: qa-testing-engineering
product: test-automation
tags: [repeat-each, pytest-repeat, flaky-test-reproduction, stress-repeat, flaky-tests]
level: practitioner
status: gated
description: "Reproduce flaky tests by stress-repeating them: Playwright --repeat-each, pytest-repeat/pytest-flakefinder, Jest/JUnit repeats, CPU stress, parallel load and randomised order."
sources:
  - https://playwright.dev/docs/test-cli
  - https://pypi.org/project/pytest-repeat/
  - https://junit.org/junit5/docs/current/user-guide/#writing-tests-repeated-tests
  - https://github.com/dropbox/pytest-flakefinder
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Stress-repeating a test to reproduce flakiness

**Goal:** turn "fails 1 in 50 in CI" into a local, repeatable failure you can debug.

## Repeat commands
```bash
# Playwright
npx playwright test tests/cart.spec.ts --repeat-each=50 --retries=0 --workers=4
# pytest
pip install pytest-repeat
pytest tests/test_cart.py::test_total --count=100 -x -p no:randomly
pytest --count=20 --repeat-scope=session tests/
# pytest-flakefinder (re-runs each test N times in one session)
pytest --flake-finder --flake-runs=50 tests/test_cart.py
# Jest (no built-in flag): loop
for i in $(seq 50); do npx jest cart.test.ts --silent || break; done
# JUnit 5: @RepeatedTest(100) temporarily, or Maven
mvn test -Dtest=CartTest -Dsurefire.rerunFailingTestsCount=0 -Dsurefire.runOrder=random
# Go
go test -run TestCart -count=200 -race ./...
```
Checked on pytest 9.1 (pytest-repeat 0.9.4, pytest-flakefinder 1.1.0), Playwright 1.x test runner and Jest 30.5.2: a test failing about 5% of the time failed within 100 `--count` repeats with `-x` stopping at `test_total[5-100]`; `--count=20 --repeat-scope=session` ran 40 items for 2 tests; `--flake-finder --flake-runs=50` ran 100 items for 2 tests; `playwright test --repeat-each=50 --retries=0 --workers=4` ran 150 tests for 3. The Go command fails on a machine without a C compiler (`go: -race requires cgo; enable cgo by setting CGO_ENABLED=1`); without `-race` the `-count=200` run passed. The Maven/Surefire line, `stress-ng` and `@RepeatedTest` were not run (gated: unconfirmed, source is paywalled or blocked). Reason: no Maven or Linux host here.

## Amplify conditions that cause flakes
- **CPU contention:** run with more workers than cores, or `stress-ng --cpu 4` alongside; timing bugs surface faster.
- **Parallelism:** run the whole file/suite repeatedly with full parallelism to expose shared-state collisions.
- **Order:** pytest-randomly (`-p randomly` is a no-op once installed; it prints `Using --randomly-seed=N` and `-p randomly --randomly-seed=N` replays), pytest-random-order (`--random-order`, `--random-order-seed`), Jest `--randomize` (shuffles tests within a file; prints `Seed:` and `--seed` replays it), Surefire `runOrder=random`; record the seed that fails.
- **Slow network:** add latency (route delays, Toxiproxy) to expose missing waits.

## Capture evidence when it fails
Traces/videos on failure (Playwright `trace: 'retain-on-failure'`), verbose logs, seed values, timestamps. Stop at first failure (`-x`, `--max-failures=1`, both in `playwright test --help`) to keep artifacts small.

## Estimating rate
Failures f in n runs: rate ≈ f/n. To be ~95% confident a fix works for a 2% flake, you need roughly 150 clean runs (3/0.02, rule of three).

## Gotchas
- Repeating with retries enabled hides the flake; set retries to 0.
- Repeats sharing external state (same DB rows) may fail for reasons unrelated to the original flake.

## Verify
After the fix, the same repeat command passes the computed number of runs with zero failures.
