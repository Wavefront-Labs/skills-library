---
id: computing-software.web-development.frontend-development.cross-browser-test-matrix
name: cross-browser-test-matrix
category: computing-software
field: web-development
product: frontend-development
tags: [cross-browser, browser-test-matrix, playwright, compatibility]
level: practitioner
status: docs-checked
description: "Cross-browser test matrix with Playwright projects for Chromium, Firefox and WebKit plus mobile devices, and using Baseline to judge feature support."
sources:
  - https://playwright.dev/docs/test-projects
  - https://web.dev/baseline
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cross-browser test matrix

## 1. Build the matrix from your data
Start from analytics: list browser, version, OS and device class with share, then decide which combinations get full regression, which get smoke tests and which are best effort. Write the policy down.

## 2. Automate engines in CI with Playwright projects
A project is a logical group of tests run with the same configuration. Projects let you run tests in chromium, webkit and firefox, branded browsers such as Google Chrome and Microsoft Edge, and emulated tablet and mobile devices (see Playwright's registry of device parameters).
```ts
// playwright.config.ts
import { defineConfig, devices } from '@playwright/test';
export default defineConfig({
  projects: [
    { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
    { name: 'firefox', use: { ...devices['Desktop Firefox'] } },
    { name: 'webkit', use: { ...devices['Desktop Safari'] } },
    { name: 'Mobile Chrome', use: { ...devices['Pixel 5'] } },
    { name: 'Mobile Safari', use: { ...devices['iPhone 12'] } },
  ],
});
```
- `npx playwright test` runs all projects by default; `--project=firefox` runs one.
- Projects can also carry different timeouts or retries, for example a "Smoke" project with a small subset and no retries beside a "Default" project that runs the rest with retries.
- Project dependencies run a setup project first (for example global setup) before the browser projects.

## 3. Prevent rather than test with Baseline
- Baseline summarises which web platform features are ready to use. Newly available: supported by all core browsers. Widely available: 30 months after becoming newly interoperable. Before that, Limited availability.
- It was originated by the Chrome team and is now defined by the WebDX Community Group.
- Related tooling listed on the page: a Lighthouse Baseline features audit, Browserslist Baseline queries, a Baseline Checker that selects a target from Google Analytics data, and the web-features npm package.

## Verify
CI runs every Playwright project; the matrix document is reviewed against current analytics.

## Checked
Method: docs-only read on 2026-11-09 of the Playwright test-projects page (projects, run, environments, splitting, dependencies sections) and the web.dev Baseline page, via text extraction. Dropped sources: BrowserStack docs (landing page) and the Apple Safari inspecting page (excluded domain). Removed as unstated: engine grouping and tier lists, claims about what Playwright WebKit cannot reproduce, real-device cloud guidance, per-release checklist, eslint-plugin-compat, and the browserstack and real-device-testing tags.
