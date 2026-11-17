---
id: computing-software.qa-testing-engineering.playwright.api-testing-and-route-mocking
name: api-testing-and-route-mocking
category: computing-software
field: qa-testing-engineering
product: playwright
tags: [playwright, api-testing, apirequestcontext, page-route, route-fulfill, network-mocking, request-interception, har-replay, schema-validation, test-setup-via-api, storage-state, auth-bypass, javascript, typescript]
level: practitioner
status: verified
description: "Use Playwright's APIRequestContext for backend contract tests and page.route for network mocking, and seed/auth E2E tests via API instead of the UI for speed and stability."
sources: ["https://playwright.dev/docs/api-testing", "https://playwright.dev/docs/network", "https://playwright.dev/docs/auth"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Playwright: API testing and route mocking

**Goal:** use Playwright for more than browser E2E — direct API tests for backend
contracts, and `page.route` to control network responses for UI tests that would
otherwise depend on fragile real-world conditions.

## 1. API testing with APIRequestContext
`request` runs outside the browser (no cookies/CORS quirks baked in automatically
unless you choose to share storage state), making it fast and suited to pure
backend checks:
```ts
test('order total is correct', async ({ request }) => {
  const res = await request.post('/api/orders', { data: { sku: 'A1', qty: 2 } })
  expect(res.status()).toBe(201)
  expect((await res.json()).total).toBeCloseTo(39.98, 2)
})
```
Share a `baseURL` via `playwright.config.ts` (`use: { baseURL }`) so API and UI
tests hit the same environment consistently.

## 2. Seeding state and bypassing login via API
The highest-leverage Playwright pattern: authenticate and seed data via the API in
a `setup` project, save `storageState` to disk, and have every real test reuse it
— skip the login UI entirely except in a dedicated login test:
```ts
// auth.setup.ts
const res = await request.post('/auth/login', { data: creds })
await context.storageState({ path: 'playwright/.auth/user.json' })
// playwright.config.ts: { use: { storageState: 'playwright/.auth/user.json' }, dependencies: ['setup'] }
```
This is usually the single biggest speed-up available to a Playwright suite —
logging in through the UI once per test can dominate total runtime.

## 3. Route mocking with page.route
Intercept and control responses for UI tests that need a hard-to-produce state:
```ts
await page.route('**/api/products*', route => route.fulfill({ json: productsFixture }))
await page.route('**/api/orders', route => route.fulfill({ status: 500, json: { error: 'boom' } }))
await page.route('**/api/slow', route => new Promise(r => setTimeout(() => r(route.continue()), 3000)))
```
Register routes **before** the navigation/action that triggers the request — a
route added after the request fires does nothing, the same ordering trap as other
tools' network interception. Use `route.continue({ headers, url })` to modify a
real request rather than fully replacing it, when you want to pass through to the
real backend with one field changed.

## 4. HAR-based mocking for whole-page realism
`page.routeFromHAR('trace.har', { update: false })` replays a previously recorded
set of network responses verbatim — useful for a complex page with many
third-party calls (analytics, ads, fonts) you don't want to hand-stub individually.
Record with `recordHar` in a dedicated capture run; don't hand-edit a HAR file,
regenerate it when the app's requests change.

## 5. When to use API tests vs. route-mocked UI tests vs. real E2E
- **Pure API test**: verifying backend contract/business logic — fastest, no browser.
- **Route-mocked UI test**: verifying the UI reacts correctly to a given
  response/error — fast, deterministic, doesn't prove the real backend returns
  that shape.
- **Unmocked E2E**: a small number of true smoke tests against the real backend,
  to catch contract drift the mocked tests structurally can't see (mirrors the
  same tradeoff in `cypress.api-testing-and-ci-parallelization`).

## Run notes
Run on Playwright 1.64: `request.post('/api/orders')` against a `baseURL` server returned 201 and `toBeCloseTo(39.98, 2)` passed; `route.fulfill({ json })` and `{ status: 500, json }` mocked a `**/api/products*` URL including its query string; a route that delayed `route.continue()` by 1 s took about 1.02 s; `route.continue({ headers })` passed through (200). A context recorded with `recordHar` produced a file, and `routeFromHAR(file, { update: false })` replayed the page and the recorded GET; a request that was not in the HAR failed (`Failed to fetch`). Replay of non-GET requests was not tested; check the release notes for your version.

## Verify
- [ ] Auth/state seeded via API + `storageState`, not the login UI, for non-auth tests.
- [ ] Every `page.route` registered before the triggering navigation/action.
- [ ] At least one unmocked smoke E2E test exists per critical flow.
- [ ] Mocked error/slow states exist for each critical API the UI depends on.
- [ ] API tests assert response shape, not just status code.
