---
id: computing-software.qa-testing-engineering.playwright.max-failures-and-forbid-only
name: max-failures-and-forbid-only
category: computing-software
field: qa-testing-engineering
product: playwright
tags: [max-failures, forbidonly, ci-guards, playwright-config]
level: practitioner
status: verified
description: "Guard Playwright CI runs with forbidOnly to block committed test.only, maxFailures to stop runaway failures, and related fail-fast settings."
sources:
  - https://playwright.dev/docs/api/class-testconfig#test-config-forbid-only
  - https://playwright.dev/docs/api/class-testconfig#test-config-max-failures
  - https://playwright.dev/docs/test-cli
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# maxFailures and forbidOnly CI guards

**Goal:** CI never silently runs a subset, and never burns an hour on a broken environment.

## forbidOnly
```ts
forbidOnly: !!process.env.CI,
```
A committed `test.only` / `test.describe.only` makes the run fail immediately with the offending location, instead of running one test and reporting green (without the flag the same file ran just the focused test and passed). CLI: `--forbid-only`; config key `forbidOnly`.

Add a lint rule too: `eslint-plugin-playwright` rule `playwright/no-focused-test`.

## maxFailures
```ts
maxFailures: process.env.CI ? 10 : undefined,
```
CLI `-x` (stop after first failure) or `--max-failures=10`. When reached, the remaining tests are reported as `did not run` and the run fails (run here: 6 failing tests, `--max-failures=2` gave `2 failed, 4 did not run`; `-x` gave `1 failed, 5 did not run`). Retries do not add to the count: with `--retries=2` each test that failed all three attempts counted once.

Good values: around 5-10% of the suite, or lower for smoke stages. An environment outage then fails in minutes.

## Related
- `--fail-on-flaky-tests` for release pipelines.
- `globalTimeout` caps total time (e.g. 60 min).
- `--pass-with-no-tests` only for jobs where empty selection is legitimate (`--only-changed`).

## Gotchas
- `maxFailures` leaves tests unrun, so the report undercounts real failures; rerun fully after fixing the environment.
- Sharding: each shard counts its own failures.

## Verify
Commit a `test.only` on a branch: the run fails with `Error: item focused with '.only' is not allowed due to the '--forbid-only' CLI flag: "only.spec.ts focused"` (Playwright 1.64; wording may differ with the config key or other versions).
