---
id: computing-software.web-development.nextjs.testing-nextjs-apps
name: testing-nextjs-apps
category: computing-software
field: web-development
product: nextjs
tags: [nextjs, nextjs-testing, vitest, jest, playwright, react-testing-library, web-development]
level: practitioner
status: docs-checked
description: "Testing Next.js App Router apps: Vitest with React Testing Library for sync components, and Playwright E2E against a production build for async server components."
sources:
  - https://nextjs.org/docs/app/guides/testing
  - https://nextjs.org/docs/app/guides/testing/vitest
  - https://nextjs.org/docs/app/guides/testing/playwright
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Testing Next.js apps

**Goal:** fast unit tests where they work and E2E where the framework matters.

## 1. What tool for what
The Next.js testing overview lists unit, component, integration, end-to-end and snapshot tests, with guides for Cypress, Jest (unit and snapshot), Playwright (E2E) and Vitest (unit).

| Code | Tool (per the Next.js docs) |
|---|---|
| Client components, synchronous server components | Vitest with React Testing Library (Jest also has a guide) |
| Async server components | E2E; the docs say some tools do not fully support them yet and Vitest does not support them |
| User flows in a browser | Playwright (Chromium, Firefox and WebKit) |

## 2. Vitest setup
Install `vitest @vitejs/plugin-react jsdom @testing-library/react @testing-library/dom vite-tsconfig-paths` (the last for TypeScript) as dev dependencies, and add `"test": "vitest"` to `package.json`. Vitest watches for changes by default.
```ts
// vitest.config.mts
import { defineConfig } from "vitest/config";
import react from "@vitejs/plugin-react";
import tsconfigPaths from "vite-tsconfig-paths";
export default defineConfig({ plugins: [tsconfigPaths(), react()], test: { environment: "jsdom" } });
```
Example test: `render(<Page />)` then `screen.getByRole("heading", { level: 1, name: "Home" })`. Test files may sit in a `__tests__` folder or be colocated inside the app router.

## 3. Playwright
Set up with `pnpm create playwright` (or the `with-playwright` example). The docs recommend running tests against production code: `npm run build`, `npm run start`, then `npx playwright test` in another terminal. Alternatively, use Playwright's `webServer` feature to start the server and wait for it. Setting `baseURL` in `playwright.config.ts` lets tests use `page.goto("/")`. On CI, `npx playwright install-deps` installs the dependencies; Playwright is headless by default.
```ts
test("should navigate to the about page", async ({ page }) => {
  await page.goto("/");
  await page.click("text=About");
  await expect(page).toHaveURL("/about");
  await expect(page.locator("h1")).toContainText("About");
});
```
With Cache Components, the `instant()` helper from `@next/playwright` asserts what is visible right after a navigation, before dynamic content streams in.

## Verify
- [ ] CI runs unit tests and Playwright against a production build.
- [ ] At least one E2E per critical flow.

## Checked
2026-11-09. Read the three cited Next.js testing pages in full. Removed (not on those pages): Jest `next/jest` configuration, mocking `next/navigation` and `next/cache`, server-action unit tests and the `redirect()` assertion, `storageState`, MSW and `page.route` mocking, seeding a test database, the `vitest.setup.ts` file, and the mswjs source (not read).
Method: documentation only; no commands were run.
