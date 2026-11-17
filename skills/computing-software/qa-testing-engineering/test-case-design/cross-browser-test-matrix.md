---
id: computing-software.qa-testing-engineering.test-case-design.cross-browser-test-matrix
name: cross-browser-test-matrix
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [cross-browser-testing, compatibility-testing, browser-matrix, browserslist, analytics-driven-testing, webkit]
level: practitioner
status: docs-checked
description: "Choose a cross-browser matrix from real traffic: tiers, Browserslist queries and coverage, Playwright projects and channels, WebKit versus Safari, and Selenium Grid."
sources:
  - https://playwright.dev/docs/browsers
  - https://github.com/browserslist/browserslist
  - https://www.selenium.dev/documentation/grid/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cross-browser test strategy and matrix

**Goal:** catch browser-specific defects with the least test duplication.

## Build the matrix from data
1. Pull browser/OS/device share from your own analytics for a period you choose.
2. Tier it. Agree the share thresholds with stakeholders; the numbers below are not from any source, only the shape:
   - **Tier 1** (large share or business-critical): full automated E2E plus manual exploratory each release.
   - **Tier 2** (smaller share): automated smoke and critical journeys.
   - **Tier 3** (long tail): best effort, no blocking.
3. Align the build target with the matrix. Browserslist shares target browsers between tools such as Autoprefixer and Babel, via a `browserslist` key in package.json or a `.browserslistrc` file. Its default query is `> 0.5%, last 2 versions, Firefox ESR, not dead`. Custom traffic data can be queried (`> 1% in my stats`) after exporting analytics to a `browserslist-stats.json` file; browser names and versions must match the Can I Use database or the entries are ignored.

## Covering engines efficiently
- Playwright runs Chromium, WebKit and Firefox, plus branded Google Chrome and Microsoft Edge, and emulated tablet and mobile devices, as `projects` in the config (for example `devices['Desktop Safari']` for a `webkit` project). `npx playwright test` runs all projects; `--project=firefox` runs one.
- Branded browsers are selected with the `channel` option (`chrome`, `msedge`, plus beta, dev and canary variants). By default Playwright uses open source Chromium builds, which run ahead of the stable branded releases; use a stable channel when policy requires regression testing against currently public browsers.
- WebKit is built from WebKit main sources, often before the changes reach Safari, and Playwright does not work with branded Safari. For the closest-to-Safari experience run WebKit on macOS.
- Browserslist notes that all iOS browsers use WebKit.
- Selenium Grid runs WebDriver scripts on remote machines to test in parallel, on different browser versions and across platforms.
- Suggested policy (judgement, not from the sources): full suite on one engine, critical journeys on the others.

## What tends to differ
Playwright documents that available media codecs vary between Linux, macOS and Windows, and that Chromium lacks some codecs bundled with Chrome and Edge; test those with the official channel. Enterprise browser policies on Chrome and Edge can interfere with Playwright launching them.

## Gotchas
- Playwright warns that new Chrome and Edge headless mode differs from the chromium headless shell it uses by default, so expect different behaviour in some cases. Keep visual baselines from the same mode as CI.
- Browserslist `defaults` includes Firefox ESR; testing only the newest release can miss users on extended-support versions.

## Verify
`npx browserslist` lists the browsers a query selects; `browserslist --coverage "> 1%"` prints the share of users they cover.

## Checked
Date: 2026-11-08
Read in full: Playwright "Browsers" (Configure Browsers, Chromium, headless shell, new headless mode, Google Chrome and Edge incl. "When to use", Firefox, WebKit); Browserslist README (Best Practices, Queries, Full List, Config File, Custom Usage Data, JS API coverage, Environment Variables); Selenium Grid landing page (about 1.4k characters, only the Grid aims list).
Confirmed: default query string `> 0.5%, last 2 versions, Firefox ESR, not dead`; `> 1% in my stats`, `browserslist-stats.json`, Can I Use name matching; `--coverage`; `channel` values; projects config; `--project`; WebKit/Safari statements; codec and enterprise-policy notes; headless difference; iOS-uses-WebKit footnote; Grid aims.
Removed: 90-day window and the 5%, 1-5% and <1% tier thresholds (not sourced; now flagged as local choices), Gecko/Opera/Samsung engine claims, the CTAL-TA 4.4 reference, device-farm product names, ITP, `dvh`, `:has()` and other CSS claims, and the invented Verify step.
Method: documentation only; no commands were run.
