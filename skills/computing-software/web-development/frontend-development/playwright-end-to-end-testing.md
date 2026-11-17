---
id: computing-software.web-development.frontend-development.playwright-end-to-end-testing
name: playwright-end-to-end-testing
category: computing-software
field: web-development
product: frontend-development
tags: [frontend-testing, playwright, e2e-testing, locators, test-automation, ci]
level: practitioner
status: docs-checked
description: "Writing reliable Playwright end-to-end tests: role-based locators, web-first assertions with auto-wait, auth state reuse, network mocking, traces, and CI sharding."
sources:
  - https://playwright.dev/docs/best-practices
  - https://playwright.dev/docs/locators
  - https://playwright.dev/docs/auth
  - https://playwright.dev/docs/trace-viewer
  - https://playwright.dev/docs/test-cli
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# End-to-end tests with Playwright

## 1. Setup
`npm init playwright@latest` -> `playwright.config.ts`, `tests/`. Key config:
```ts
export default defineConfig({
  use: { baseURL: "http://localhost:3000", trace: "on-first-retry", screenshot: "only-on-failure" },
  retries: process.env.CI ? 2 : 0,
  webServer: { command: "npm run start", url: "http://localhost:3000", reuseExistingServer: !process.env.CI },
  projects: [{ name: "setup", testMatch: /auth\.setup\.ts/ },
             { name: "chromium", use: { ...devices["Desktop Chrome"], storageState: "playwright/.auth/user.json" }, dependencies: ["setup"] }],
});
```

## 2. Locators and assertions
```ts
test("adds item to cart", async ({ page }) => {
  await page.goto("/products/42");
  await page.getByRole("button", { name: "Add to cart" }).click();
  await expect(page.getByRole("status")).toHaveText("Added to cart");
  await expect(page.getByRole("link", { name: /cart \(1\)/i })).toBeVisible();
});
```
- Prefer `getByRole`, `getByLabel`, `getByText`; fall back to `getByTestId`. Avoid CSS/XPath tied to markup.
- Locators are lazy and auto-wait for actionability (visible, enabled, stable). Web-first `expect(locator)` assertions retry until timeout. Never use `waitForTimeout` in tests (the docs say it is for debugging only), and avoid `networkidle` waits (marked DISCOURAGED).
- Do not assert with `expect(await locator.isVisible()).toBe(true)` - it does not retry (use the web-first `await expect(locator).toBeVisible()`).

## 3. Auth once
```ts
// auth.setup.ts
setup("login", async ({ page }) => {
  await page.goto("/login");
  await page.getByLabel("Email").fill(process.env.E2E_USER!);
  await page.getByLabel("Password").fill(process.env.E2E_PASS!);
  await page.getByRole("button", { name: "Sign in" }).click();
  await page.waitForURL("/dashboard");
  await page.context().storageState({ path: "playwright/.auth/user.json" });
});
```
Or log in via API request for speed. Git-ignore the `.auth` folder.

## 4. Network control
`await page.route("**/api/recommendations", r => r.fulfill({ json: [] }))` to stub flaky third parties; `page.waitForResponse` to sync on a request. Keep the core journey un-mocked against a seeded test backend.

## 5. Debugging
`npx playwright test --ui`, `--debug`, `npx playwright codegen url` for locator discovery, `npx playwright show-trace trace.zip` (DOM snapshots, network, console per step).

## 6. CI
Install browsers `npx playwright install --with-deps`; shard `--shard=1/4`; merge reports with `merge-reports`; upload `playwright-report/` and traces as artifacts.

## Verify
Run each new test 20 times locally: `npx playwright test file.spec.ts --repeat-each=20` - zero failures before merging.

## Checked

Checked 2026-10-26 against the Playwright docs source (microsoft/playwright `docs/src`, main, last commit 2026-10-25): best practices, locators, test configuration, TestConfig/TestOptions/TestProject, authentication, web server, network, CLI, debugging, trace viewer and CI pages.

- Confirmed: `trace: "on-first-retry"`, `screenshot: "only-on-failure"`, `baseURL`, `retries`, `webServer.reuseExistingServer: !process.env.CI`, project `dependencies`, `playwright/.auth` in `.gitignore`, `--ui`, `--debug`, `codegen`, `show-trace` and trace.playwright.dev, `--repeat-each`, `merge-reports`, `--shard`, `--with-deps`, web-first assertions versus non-retrying `isVisible()`, `page.waitForResponse`.
- Changed: `waitForTimeout` is documented as debug-only and `networkidle` as DISCOURAGED, so both are now named.

Method: documentation only; no commands were run.
