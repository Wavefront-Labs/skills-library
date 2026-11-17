---
id: computing-software.qa-testing-engineering.playwright.environment-config-and-baseurl
name: environment-config-and-baseurl
category: computing-software
field: qa-testing-engineering
product: playwright
tags: [playwright-env, baseurl, dotenv, playwright-config, multi-environment]
level: practitioner
status: docs-checked
description: "Run one Playwright suite against local, staging and production-like environments using baseURL, env vars, dotenv and per-environment projects without leaking secrets."
sources:
  - https://playwright.dev/docs/test-parameterize
  - https://playwright.dev/docs/api/class-testoptions#test-options-base-url
  - https://playwright.dev/docs/test-projects
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Environment-specific config and baseURL

**Goal:** `ENV=staging npx playwright test` just works.

## baseURL
```ts
use: { baseURL: process.env.BASE_URL ?? 'http://127.0.0.1:3000' }
// in tests:
await page.goto('/login');                 // resolved against baseURL
await request.get('/api/health');          // the request fixture respects baseURL too
```
The base URL is combined with the `URL()` constructor. Per the docs: `http://localhost:3000` with `/bar.html` gives `http://localhost:3000/bar.html`; `http://localhost:3000/foo/` with `./bar.html` gives `http://localhost:3000/foo/bar.html`; `http://localhost:3000/foo` (no trailing slash) with `./bar.html` gives `http://localhost:3000/bar.html`. If the app lives under a sub-path, keep the trailing slash and use relative paths.

## dotenv
```ts
// playwright.config.ts
import dotenv from 'dotenv';
import path from 'path';
dotenv.config({ path: path.resolve(__dirname, `.env.${process.env.ENV ?? 'local'}`) });
```
The docs suggest `dotenv` with `.env` files for managing environment variables. Keep real `.env.*` files out of git and inject secrets in CI as masked variables.

## Projects per environment
```ts
projects: [
  { name: 'staging', use: { baseURL: 'https://staging.example.com' }, grepInvert: /@destructive/ },
  { name: 'prod-smoke', use: { baseURL: 'https://www.example.com' }, grep: /@smoke/ },
]
```
`npx playwright test --project=prod-smoke`.

## Gotchas
- Environment variables passed on the command line are read when the config file loads, so set them before running `npx playwright test`.
- Don't branch test logic heavily on environment; tag tests instead (`@destructive`, `@smoke`).
- Never run data-mutating tests against production; enforce with `grepInvert` in the prod project.

## Verify
`ENV=staging npx playwright test --list --project=staging` shows the expected subset, and a `page.goto('/')` lands on the expected host.

## Checked

2026-10-25: checked against the Playwright docs (microsoft/playwright main, docs/src, commit of 2026-10-24). Confirmed: baseURL resolution through the URL() constructor with the documented examples, baseURL applying to page navigation and the request fixture, reading environment variables in the config from the command line, the dotenv pattern, and the project-level grep and grepInvert properties. Removed: the claim about worker processes inheriting environment variables, which the docs do not state.

Method: documentation only; no commands were run.
