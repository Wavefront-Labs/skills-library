---
id: computing-software.web-development.frontend-development.diagnosing-flaky-ui-tests
name: diagnosing-flaky-ui-tests
category: computing-software
field: web-development
product: frontend-development
tags: [frontend-testing, flaky-tests, playwright, cypress, test-reliability, ci]
level: practitioner
status: docs-checked
description: "Finding flaky UI tests with Playwright and Cypress retries: how retries classify flakes, tracing on first retry, reading the trace viewer, isolating tests."
sources:
  - https://playwright.dev/docs/test-retries
  - https://docs.cypress.io/app/guides/test-retries
  - https://playwright.dev/docs/trace-viewer
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Diagnosing flaky UI tests

## 1. Surface flakes with retries
- Playwright: by default failing tests are not retried. Enable with `npx playwright test --retries=3` or `retries` in the config; per group or file use `test.describe.configure({ retries: 2 })`.
- Playwright classifies tests: "passed" (first run), "flaky" (failed first run, passed on retry), "failed" (failed all retries). The report lists flaky tests, so track them rather than letting retries hide them.
- On any failure Playwright discards the worker process and browser and starts a new one; with retries the new worker begins by retrying the failed test. This keeps failing tests from affecting healthy ones as long as tests are independent.
- `testInfo.retry` is readable in any test, hook or fixture, e.g. to clear server-side state before a retry.
- Cypress: set `retries: 2` to retry a failed test up to 2 extra times (3 attempts total). Use `retries: { runMode, openMode }` to differ between `cypress run` and `cypress open`; retries can also be set per test or per suite. Screenshots of retried attempts are suffixed `(attempt n)`.

## 2. Record traces
- Playwright docs recommend `trace: 'on-first-retry'` in CI (with `retries` enabled), producing a trace.zip for each retried test.
- Other values: `'on-all-retries'`, `'retain-on-failure'` (record every test, delete traces of passing ones; use when retries are off), `'off'`, and `'on'` (every test; the docs call it performance heavy and not recommended).
- Open with `npx playwright show-trace path/to/trace.zip` (or a URL), or at trace.playwright.dev, which loads the trace in the browser without transmitting data.

## 3. Read the trace
- Actions tab: locator used and duration per action; Before and After snapshot tabs show the DOM around each action; the Action snapshot highlights the click position.
- Log tab: what Playwright did behind the scenes, such as scrolling into view and waiting for the element to be visible, enabled and stable.
- Errors tab and red timeline line show where it failed; Console and Network tabs filter to the selected action or time range; Attachments compare screenshot diffs.

## 4. Isolation
Playwright's own advice: make tests isolated so they can be run and retried independently. `test.describe.serial()` (serial mode) retries a dependent group together and skips tests after a failure; use only for genuinely dependent tests.

## Verify
Flaky tests appear in the report with a trace from the first retry; after the fix the test no longer reports "flaky" across CI runs.

## Checked
Method: docs-only read on 2026-11-09 of the Playwright test-retries and trace-viewer pages in full, and the Cypress test-retries page (retry configuration and screenshot sections, via grep of the extracted text). The Google Testing Blog source was dropped as a blog. Removed as unstated on the pages: --repeat-each and CPU stress advice, cause-and-fix table (hydration, animations, time zones, route stubbing), quarantine policy and timeout advice.
