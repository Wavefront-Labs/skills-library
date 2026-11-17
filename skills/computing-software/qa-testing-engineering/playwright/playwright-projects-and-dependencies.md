---
id: computing-software.qa-testing-engineering.playwright.playwright-projects-and-dependencies
name: playwright-projects-and-dependencies
category: computing-software
field: qa-testing-engineering
product: playwright
tags: [playwright, playwright-projects, playwright-config, setup-project, project-dependencies, cross-browser, environments]
level: practitioner
status: verified
description: "Use Playwright projects to run the same tests across browsers, devices and environments, and project dependencies for setup like authentication and seeding."
sources:
  - https://playwright.dev/docs/test-projects
  - https://playwright.dev/docs/test-global-setup-teardown
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Playwright projects and dependencies

**Goal:** one config that runs tests in several configurations, with setup steps modelled as projects.

## Config
```ts
// playwright.config.ts
import { defineConfig, devices } from '@playwright/test'
export default defineConfig({
  testDir: './tests',
  use: { baseURL: process.env.BASE_URL ?? 'http://localhost:3000', trace: 'on-first-retry' },
  projects: [
    { name: 'setup', testMatch: /.*\.setup\.ts/ },
    { name: 'chromium', use: { ...devices['Desktop Chrome'], storageState: 'playwright/.auth/user.json' },
      dependencies: ['setup'] },
    { name: 'webkit', use: { ...devices['Desktop Safari'], storageState: 'playwright/.auth/user.json' },
      dependencies: ['setup'] },
    { name: 'mobile', use: { ...devices['Pixel 7'] }, testMatch: /.*mobile.*\.spec\.ts/ },
    { name: 'cleanup', testMatch: /global\.teardown\.ts/ },
  ],
})
```
Add `teardown: 'cleanup'` on the setup project to run cleanup after all dependents finish.

## Running
```bash
npx playwright test --project=chromium
npx playwright test --project=chromium --project=webkit
```
Dependencies run first automatically; filtering to one project still runs its dependencies (skip with `--no-deps`, which per the docs also ignores teardowns). Run here with `--project=chromium`: `setup` ran first, then `chromium`, then the `cleanup` teardown project; with `--no-deps` only `chromium` ran. Add `teardown: 'cleanup'` as above for that order.

## Patterns
- Environments as projects (`staging`, `prod-smoke`) with different `baseURL` and `testMatch`/`grep`.
- `testIgnore`/`testMatch` to route specs to projects (mobile-only specs).
- Per-project `retries`, `timeout`, `fullyParallel`.

## Why dependencies beat globalSetup
Setup runs as a test: it appears in the HTML report, gets traces, fixtures and retries.

## Gotchas
- All projects share the same `testDir` by default; a spec matched by several projects runs once per project (often desired, sometimes a surprise).
- Each project multiplies runtime; keep the full suite on one engine, run only critical tests on the rest.

## Verify
`npx playwright test --list` shows each test under the expected projects; HTML report shows setup as a separate project.
