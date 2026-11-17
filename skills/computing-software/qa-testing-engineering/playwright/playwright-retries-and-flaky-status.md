---
id: computing-software.qa-testing-engineering.playwright.playwright-retries-and-flaky-status
name: playwright-retries-and-flaky-status
category: computing-software
field: qa-testing-engineering
product: playwright
tags: [playwright-retries, flaky-classification, testinfo-retry, flaky-tests]
level: practitioner
status: verified
description: "Configure Playwright retries, read the flaky status, use testInfo.retry for cleanup on retry, and keep retries from hiding real regressions."
sources:
  - https://playwright.dev/docs/test-retries
  - https://playwright.dev/docs/api/class-testinfo#test-info-retry
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Retries and flaky classification

**Goal:** retries as a signal-collecting tool, not a carpet.

## Config
```ts
retries: process.env.CI ? 2 : 0,
use: { trace: 'on-first-retry' },
```
CLI: `--retries=3`. Per group: `test.describe.configure({ retries: 1 })`.

## Outcomes
- **passed**: passed first time.
- **flaky**: failed, then passed on a retry. Job stays green unless `--fail-on-flaky-tests` (or `failOnFlakyTests: true` in config).
- **failed**: failed all attempts.
Each retry starts in a **new worker process** (fresh browser, beforeAll runs again; run here `workerIndex` went 0 then 1 between the failed attempt and the retry). Run here with `--retries=1`: the flaky test exited 0, and 1 with `--fail-on-flaky-tests`; `--reporter=json` gave the test `status: 'flaky'` and `stats.flaky: 1`.

## testInfo.retry
```ts
test.beforeEach(async ({}, testInfo) => {
  if (testInfo.retry) await cleanupLeftoverOrder();   // previous attempt may have left state
});
```

## Serial groups
In `mode: 'serial'`, a failure retries the whole group from the first test (run here: s1 passed, s2 failed, s3 skipped; the retry re-ran s1, s2, s3 with `retry` 1).

## Policy that works
1. Retries on in CI only, max 2.
2. Report flaky tests (HTML report search `s:flaky`, per its filter source; JSON reporter `status: 'flaky'`) to a tracking issue weekly.
3. New tests: run `--repeat-each=20 --retries=0` before merge.
4. For release gates, consider `--fail-on-flaky-tests`.

## Gotchas
- Retries double CI time on real failures; pair with `maxFailures` to stop runaway runs.
- A test that is flaky because of a real race in the product is a product bug; retries hide it from users' view only in CI.

## Verify
JSON report counts of flaky tests are tracked over time and trend down.
