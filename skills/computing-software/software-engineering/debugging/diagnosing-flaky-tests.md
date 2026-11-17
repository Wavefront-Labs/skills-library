---
id: computing-software.software-engineering.debugging.diagnosing-flaky-tests
name: diagnosing-flaky-tests
category: computing-software
field: software-engineering
product: debugging
tags: [debugging, production-debugging, flaky-tests, test-isolation, quarantine, nondeterminism, ci-reliability]
level: practitioner
status: draft
description: "Diagnose and fix flaky tests: reproduce with repetition and random order, classify root causes (timing, order, shared state, time, network), quarantine policy and tracking."
sources:
  - https://testing.googleblog.com/2016/05/flaky-tests-at-google-and-how-we.html
  - https://docs.pytest.org/en/stable/explanation/flaky.html
  - https://engineering.atspotify.com/2019/11/test-flakiness-methods-for-identifying-and-dealing-with-flaky-tests/
  - https://www.jetbrains.com/help/teamcity/test-flakiness.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Diagnosing flaky tests

A flaky test passes and fails on the same code. Each one trains the team to ignore red builds.

## 1. Reproduce
```bash
pytest tests/test_orders.py::test_refund --count=200 -x          # pytest-repeat
pytest -p randomly --randomly-seed=12345                          # pytest-randomly; reuse the failing seed
go test -run TestRefund -count=500 -race ./orders/
mvn -Dsurefire.rerunFailingTestsCount=0 -Dtest=RefundTest -Dsurefire.runOrder=random test
npx jest --runInBand vs default parallel ; npx playwright test --repeat-each=50 --workers=8
dotnet test --filter Refund -- RunConfiguration.TestSessionTimeout=...  (loop in a shell)
```
Run under load (`stress-ng --cpu 8` alongside) to expose timing assumptions. Compare: passes alone, fails in suite -> order/shared state; fails only in parallel -> shared resources; fails only in CI -> environment.

## 2. Classify the root cause
| Cause | Signs | Fix |
|---|---|---|
| Async waits / sleeps | `sleep(1)` then assert; timeouts | wait for a condition (`await expect(locator).toBeVisible()`, Awaitility, polling with deadline) |
| Order dependence | fails with certain seeds | each test sets up and tears down its own state; no reliance on another test's data |
| Shared state | globals, singletons, static caches, env vars, shared DB rows | reset in fixtures; unique data per test (random ids, per-test schemas, Testcontainers) |
| Time | fails near midnight, month end, DST, different TZ | inject a clock; freeze time (freezegun, `TimeProvider`, `Clock.fixed`, sinon fake timers) |
| Randomness | random data without seed | seed and log the seed; property-test shrinking |
| Concurrency | race detector hits, intermittent deadlocks | fix the race in code (often a real bug), not the test |
| Network / external | DNS, third-party APIs, rate limits | stub at the boundary (WireMock, MSW, respx); no live internet in unit tests |
| Resource leaks | ports in use, file handles, threads from earlier tests | ephemeral ports (`:0`), close resources, per-test temp dirs |
| Unordered collections | asserting list order from a set/map/DB query without ORDER BY | sort or compare as sets |
| Floating point | exact equality | tolerance (`pytest.approx`) |

## 3. Policy
- Track flakiness: CI test analytics (BuildPulse, Datadog CI Visibility, GitHub/GitLab flaky test reports, TeamCity flaky detection, JUnit XML history).
- **Quarantine** a flaky test immediately (skip with a ticket link, or a separate non-blocking job) so the main build stays trustworthy; fix or delete within a fixed SLA (one to two weeks). Never just add retries and forget.
- Automatic retry (`pytest-rerunfailures`, Surefire `rerunFailingTestsCount`, Playwright `retries`) is a mitigation that must still report the flake.
- The flaky test may be exposing a real production race - check before "fixing the test".

## Verify
- [ ] Fixed test passes 500+ repetitions, in random order, in parallel, under CPU stress.
- [ ] Quarantine list has owners and dates; trend of flaky count is going down.
