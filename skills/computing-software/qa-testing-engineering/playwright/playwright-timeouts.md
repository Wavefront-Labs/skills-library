---
id: computing-software.qa-testing-engineering.playwright.playwright-timeouts
name: playwright-timeouts
category: computing-software
field: qa-testing-engineering
product: playwright
tags: [playwright-timeouts, test-timeout, action-timeout, navigation-timeout, global-timeout]
level: practitioner
status: verified
description: "Configure Playwright's layered timeouts (test, expect, action, navigation, global, fixture) and diagnose which one fired from the error message."
sources:
  - https://playwright.dev/docs/test-timeouts
  - https://playwright.dev/docs/api/class-testconfig
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Test, expect, action and navigation timeouts

**Goal:** fail fast on real hangs without false failures on legitimately slow steps.

## The layers
| Timeout | Default | Set via |
|---|---|---|
| Test (test body, fixture setup, beforeEach; teardown and afterEach get a separate timeout of the same value) | 30s | `timeout` in config, `test.setTimeout()`, `test.slow()` (x3) |
| Expect (web-first assertion) | 5s | `expect: { timeout }`, per assertion `{ timeout }` |
| Action (click, fill...) | none | `use: { actionTimeout }`, per call `{ timeout }` |
| Navigation (goto, waitForURL) | none | `use: { navigationTimeout }` |
| Global (whole run) | none | `globalTimeout` (good in CI) |
| beforeAll/afterAll | 30s, separate from tests | `test.setTimeout` inside hook |
| Fixture | none of its own (counts toward the test); worker-scoped fixtures get their own, equal to the test timeout | `{ timeout: 60_000 }` in fixture tuple |

```ts
export default defineConfig({
  timeout: 45_000,
  globalTimeout: 60 * 60_000,
  expect: { timeout: 7_000 },
  use: { actionTimeout: 10_000, navigationTimeout: 20_000 },
});
test('export', async ({ page }) => { test.slow(); /* ... */ });
test.describe.configure({ timeout: 120_000 });
```

## Reading failures
- `Test timeout of 30000ms exceeded.` -> whole test too long; look at the trace for the step that hung.
- `expect(locator).toBeVisible() failed ... Timeout: 5000ms` -> web-first assertion; `Timeout 5000ms exceeded while waiting on the predicate` -> `expect.poll`.
- `TimeoutError: locator.click: Timeout 10000ms exceeded.` -> action, followed by actionability log lines. With no `actionTimeout` a stuck click instead reports `locator.click: Test timeout of 3000ms exceeded.` (run with a 3 s test timeout).
- `Fixture "db" timeout of 60000ms exceeded during setup.` -> slow fixture: give it its own timeout (message reproduced here with a 500 ms fixture timeout).

## Gotchas
- Setting `actionTimeout` gives clearer errors than letting the test timeout catch a stuck click.
- `test.slow()` triples, it does not set (run here: 30000 became 90000); `test.setTimeout(0)` disables (avoid in CI).
- `--debug` is documented as a shortcut for `PWDEBUG=1` plus `--timeout=0 --max-failures=1 --headed --workers=1`, so test timeouts are disabled. `test.setTimeout(0)` also means no timeout (API docs).

## Verify
In CI, a deliberately stuck test fails with an action/assertion timeout message, not only "Test timeout".
