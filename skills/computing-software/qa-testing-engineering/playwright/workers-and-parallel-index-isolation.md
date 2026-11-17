---
id: computing-software.qa-testing-engineering.playwright.workers-and-parallel-index-isolation
name: workers-and-parallel-index-isolation
category: computing-software
field: qa-testing-engineering
product: playwright
tags: [playwright-workers, parallelindex, workerindex, test-isolation-playwright, parallelism]
level: practitioner
status: verified
description: "Size Playwright workers, and use workerIndex and parallelIndex to give each worker its own account, database schema or port so parallel tests never collide."
sources:
  - https://playwright.dev/docs/test-parallel
  - https://playwright.dev/docs/api/class-workerinfo
  - https://playwright.dev/docs/test-parallel#isolate-test-data-between-parallel-workers
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Worker count, workerIndex and parallelIndex isolation

**Goal:** maximum parallelism with zero shared-data collisions.

## Workers
```ts
workers: process.env.CI ? 4 : undefined,  // default: half the logical CPUs
fullyParallel: true,
```
CLI: `--workers=50%` or `--workers=1` for debugging order issues. More workers than CPU cores slows browsers and causes timeouts; measure.

## Indexes
- `workerInfo.workerIndex`: unique per worker process, increments when a worker restarts after a failure (0,1,2,3,4...).
- `workerInfo.parallelIndex`: slot number 0..workers-1, reused after restarts. Use this to map to a **fixed pool** of resources.
- Also available as env `TEST_WORKER_INDEX` and `TEST_PARALLEL_INDEX` (run here after two failures: `workerIndex` 2, `parallelIndex` 0, env vars `2` and `0`).

## Per-worker account
```ts
export const test = base.extend<{}, { account: { user: string; pass: string } }>({
  account: [async ({}, use, workerInfo) => {
    const user = `e2e-user-${workerInfo.parallelIndex}`;   // pre-provisioned e2e-user-0..7
    await resetAccount(user);
    await use({ user, pass: process.env.E2E_PASS! });
  }, { scope: 'worker' }],
});
```
Same pattern: DB schema `test_${parallelIndex}`, port `3000 + parallelIndex`, storage-state file per worker.

## Gotchas
- `workerIndex` grows unbounded across restarts; mapping it to a fixed pool overflows. Use `parallelIndex`.
- Sharding multiplies: shard 1 and shard 2 both have parallelIndex 0. Include the shard (`SHARD_INDEX` env you set) in resource names when shards share an environment.
- Tests creating unique data (`Date.now()` + random) are simpler than pools when the app allows it.

## Verify
Run with `--repeat-each=3 --workers=4`; no failures caused by duplicate data or "already exists" errors.
