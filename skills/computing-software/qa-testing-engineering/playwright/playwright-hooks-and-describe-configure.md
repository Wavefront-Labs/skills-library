---
id: computing-software.qa-testing-engineering.playwright.playwright-hooks-and-describe-configure
name: playwright-hooks-and-describe-configure
category: computing-software
field: qa-testing-engineering
product: playwright
tags: [playwright-hooks, beforeeach, beforeall, describe-configure, test-step]
level: practitioner
status: verified
description: "Use Playwright beforeEach/afterEach/beforeAll/afterAll hooks, describe.configure modes and test.step correctly, and know when a fixture is better than a hook."
sources:
  - https://playwright.dev/docs/api/class-test
  - https://playwright.dev/docs/test-fixtures#with-fixtures
  - https://playwright.dev/docs/api/class-test#test-step
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Hooks and describe.configure

**Goal:** shared setup without hidden coupling between tests.

```ts
test.describe('cart', () => {
  test.beforeEach(async ({ page }) => { await page.goto('/shop'); });
  test.afterEach(async ({ page }, testInfo) => {
    if (testInfo.status !== testInfo.expectedStatus) await page.screenshot({ path: testInfo.outputPath('fail.png') });
  });
  test('adds item', async ({ page }) => { /* ... */ });
});
```

## beforeAll / afterAll
- Run **once per worker**, not once per run; with 4 workers a beforeAll that creates a user runs 4 times.
- Cannot use the `page` fixture (test-scoped); run here: `"context" and "page" fixtures are not supported in "beforeAll" since they are created on a per-test basis.` Use `browser` and create a page manually, or a worker fixture.
- If a test fails, the worker restarts and beforeAll runs again for remaining tests (run here: `workerIndex` 3 before b1, then 4 after b2 failed).

## describe.configure
```ts
test.describe.configure({ mode: 'parallel' });   // run tests in this file in parallel
test.describe.configure({ mode: 'serial' });     // stop after first failure, retry group together
test.describe.configure({ retries: 2, timeout: 60_000 });
```

## test.step for readable reports
```ts
await test.step('log in', async () => { /* ... */ });
await test.step('pay', async () => { /* ... */ }, { box: true }); // errors point at the step call
```

## Hook or fixture?
Prefer fixtures when setup returns a value, needs teardown, is reused across files, or should run only for tests that use it. Hooks are fine for file-local navigation.

## Gotchas
- Top-level hooks (outside describe) apply to every test in the file.
- `afterEach` runs even on failure (run here with `status: failed`, `expectedStatus: passed`); guard cleanup against partial setup.
- Shared mutable variables set in `beforeAll` leak between tests in parallel mode.

## Verify
Reporter shows steps nested correctly; running a single test (`-g`) still passes (no hidden dependence on other tests).
