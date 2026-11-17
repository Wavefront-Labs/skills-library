---
id: computing-software.software-engineering.typescript.end-to-end-tests-with-playwright
name: end-to-end-tests-with-playwright
category: computing-software
field: software-engineering
product: typescript
tags: [typescript, playwright, e2e-testing, locators, auto-waiting, trace-viewer, browser-testing]
level: practitioner
status: docs-checked
description: "Write stable Playwright E2E tests: role-based locators, web-first assertions and auto-waiting, auth state reuse, fixtures, network mocking, traces for CI failures and sharding."
sources:
  - https://playwright.dev/docs/intro
  - https://playwright.dev/docs/locators
  - https://playwright.dev/docs/test-assertions
  - https://playwright.dev/docs/auth
  - https://playwright.dev/docs/trace-viewer
  - https://playwright.dev/docs/test-webserver
  - https://playwright.dev/docs/test-sharding
  - https://playwright.dev/docs/mock
  - https://playwright.dev/docs/best-practices
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# End-to-end tests with Playwright

**Goal:** browser tests that catch real regressions and don't flake.

## Setup
```bash
npm init playwright@latest           # config, example test, CI workflow
npx playwright test --ui             # watch mode with time-travel
npx playwright codegen http://localhost:3000   # record locators
```
```ts
// playwright.config.ts
export default defineConfig({
  testDir: "e2e",
  fullyParallel: true,
  retries: process.env.CI ? 2 : 0,
  use: { baseURL: "http://localhost:3000", trace: "on-first-retry", screenshot: "only-on-failure" },
  webServer: { command: "npm run start", url: "http://localhost:3000", reuseExistingServer: !process.env.CI },
  projects: [{ name: "chromium", use: { ...devices["Desktop Chrome"] } }, { name: "webkit", use: { ...devices["Desktop Safari"] } }],
});
```

## Locators and assertions
```ts
test("user can place an order", async ({ page }) => {
  await page.goto("/products/42");
  await page.getByRole("button", { name: "Add to cart" }).click();
  await page.getByRole("link", { name: /cart \(1\)/i }).click();
  await page.getByLabel("Email").fill("ada@example.com");
  await page.getByRole("button", { name: "Pay" }).click();
  await expect(page.getByRole("heading", { name: "Thank you" })).toBeVisible();
});
```
- Prefer `getByRole` / `getByLabel` / `getByText` (user-facing, also checks accessibility) over
  CSS/XPath; add `data-testid` with `getByTestId` where no accessible name exists.
- Web-first assertions (`await expect(locator).toHaveText(...)`) retry until timeout. Never
  `expect(await locator.textContent())` - no retry, flaky.
- No `page.waitForTimeout()`; actions auto-wait for visible/enabled/stable.

## Auth once, reuse
```ts
// auth.setup.ts
setup("login", async ({ page }) => {
  await page.goto("/login"); /* fill + submit */
  await page.context().storageState({ path: "playwright/.auth/user.json" });
});
// config: projects: [{ name: "setup", testMatch: /.*\.setup\.ts/ },
//   { name: "chromium", dependencies: ["setup"], use: { storageState: "playwright/.auth/user.json" } }]
```

## Isolation and data
Each test gets a fresh browser context. Create test data via API (`request` fixture) in a
fixture rather than through the UI; clean up or use unique data per test so parallel runs don't collide.

## Network control
```ts
await page.route("**/api/recommendations", (r) => r.fulfill({ json: [] }));   // stub flaky third parties
```
Mock only what you don't own; E2E value comes from hitting your real backend.

## Debugging CI failures
`trace: "on-first-retry"` -> `npx playwright show-trace trace.zip` (DOM snapshots, network,
console per step). Publish the HTML report as a CI artifact. Shard: `--shard=1/4` (`--shard=x/y`).

## Verify
- [ ] No `waitForTimeout` or manual sleeps in the suite.
- [ ] CI uploads traces/reports; flaky tests are fixed, not given more retries.

## Checked
Checked 2026-10-25 against the Playwright docs on main (microsoft/playwright docs/src). Confirmed: `npm init playwright@latest` and `--ui`; codegen; setup project with `testMatch`, `dependencies` and `storageState` under `playwright/.auth`; `trace: "on-first-retry"`, `screenshot: "only-on-failure"` and `npx playwright show-trace`; `webServer.reuseExistingServer`; `--shard=x/y`; `route.fulfill({ json })`; `request` fixture; `waitForTimeout` documented as debugging only; web-first assertions retry; `Desktop Chrome` and `Desktop Safari` device names. Removed the unconfirmed report-folder name.
Method: documentation only; no commands were run.
