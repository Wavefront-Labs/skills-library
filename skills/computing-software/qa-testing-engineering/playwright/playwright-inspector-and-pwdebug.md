---
id: computing-software.qa-testing-engineering.playwright.playwright-inspector-and-pwdebug
name: playwright-inspector-and-pwdebug
category: computing-software
field: qa-testing-engineering
product: playwright
tags: [playwright, playwright-inspector, pwdebug, playwright-debugging, page-pause, headed, vscode-extension]
level: practitioner
status: docs-checked
description: "Debug Playwright tests with the Inspector: --debug and PWDEBUG, page.pause(), stepping, locator picking, verbose API logs and the VS Code extension."
sources:
  - https://playwright.dev/docs/debug
  - https://playwright.dev/docs/getting-started-vscode
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Playwright Inspector and PWDEBUG

**Goal:** step through a failing test live and see exactly what Playwright is waiting for.

## Launching the Inspector
```bash
npx playwright test tests/checkout.spec.ts:42 --debug     # one test at a given line, headed, timeout 0
PWDEBUG=1 npx playwright test                             # same via env var (also for library scripts)
```
In code: add `await page.pause()` and run in debug mode; clicking Resume in the Inspector runs the test and stops only at `page.pause()`.

## In the Inspector
- Step through the test; the log shows the actionability checks Playwright performed by the time it paused on an action.
- **Pick locator**: hover over elements in the browser to see a suggested locator; the field next to the button shows the locator the test is paused on and can be edited live.
- The Inspector also shows actionability logs.

## Other debugging aids
- `DEBUG=pw:api npx playwright test` prints verbose API calls with timings.
- Slow down actions with the `slowMo` launch option: `use: { launchOptions: { slowMo: 500 } }`.
- Browser developer tools: set a breakpoint with `page.pause()`; `PWDEBUG=console` exposes the `playwright` object in the browser console for trying locators.
- VS Code extension: run/debug single tests, breakpoints in test code, Show browser, Pick locator, Record at cursor (see the VS Code skill).
- Trace viewer for post-mortem inspection.

## Gotchas
- `--debug` launches browsers headed and sets the default timeout to 0; remove `page.pause()` before committing.
- Bugs that only happen in CI (headless, Linux, slower) are better debugged from traces (`trace-on-first-retry-ci-debugging`).

## Verify
You can identify, for a timeout failure, which actionability check was not satisfied.

## Checked

2026-10-25: checked against the Playwright docs (microsoft/playwright main, docs/src, commit of 2026-10-24). Confirmed: the --debug flag (headed browsers, default timeout 0), running one test by file and line, PWDEBUG=1 and PWDEBUG=console, page.pause() with Resume, Inspector stepping, live locator editing, Pick locator and actionability logs, DEBUG=pw:api verbose logging, and the slowMo launch option. Removed: the eslint rule reference, the console.log and evaluateAll tips and the per-action resolved-element claim, which the docs do not state.

Method: documentation only; no commands were run.
