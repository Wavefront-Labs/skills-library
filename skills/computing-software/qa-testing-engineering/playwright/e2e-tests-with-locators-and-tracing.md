---
id: computing-software.qa-testing-engineering.playwright.e2e-tests-with-locators-and-tracing
name: e2e-tests-with-locators-and-tracing
category: computing-software
field: qa-testing-engineering
product: playwright
tags: [playwright, playwright-test, e2e-testing, end-to-end, browser-automation, locators, getbyrole, getbytestid, auto-waiting, web-first-assertions, expect, fixtures, setup-project, trace-viewer, tracing, codegen, ui-mode, parallel, sharding, workers, retries, chromium, firefox, webkit, typescript, ci, flaky-tests]
level: practitioner
status: docs-checked
description: "Reliable Playwright Test suites: role-based locators, web-first assertions, setup projects, parallel/sharded CI runs, and debugging failures with the trace viewer."
sources: ["https://playwright.dev/docs/intro", "https://playwright.dev/docs/best-practices", "https://playwright.dev/docs/trace-viewer"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Playwright end-to-end tests: locators, parallelism, traces

**Goal:** a Playwright Test (`@playwright/test`, TypeScript) suite that is fast, runs
in parallel, rarely flakes, and when it does fail tells you why in one click.

## 1. Setup
```bash
npm init playwright@latest          # creates playwright.config.ts, tests/, a CI workflow
npx playwright install --with-deps  # browsers + OS libraries
npx playwright test                 # run all; --project=chromium for one browser
npx playwright test --ui            # UI mode: watch, time-travel, pick locators
npx playwright codegen <APP_URL>    # record clicks -> starter code
```
Browser builds are tied to the Playwright version, so re-run `npx playwright install` after upgrading. In CI, the official Playwright Docker image avoids the install step; the docs recommend pinning the image to a specific version that matches the Playwright version in your project.

## 2. Locators: ask what the user sees
Preference order, per the docs' best practices:
```ts
page.getByRole('button', { name: 'Sign in' })
page.getByLabel('Email')
page.getByPlaceholder('Search')
page.getByText('Order confirmed')
page.getByTestId('cart-count')   // data-testid by default; change with use.testIdAttribute
```
Chain and filter instead of writing long CSS:
```ts
page.getByRole('row').filter({ hasText: 'Order #1042' }).getByRole('button', { name: 'Refund' })
```
**Strictness:** an action on a locator matching 2+ elements throws. That's a feature;
narrow the locator rather than reaching for `.first()`.

## 3. Auto-waiting and web-first assertions
Actions (`click`, `fill`) wait for the element to be attached, visible, stable,
enabled and receiving events. Assertions must use the async `expect` forms that retry:
```ts
await expect(page.getByTestId('cart-count')).toHaveText('3')  // retries until expect timeout (5 s default)
await expect(page).toHaveURL(/\/checkout/)
```
Anti-pattern: `expect(await locator.textContent()).toBe('3')` reads once, never retries, flakes.
Avoid `page.waitForTimeout()`. To wait for a backend call, create the promise
*before* the action: `const r = page.waitForResponse('**/api/cart'); await btn.click(); await r;`

## 4. Shared setup once, not per test
Expensive preconditions (seeding data, signing in a test account) go in a **setup
project**: a file matched by `testMatch: /.*\.setup\.ts/`, listed in other projects'
`dependencies: ['setup']`. Playwright runs it first, once. For sign-in, the docs
describe saving the browser context state to a file and pointing `use.storageState` at
it; keep that file git-ignored and use a dedicated low-privilege test account with
values injected by your CI's secret store, never hard-coded.
Custom **fixtures** (`test.extend({...})`) give each test a ready page object or API
client, with teardown after `await use(...)`.

## 5. Config that pays off
```ts
export default defineConfig({
  fullyParallel: true,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 2 : undefined,
  use: { baseURL: 'http://localhost:3000', trace: 'on-first-retry',
         screenshot: 'only-on-failure', video: 'retain-on-failure' },
  webServer: { command: 'npm run start', url: 'http://localhost:3000',
               reuseExistingServer: !process.env.CI },
});
```
Each test gets a fresh browser context (isolated cookies and storage), so tests must
not depend on run order. Shard big suites across CI machines with
`npx playwright test --shard=1/4` … `4/4` using the `blob` reporter, then
`npx playwright merge-reports` to get one HTML report.

## 6. Debugging a failure with traces
`trace: 'on-first-retry'` records a trace when a test is retried. Open it with
`npx playwright show-trace <path>/trace.zip` (or drop it on trace.playwright.dev, which
runs locally in your browser). It shows DOM snapshots before and after each action,
network, console and the source line. A test reported **flaky** (failed, then passed
on retry) is a bug to fix, not a pass; retries only hide it.

## Verify
- [ ] No `waitForTimeout` and no non-retrying `expect(await ...)` patterns (search the suite for them).
- [ ] Locators are role/label/test-id based; any `.nth()`/`.first()` has a comment saying why.
- [ ] `npx playwright test --repeat-each=10` passes with zero flaky.
- [ ] A deliberately broken assertion produces a trace you can open and read.
- [ ] Session-state files are git-ignored; no secrets in the repo.

## Checked

2026-10-25: checked against the Playwright docs (microsoft/playwright main, docs/src, commit of 2026-10-24). Confirmed: npm init playwright@latest, npx playwright install --with-deps, --ui, codegen, the default timeouts (test 30 s, expect 5 s), trace on-first-retry, show-trace and trace.playwright.dev, project dependencies with a *.setup.ts testMatch, the workers CI example, --shard=x/y with merge-reports, --repeat-each, waitForResponse created before the click, strictness, and the Docker image version-pinning advice. Removed: the exact-pinning and error-message claim and the lazy-locator sentence, which are not stated in these pages.

Method: documentation only; no commands were run.
