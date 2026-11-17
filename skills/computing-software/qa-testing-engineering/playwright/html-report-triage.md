---
id: computing-software.qa-testing-engineering.playwright.html-report-triage
name: html-report-triage
category: computing-software
field: qa-testing-engineering
product: playwright
tags: [html-reporter, show-report, playwright-reporters, report-attachments]
level: practitioner
status: docs-checked
description: "Configure and triage the Playwright HTML report: open modes, output folder, filtering by status/project/tag, attachments, steps, flaky markers and hosting the report from CI."
sources:
  - https://playwright.dev/docs/test-reporters
  - https://playwright.dev/docs/ci-intro
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# HTML report and show-report triage

**Goal:** go from a red CI job to the root cause in minutes.

## Config
```ts
reporter: [
  ['html', { open: process.env.CI ? 'never' : 'on-failure', outputFolder: 'playwright-report', title: 'E2E nightly' }],
  ['list'],
],
```
Open later: `npx playwright show-report [folder]`, which also accepts a `.zip` archive downloaded from a CI artifact (it must contain `index.html` at its top level). The report needs a web server to work correctly, so opening `index.html` directly from disk does not work as expected.

## Triage flow
1. Filter the report by browser, passed, failed, skipped and flaky tests.
2. Open a failed test to see the error, the steps and the attachments.
3. Attachments include screenshots, video and the trace; once the report is served with `show-report`, click the trace icon next to the test's file name to open the trace viewer. Custom attachments (logs, API responses) appear there too.
4. Check whether failures cluster by project (browser) or by file (shared data).

## CI hosting
- Upload `playwright-report/` as a CI artifact (`actions/upload-artifact` with a `retention-days` value).
- Or publish the report folder to static web hosting per run; the docs show Azure Storage static websites. Use `attachmentsBaseURL` if report and `data` folder are uploaded to different places.
- Sharded runs: merge blob reports into one HTML report first (`merge-reports`).

## Gotchas
- `open` takes `always`, `never` or `on-failure` (default `on-failure`); set `never` in CI so no browser is opened.
- `PLAYWRIGHT_HTML_OUTPUT_DIR`, `PLAYWRIGHT_HTML_OPEN` and `PLAYWRIGHT_HTML_TITLE` are the environment equivalents of `outputFolder`, `open` and `title`.

## Verify
Downloaded artifact opens with `npx playwright show-report ./playwright-report` and traces load for failed tests.

## Checked

2026-10-25: checked against the Playwright docs (microsoft/playwright main, docs/src, commit of 2026-10-24). Confirmed: the html reporter options open, outputFolder and title with the open values always, never and on-failure (default on-failure), their PLAYWRIGHT_HTML_* environment variables, show-report with an optional folder or zip archive, the need for a web server to view the report, filtering by browser, passed, failed, skipped and flaky, the trace icon opening the trace viewer, and attachmentsBaseURL. Removed: the status and project filter-prefix syntax, the Retries tab, the 14-day retention figure and the report-size remark, none of which these pages state.

Method: documentation only; no commands were run.
