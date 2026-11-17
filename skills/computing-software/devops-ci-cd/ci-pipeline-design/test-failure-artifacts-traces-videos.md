---
id: computing-software.devops-ci-cd.ci-pipeline-design.test-failure-artifacts-traces-videos
name: test-failure-artifacts-traces-videos
category: computing-software
field: devops-ci-cd
product: ci-pipeline-design
tags: [ci-pipeline-design, playwright-trace, test-failure-artifacts, acceptance-tests]
level: practitioner
status: docs-checked
description: "Capture traces, videos and screenshots on e2e test failure (Playwright, Cypress, Selenium) and publish them as CI artifacts to diagnose failures without rerunning."
sources: ["https://playwright.dev/docs/trace-viewer", "https://docs.cypress.io/app/guides/screenshots-and-videos"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Traces, videos and screenshots on failure

## Playwright
```ts
// playwright.config.ts
export default defineConfig({
  retries: process.env.CI ? 1 : 0,
  use: {
    trace: 'on-first-retry',          // needs retries; see Playwright test options for other modes
  },
});
```
Open a trace with `npx playwright show-trace path/to/trace.zip` or drag it into trace.playwright.dev (a statically hosted Trace Viewer).

## Cypress
`video: true` (video recording is disabled by default); screenshots on failure are on unless `screenshotOnRunFailure` is false. Videos go to `videosFolder` (default `cypress/videos`). Use the `after:spec` event listener to delete videos of passing specs.

## Selenium/WebDriver
Take screenshot + page source in the test framework's failure hook; capture browser console logs and
server logs from the same time window.

## CI upload
GitHub Actions: upload the results directory with `actions/upload-artifact` (see its README) in a step that runs even when tests fail.
GitLab: `artifacts: when: on_failure, expire_in: <duration>, paths: [test-results/]`; add
`artifacts:expose_as` for a link in the MR.

## Gotchas
- `trace: 'on'` for every test is heavy (CPU, disk); use on-first-retry/retain-on-failure.
- Traces and videos may contain secrets/PII typed into forms; restrict artifact access and retention.

## Verify
- [ ] A forced failure produces a downloadable trace that shows the failing step.

## Checked

2026-10-28. Confirmed: Playwright trace: 'on-first-retry' for CI, show-trace command and trace.playwright.dev (Trace Viewer page); Cypress video disabled by default, screenshotOnRunFailure, videosFolder default cypress/videos and the after:spec listener (screenshots and videos guide); GitLab artifacts:expose_as (CI YAML reference). Removed: Playwright screenshot, video and reporter options, the v13 note, retention figures and the exact upload-artifact inputs.

Method: documentation only; no commands were run.
