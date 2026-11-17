---
id: computing-software.qa-testing-engineering.test-automation.ui-automation-framework-selection
name: ui-automation-framework-selection
category: computing-software
field: qa-testing-engineering
product: test-automation
tags: [framework-selection, playwright, cypress, selenium, webdriverio, tool-evaluation]
level: practitioner
status: draft
description: "Choose a UI automation framework (Playwright, Cypress, Selenium, WebdriverIO): criteria, a comparison table, proof-of-concept tasks on your own app, and decision records."
sources:
  - https://www.istqb.org/certifications/certified-tester-advanced-level-test-automation-engineering-ctal-tae
  - https://playwright.dev/docs/intro
  - https://docs.cypress.io/
  - https://www.selenium.dev/documentation/test_practices/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Choosing a UI automation framework

**Goal:** pick the framework that fits the application, team skills and constraints, proven by a proof of concept on your own app rather than blog posts.

## Criteria
- **Browsers and platforms:** Chromium/Firefox/WebKit, real Safari, mobile web, native mobile (Appium), desktop/Electron.
- **Languages** the team will maintain tests in.
- **App architecture quirks:** multiple tabs/windows, iframes, cross-origin flows (SSO), shadow DOM, file downloads.
- **Reliability features:** auto-waiting, retries, tracing and debugging.
- **Parallelism and CI cost**, sharding, Docker images.
- **Ecosystem:** component testing, API testing, visual and accessibility plugins, reporting.
- **Grid/cloud vendor support** and existing investments.

## Snapshot comparison (verify against current versions)

| | Playwright | Cypress | Selenium WebDriver | WebdriverIO |
|---|---|---|---|---|
| Languages | JS/TS, Python, Java, .NET | JS/TS | Java, Python, C#, JS, Ruby | JS/TS |
| Browsers | Chromium, Firefox, WebKit | Chromium family, Firefox, WebKit (experimental) | all incl. real Safari, via drivers | WebDriver + BiDi, Appium |
| Multi-tab / cross-origin | native | limited (`cy.origin`) | native | native |
| Auto-wait | yes | yes (retry-ability) | explicit waits | yes |
| Parallel | built in, free | via CI or Cypress Cloud | Grid | built in |
| Native mobile | no (Android experimental) | no | via Appium | via Appium |

## Proof of concept
Automate the same 3-5 representative flows in the top two candidates (login with SSO, a complex form, a file upload, a flaky-prone async screen), run them 20 times in CI, and compare: authoring time, flake rate, runtime, debugging experience, team feedback.

## Decide
Write an architecture decision record: context, options, criteria scores, PoC results, decision, consequences. Revisit when constraints change.

## Verify
The ADR exists with PoC data from your own app, and the chosen framework runs the PoC flows in CI with a flake rate under the agreed limit.
