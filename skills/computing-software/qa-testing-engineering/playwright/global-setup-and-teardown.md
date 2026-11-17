---
id: computing-software.qa-testing-engineering.playwright.global-setup-and-teardown
name: global-setup-and-teardown
category: computing-software
field: qa-testing-engineering
product: playwright
tags: [playwright, global-setup, global-teardown, playwright-config, test-environment-setup]
level: practitioner
status: verified
description: "Choose between Playwright project dependencies and globalSetup/globalTeardown files for suite-wide setup like seeding, starting services and environment checks."
sources:
  - https://playwright.dev/docs/test-global-setup-teardown
  - https://playwright.dev/docs/test-webserver
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Playwright global setup and teardown

**Goal:** run once-per-suite work (seed DB, start servers, check environment) reliably.

## Option 1 (recommended): setup project
See `playwright-projects-and-dependencies`. Visible in reports, traceable, supports fixtures.

## Option 2: globalSetup file
```ts
// playwright.config.ts
export default defineConfig({
  globalSetup: require.resolve('./global-setup'),
  globalTeardown: require.resolve('./global-teardown'),
})
```
```ts
// global-setup.ts
import { FullConfig, request } from '@playwright/test'
export default async function globalSetup(config: FullConfig) {
  const ctx = await request.newContext({ baseURL: config.projects[0].use.baseURL })
  const health = await ctx.get('/health')
  if (!health.ok()) throw new Error(`SUT unhealthy: ${health.status()}`)
  await ctx.post('/api/test/seed', { data: { dataset: 'baseline' } })
  process.env.RUN_ID = Date.now().toString()   // available to workers
  await ctx.dispose()
}
```
Values in `process.env` set here are visible to tests (run here: a test printed the `RUN_ID` set in globalSetup). A function returned from globalSetup acts as teardown (run here: it ran after the last project finished). `config.projects[0].use.baseURL` was the configured `baseURL`.

## Starting the app: webServer
```ts
webServer: { command: 'npm run start', url: 'http://localhost:3000', reuseExistingServer: !process.env.CI, timeout: 120_000 }
```
Multiple servers: an array of webServer entries.

## Gotchas
- globalSetup has no fixtures and no trace recording, is not shown in the HTML report, and browser management is manual (docs comparison table); failures are harder to debug.
- Seeding in global setup creates shared data; parallel tests mutating it conflict. Prefer per-test data via fixtures and keep global data read-only.

## Verify
Stop the app: the run fails fast in setup with a clear message, not 200 timeouts.
