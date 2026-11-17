---
id: computing-software.qa-testing-engineering.test-automation.suite-strategy-and-flaky-test-control
name: suite-strategy-and-flaky-test-control
category: computing-software
field: qa-testing-engineering
product: test-automation
tags: [test-automation, test-strategy, test-pyramid, testing-trophy, unit-tests, integration-tests, contract-testing, e2e-testing, flaky-tests, flakiness, quarantine, test-isolation, test-data, page-object-model, ci, continuous-integration, pipeline, shift-left, test-impact, parallelization, sharding, test-retries, test-maintenance, qa-strategy]
level: practitioner
status: draft
description: "Tool-agnostic strategy for a sustainable automated suite: layer tests by the pyramid, isolate test data, wire suites into CI stages with time budgets, and find, triage and fix flaky tests."
sources: ["https://martinfowler.com/articles/practical-test-pyramid.html", "https://testing.googleblog.com/2016/05/flaky-tests-at-google-and-how-we.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Test automation strategy and flaky-test control

**Goal:** an automated suite the team trusts — fast enough to run on every change,
red only when something is really broken, and cheap to maintain as the product changes.

## 1. Put each check at the lowest layer that can catch the bug
| Layer | Checks | Speed | Typical share |
|---|---|---|---|
| Unit | Logic, edge cases, error handling | ms | most tests |
| Integration / component | Your code + a real DB, queue, framework wiring; one service via its API | 10s–100s ms | a solid middle |
| Contract | Consumer/provider agree on API shape (e.g. Pact) | fast | per service pair |
| End-to-end (UI) | A few critical user journeys through the deployed stack | seconds–minutes | a handful to dozens |

The ratios are a heuristic, not a law ("testing trophy" variants weight integration
more). The real rule: **if a lower-level test could catch it, don't write it as E2E.**
Validation rules for a form field are unit tests; "a customer can buy something" is E2E.
Every E2E test should map to a journey whose breakage would page someone.

## 2. Design for isolation
- **Each test creates its own data** (unique IDs/emails with a random suffix) through an
  API or factory, and does not depend on another test having run. Order dependence is
  the most common hidden cause of "works alone, fails in the suite".
- Reset or namespace state rather than sharing one seeded account across tests.
- Control time, randomness and external services (fakes, stubs, test containers).
- UI suites: page objects / component objects own locators; tests express intent.
  One locator change = one edit.

## 3. Wire into CI with time budgets
- **On every PR (target < 10 min):** lint, unit, integration, contract, a small E2E smoke set.
- **On merge / nightly:** full E2E across browsers, longer integration, performance smoke.
- Run in parallel / shard by historical timing; fail fast on the cheap stages first.
- Publish JUnit XML so CI shows per-test history; keep screenshots/traces/logs as artifacts.
- A red main branch is stop-the-line: fix or revert within the hour, or the suite stops meaning anything.

## 4. Flaky tests: find, triage, fix
A flaky test passes and fails on the same code. Left alone, people learn to re-run
until green and stop reading failures.
**Find:** track tests that failed then passed on retry (most runners report "flaky");
rerun suspects in a loop (`--repeat-each`, `pytest --count` via pytest-repeat, a shell loop)
and in random order.
**Triage by cause** — in practice it is almost always one of:
1. **Async timing** — fixed sleeps, asserting before the UI/API settled → use condition waits / retrying assertions.
2. **Shared state / order dependence** — leaked data, global singletons, unreset mocks → per-test data and teardown.
3. **Test environment** — shared staging changed, resource starvation in CI containers, small `/dev/shm`.
4. **Non-determinism in the product** — unordered results asserted in order, time zones, DST, floats → a real bug or a wrong assertion.
5. **External dependencies** — third-party sandboxes → stub them below E2E.
**Policy:** quarantine (move to a non-blocking job, with a ticket and an owner and a
date) rather than delete or ignore — and cap the quarantine size. Retries in CI are a
stopgap to keep PRs moving; they must still be reported, never silent.

## 5. Keep it maintainable
- Delete tests that duplicate coverage at a higher layer or test removed features.
- Review test code like product code; no copy-pasted 200-line tests.
- Measure: suite duration trend, flaky rate, defects escaping to production by layer.
  Escapes tell you where coverage is missing; flaky rate tells you where trust is leaking.

## Unconfirmed / notes
Strategy guidance distilled from widely cited practice (Fowler's test pyramid, Google
testing blog on flakiness); the time budgets and ratios are judgement calls to adapt,
not measured standards.

## Verify
- [ ] Every E2E test names the user journey it protects; nothing E2E that a unit test could cover.
- [ ] Tests pass when run alone, in random order, and in parallel.
- [ ] PR pipeline finishes inside its budget; slow stages run later.
- [ ] Flaky tests are visible on a list with owners; quarantine has a size cap.
- [ ] Failure artifacts (logs, screenshots, traces) are attached to every red run.
