---
id: computing-software.qa-testing-engineering.test-automation.retry-policy-without-masking-defects
name: retry-policy-without-masking-defects
category: computing-software
field: qa-testing-engineering
product: test-automation
tags: [retry-policy, test-retries, flaky-tests, flakiness, ci]
level: practitioner
status: docs-checked
description: "Configure Playwright and Cypress test retries and read their flaky reporting, with the SWE-at-Google caution that reruns trade CPU for engineer time and defer root-cause fixes."
sources:
  - https://abseil.io/resources/swe-book/html/ch11.html
  - https://playwright.dev/docs/test-retries
  - https://docs.cypress.io/app/guides/test-retries
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Retry policy without masking defects

**Goal:** retries absorb rare noise while every retry stays visible, so real intermittent bugs still get fixed.

## What the sources say
- *Software Engineering at Google* ch. 11: automatically rerunning failed tests effectively trades CPU cycles for engineering time. That makes sense at low levels of flakiness, but rerunning only delays the need to fix the root cause.
- Playwright: by default failing tests are not retried. Enable with `npx playwright test --retries=3` or `retries: 3` in config. A failed test causes the worker process (and browser) to be discarded and a new one started; with retries, the new worker begins by retrying the failed test. Results are categorised as passed (first run), flaky (failed first, passed on retry) and failed (failed all retries). `testInfo.retry` lets a test, hook or fixture detect a retry, for example to clear server-side caches first. Retries can be set per group or file with `test.describe.configure({ retries: 2 })`.
- Playwright serial mode (`test.describe.serial` / `mode: 'serial'`) groups dependent tests: after a failure the rest are skipped and the whole group is retried together. The docs say it is usually better to make tests isolated so they can run and be retried independently.
- Cypress: retries are off until enabled. With `retries: 2`, a test can run up to 3 attempts before being marked failed. Use `retries: { runMode, openMode }` to set different counts for `cypress run` and `cypress open` (the docs' example uses 2 and 0), or a single number for all modes; it can also be set for a specific test. Cypress Cloud shows a Flaky filter and badge for tests that retried and then passed, and a flaky rate per test.

## Practitioner policy (judgement, not from these pages)
Keep the retry count low, always report passed-on-retry as flaky rather than passed, and track recurring flakes with an owner so the retry rate falls over time.

## Verify
Reports separate flaky from passed, retry counts are explicit in config, and persistent flakes are investigated rather than only retried.

## Checked
2026-11-08. Confirmed against the Playwright test-retries page, the Cypress test-retries page and the SWE at Google chapter on rerunning flaky tests. Removed (not in these pages): zero retries for unit tests, the 1-2 maximum, quarantine rules, `trace: 'on-first-retry'`, pytest-rerunfailures and Surefire settings, and the CI-only `process.env.CI` config. Replaced the Google Testing Blog landing page, which has no retry policy, with the book chapter.
Method: documentation only; no commands were run.
