---
id: computing-software.qa-testing-engineering.test-automation.flaky-test-root-causes
name: flaky-test-root-causes
category: computing-software
field: qa-testing-engineering
product: test-automation
tags: [test-order-dependence, async-timing, flaky-tests, test-reliability, shared-state]
level: practitioner
status: docs-checked
description: "Diagnose and fix flaky-test root causes: async timing and fixed sleeps, order dependence and shared state, time and randomness, concurrency, resource leaks."
sources:
  - https://mir.cs.illinois.edu/lamyaa/publications/fse14.pdf
  - https://playwright.dev/docs/actionability
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Flakiness root causes

**Goal:** fix the cause, not add retries. Luo et al. (FSE 2014), an empirical study of flaky-test fixes, found the top three categories are Async Wait, Concurrency and Test Order Dependency, and recommend that detection and fixing techniques focus on them.

## What the study found
- About a third of Async Wait flaky tests (34%) use a simple method call with a time delay to enforce an ordering, and many (54%) were fixed with `waitFor`-style synchronisation.
- Many Test Order Dependency flaky tests (47%) are caused by dependence on external resources.
- Almost all Concurrency flaky tests involve only two threads.

## Catalogue, symptom, fix
| Cause | Symptom | Fix |
|---|---|---|
| Async wait / fixed sleep | fails on slow CI, fixed delay in code | wait for a condition (web-first assertions, explicit waits, `await` the promise, poll with a timeout) |
| Order dependence (polluter/victim) | passes alone, fails in suite (or vice versa) | isolate state: fresh fixtures, reset DB, no module-level globals; find the polluter by bisecting the test order |
| Shared state in parallel | fails with multiple workers | unique data per test (ids, emails), per-worker DB/schema |
| Time | fails at midnight, month end, DST, in other TZ | inject or freeze the clock; set the time zone explicitly |
| Randomness | fails one run in N | seed the RNG and log the seed |
| Concurrency in code | intermittent wrong values | real race: fix the code; test with race detectors |
| Unordered collections | assertion on list order from a set/dict/DB without ORDER BY | sort before compare or assert as sets |
| External dependencies | timeouts, 503 | stub at the boundary or use contract tests |
| Resource leaks | fails late in long runs | close connections and browsers |
| Animation/rendering | click intercepted | wait for stable state (see below) |
| Floating point | rare assertion mismatch | approximate comparison |

## UI actions and actionability
Playwright auto-waits before an action until the element is Visible, Stable (not animating, or animation completed), Receives Events (not obscured by other elements) and Enabled, among other checks (see the actionability page). Lean on those checks rather than adding sleeps.

## Finding an order-dependent polluter
Run the tests in randomised order, record the seed so the order can be replayed, then bisect the preceding tests against the failing one. Use your test runner's random-order and test-selection options (look them up for your framework).

## Gotchas
- Increasing timeouts hides the problem and slows the suite.
- Retrying at the CI-job level masks real product races.

## Verify
After the fix, the test passes many repeated runs in random order with parallel workers, and the cause is recorded on the flaky ticket.

## Checked
2026-11-09. Confirmed in the FSE 2014 paper (converted with pdftotext): findings F.1, F.4, F.6, F.7 and F.8 (top three categories, 34%, 54%, 47%, two-thread concurrency) and the Playwright actionability page (Visible, Stable, Receives Events, Enabled). Removed: the Google Testing Blog source (not used for any retained claim), pytest-randomly and detect-test-pollution commands, freezegun/jest/page.clock names, WireMock/MSW, pytest.approx, the "100+ runs" figure.
Method: documentation only; no commands were run.
