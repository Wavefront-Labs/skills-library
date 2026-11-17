---
id: computing-software.qa-testing-engineering.playwright.debugging-in-vscode-extension
name: debugging-in-vscode-extension
category: computing-software
field: qa-testing-engineering
product: playwright
tags: [playwright-vscode, playwright-debugging, breakpoints, pick-locator]
level: practitioner
status: docs-checked
description: "Debug Playwright tests in the VS Code extension: run/debug from the gutter, breakpoints, live locator highlighting, Pick locator, show browser and record at cursor."
sources:
  - https://playwright.dev/docs/getting-started-vscode
  - https://playwright.dev/docs/debug
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Debugging with the VS Code extension

**Goal:** step through a failing test with live browser feedback instead of console.log loops.

## Setup
Install "Playwright Test for VSCode" (ms-playwright.playwright). The Testing sidebar lists tests from `playwright.config.ts`; check the projects (browsers) to run in the sidebar; with several `playwright.config.ts` files, switch between them with the gear icon.

## Core moves
- **Run / Debug** via the green triangle in the gutter; right-click > Debug Test to stop at breakpoints.
- **Show browser** checkbox: runs in a visible browser; with Run Test (not Debug Test) the browser session is reused, so you can keep Chrome DevTools open between runs.
- **Live locator highlighting**: after a run with Show browser enabled, click a locator in your code and the element highlights in the browser window; edit the locator and the browser shows the change live.
- **Pick locator**: click an element in the opened browser and the best locator is copied to the clipboard.
- **Record new** opens a browser and generates test code as you interact; **Record at cursor** adds actions at the cursor inside an existing test.
- **Show trace viewer** (sidebar option): a trace opens automatically when the test finishes.

## Debugging outside the extension
For the command line, `npx playwright test --debug` opens the Playwright Inspector, launches browsers headed and sets the default timeout to 0 (no timeout); `PWDEBUG=1` does the same for the environment-variable route.

## Gotchas
- With `--debug` or `PWDEBUG=1` the default timeout is 0, so a test may pass interactively but time out in CI; check timings in the trace.
- If no tests appear, check which config is selected with the gear icon in the sidebar.

## Verify
Right-click Debug Test pauses at a breakpoint, and clicking a locator in the editor highlights its element in the browser.

## Checked

2026-10-25: checked against the Playwright docs (microsoft/playwright main, docs/src, commit of 2026-10-24). Confirmed: the extension id ms-playwright.playwright, the project checkboxes and multi-config gear icon, Show Browser, live locator highlighting and live locator editing, Pick locator copying to the clipboard, Record new and Record at cursor, Show Trace Viewer opening a trace after the run, breakpoints with Debug Test, and the --debug and PWDEBUG defaults (headed, timeout 0). Removed: the launch.json example, the Reveal test output item and the fixture-breakpoint claim, which the docs do not cover.

Method: documentation only; no commands were run.
