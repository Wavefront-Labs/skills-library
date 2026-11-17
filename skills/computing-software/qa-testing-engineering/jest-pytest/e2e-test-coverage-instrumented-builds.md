---
id: computing-software.qa-testing-engineering.jest-pytest.e2e-test-coverage-instrumented-builds
name: e2e-test-coverage-instrumented-builds
category: computing-software
field: qa-testing-engineering
product: jest-pytest
tags: [e2e-coverage, istanbul-instrumentation, cypress-code-coverage, playwright-coverage, v8-coverage-e2e]
level: practitioner
status: docs-checked
description: "Collect code coverage from E2E tests: istanbul-instrumented front-end builds, Cypress code-coverage, Playwright V8 coverage and server-side coverage during the run."
sources:
  - https://docs.cypress.io/app/tooling/code-coverage
  - https://playwright.dev/docs/api/class-coverage
  - https://github.com/istanbuljs/babel-plugin-istanbul
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Collecting coverage from E2E tests

**Use:** find features no E2E test touches, and combine with unit coverage for a full picture. Not a gate by itself.

## Front-end: instrumented build
- Instrument the app code with Istanbul, either with `nyc instrument` (for example
  `npx nyc instrument --compact=false src instrumented`) or as part of transpilation with
  `babel-plugin-istanbul`.
- Instrumented code populates `window.__coverage__` in the browser, which keeps track of the original statements.

### Cypress
```bash
npm install @cypress/code-coverage --save-dev
```
Add `import '@cypress/code-coverage/support'` to the support file, and register
`require('@cypress/code-coverage/task')` in `setupNodeEvents`. The plugin merges the coverage from each test,
saves the combined result, and calls `nyc` (its peer dependency) to generate static HTML reports. Follow the
`@cypress/code-coverage` README for current setup, including Vite, Vue and Angular examples.

### Playwright
V8 coverage (Chromium-based browsers only; no instrumentation needed):
```ts
await page.coverage.startJSCoverage();   // options include resetOnNavigation
// ... test
const entries = await page.coverage.stopJSCoverage();
```
Playwright's documentation example converts entries with the `v8-to-istanbul` package. Alternatively, with an
Istanbul-instrumented build, read `window.__coverage__` from the page after each test and write it out for `nyc`.

## Back-end
Run the server with its language's coverage tooling enabled during the E2E run, stop it gracefully so the data
is flushed, then merge and report. Use that tool's own documentation for the commands.

## Gotchas
- Never ship instrumented bundles to production; gate instrumentation behind an environment flag.
- Source maps must match the built files, or V8 coverage maps to the wrong lines.
- E2E coverage is broad but shallow: a line "covered" by E2E may have no assertion on its behaviour.

## Verify
Report shows untouched routes/components; adding a test for one raises its file's coverage.

## Checked
2026-11-01. Confirmed: Cypress code-coverage page (`window.__coverage__`, `nyc instrument`, babel plugin,
`@cypress/code-coverage` support and task setup, merging, nyc HTML reports); Playwright Coverage page
(Chromium-only, `startJSCoverage`, `stopJSCoverage`, `resetOnNavigation`, `v8-to-istanbul` example);
babel-plugin-istanbul README (Babel plugin that instruments with Istanbul, used with nyc). Removed: the
`vite-plugin-istanbul` options, `NODE_ENV=test` rule, `.nyc_output` shared-merge claim, `coverage/lcov-report`
path, `monocart-reporter`, and the Python, Go and JaCoCo server commands, none of which the pages state.
Method: documentation only; no commands were run.
