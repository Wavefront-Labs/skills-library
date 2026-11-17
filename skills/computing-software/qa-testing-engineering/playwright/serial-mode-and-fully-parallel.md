---
id: computing-software.qa-testing-engineering.playwright.serial-mode-and-fully-parallel
name: serial-mode-and-fully-parallel
category: computing-software
field: qa-testing-engineering
product: playwright
tags: [playwright, serial-mode, fully-parallel, workers, parallelism, test-isolation, playwright-config]
level: practitioner
status: verified
description: "Control Playwright parallelism: workers, fullyParallel, describe.configure serial/parallel modes, worker index for data isolation and when serial tests are justified."
sources:
  - https://playwright.dev/docs/test-parallel
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Serial mode and fullyParallel

**Goal:** maximum parallelism without tests interfering.

## Defaults
- Test files run in parallel across worker processes; tests inside a file run in order in one worker.
- `workers`: default half the CPU cores; set `workers: process.env.CI ? 2 : undefined` or `--workers=4`; percentage like `'50%'`.

## fullyParallel
```ts
export default defineConfig({ fullyParallel: true })
```
Tests within a file also spread across workers (run here with 2 workers and 4 tests: without `fullyParallel` all four ran on worker 0 in order; with `--fully-parallel` they split across workers 0 and 1). Better load balance and sharding; requires full test independence.

## Per-describe modes
```ts
test.describe.configure({ mode: 'parallel' })   // within this file, even if fullyParallel is off
test.describe.configure({ mode: 'serial' })     // run in order; if one fails, the rest are skipped (reported `did not run`)
test.describe.configure({ mode: 'default' })    // in order, but failures don't skip the rest
```
Serial is for genuinely dependent steps (a multi-step wizard sharing one page). Prefer one longer test with `test.step` over serial tests.

## Isolation for parallel runs
- Each test gets a fresh browser context by default.
- Data: unique per test (create via API in a fixture) or partitioned by `testInfo.workerIndex` / `parallelIndex` (e.g. account `user-${parallelIndex}`).
- Shared backend state (feature flags, global settings) changed by a test breaks parallel tests: isolate in a separate project with `workers: 1`.

## Gotchas
- `test.describe.serial` retries the whole group on retry.
- More workers than the SUT can handle cause timeouts that look like flakiness; size workers to the environment.

## Verify
Run with `--repeat-each=3 --workers=8`; no new failures compared with `--workers=1`.
