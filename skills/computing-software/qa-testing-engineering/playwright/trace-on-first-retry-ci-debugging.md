---
id: computing-software.qa-testing-engineering.playwright.trace-on-first-retry-ci-debugging
name: trace-on-first-retry-ci-debugging
category: computing-software
field: qa-testing-engineering
product: playwright
tags: [playwright, trace-on-first-retry, trace-viewer, ci, debugging-ci-failures, trace-zip]
level: practitioner
status: docs-checked
description: "Debug CI-only failures with Playwright traces: trace modes, collecting on retry, opening trace.zip locally or at trace.playwright.dev, and what each trace tab tells you."
sources:
  - https://playwright.dev/docs/trace-viewer
  - https://playwright.dev/docs/trace-viewer-intro
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Traces from CI

**Goal:** diagnose failures you cannot reproduce locally using the recorded trace.

## Configure
```ts
use: { trace: 'on-first-retry' }    // recommended: cheap, trace only when a test is retried
// alternatives: 'on', 'on-all-retries', 'retain-on-failure', 'retain-on-first-failure', 'retain-on-failure-and-retries'
retries: process.env.CI ? 2 : 0,
```
Also: `screenshot: 'only-on-failure'`, `video: 'retain-on-failure'`.
`on-first-retry` produces a `trace.zip` for each test that was retried; traces go into the `test-results` directory and are attached in the HTML report. Upload `playwright-report/` and `test-results/` as CI artifacts.

## Open
```bash
npx playwright show-trace path/to/trace.zip
```
Or drop the zip on https://trace.playwright.dev, a statically hosted viewer that loads the trace entirely in your browser and does not transmit data externally. `show-trace` also accepts a URL.

## Reading a trace
- **Actions** tab: the locator used for each action and how long it took; hover an action to see the DOM snapshot change. Snapshots (Before, Action, After) are captured for each action, and the Action snapshot highlights the DOM node and the exact click position.
- **Call** tab: timing, locator, strict mode and key used for the action; **Log** tab for the action log.
- **Network** tab: requests made during the test.
- **Console** tab: console output from the page.
- **Source** tab highlights the line of code for the selected action; **Errors** tab shows the failure.
- **Attachments** tab: attachments, including expected, actual and diff images for visual comparisons.
- **Metadata** tab: information about the run.

## Gotchas
- Traces record page content and network activity of the test environment; treat artifacts as sensitive and set a short retention.
- `trace: 'on'` records every run; prefer `on-first-retry` or a `retain-on-*` mode.

## Verify
For a CI failure, you can name the root cause from the trace without rerunning the test.

## Checked

2026-10-25: checked against the Playwright docs (microsoft/playwright main, docs/src, commit of 2026-10-24). Confirmed: the trace modes in TestOptions (off, on, on-first-retry, on-all-retries, retain-on-failure, retain-on-first-failure, retain-on-failure-and-retries), on-first-retry producing a trace.zip per retried test in test-results, show-trace with a path or URL, trace.playwright.dev loading traces entirely in the browser without transmitting data, and the trace viewer tabs (Actions, Call, Log, Errors, Console, Network, Source, Metadata, Attachments) and the Before, Action and After snapshots. Removed: the devtools-on-snapshot and pick-locator claims and the list of typical findings, which no doc covers.

Method: documentation only; no commands were run.
