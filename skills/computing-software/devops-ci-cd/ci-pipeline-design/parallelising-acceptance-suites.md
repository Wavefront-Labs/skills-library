---
id: computing-software.devops-ci-cd.ci-pipeline-design.parallelising-acceptance-suites
name: parallelising-acceptance-suites
category: computing-software
field: devops-ci-cd
product: ci-pipeline-design
tags: [ci-pipeline-design, acceptance-parallelisation, acceptance-tests, test-isolation]
level: advanced
status: docs-checked
description: "Run Playwright and Cypress e2e suites in parallel safely: per-test and per-worker isolation, locks, sharding and report merging."
sources: ["https://playwright.dev/docs/test-parallel", "https://playwright.dev/docs/test-sharding", "https://docs.cypress.io/cloud/features/smart-orchestration/parallelization"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Parallelising acceptance suites

E2E suites grow to hours serially. Parallelism needs **isolation** first.

## Isolation strategies (Playwright)
Each worker is a separate OS process with its own BrowserContext, so cookies, storage and in-memory globals are already isolated. Flakiness comes from state outside a single test.

| Shared thing | Isolation |
|---|---|
| Backend records | derive ids from `testInfo.testId` (for example `order-${testInfo.testId}`) so parallel tests never collide |
| Files | write to `testInfo.outputPath('export.csv')`, scoped to the current test |
| Data shared by many tests | create it once per worker in a worker-scoped fixture keyed on `testInfo.workerIndex` (for example a DB user `user-${workerIndex}`), delete it after |
| Resource that cannot take concurrent access (external service, global account setting) | named lock: `test('...', { lock: 'user-settings' }, ...)`; tests sharing a name never run together, across files, workers and projects |
| Test sensitive to any concurrent activity | built-in `{ lock: '-exclusive-' }`: starts only when nothing else runs, nothing starts until it ends |

Keep tests independent: a test that leaks state through a module-level variable or relies on another test's side effects breaks once tests run in parallel or in a different order. `test.describe.configure({ mode: 'serial' })` exists for inter-dependent tests (later tests are skipped after a failure, the group retries together) but Playwright says it is not recommended.

## In-machine workers (Playwright)
- Test files run in parallel by default; tests inside a file run in order in one worker.
- `fullyParallel: true` (config or per project) runs every test in parallel; `test.describe.configure({ mode: 'parallel' })` does it for one file; `{ mode: 'default' }` opts a describe back out.
- `workers: process.env.CI ? 2 : undefined` or `--workers 4` caps workers; `workers: 1` disables parallelism.
- Workers cannot talk to each other. A worker is shut down after a test failure so later tests get a clean environment.
- `testInfo.workerIndex` is unique per worker process and a restarted worker gets a new one; `testInfo.parallelIndex` runs 0 to workers-1 and is kept by the replacement worker. Env vars: `TEST_WORKER_INDEX`, `TEST_PARALLEL_INDEX`.
- `maxFailures` / `--max-failures=10` stops the run after N failures so a broken suite does not burn CI time.

## Across machines
```bash
npx playwright test --shard=2/6
npx playwright merge-reports --reporter html ./all-blob-reports
```
- Playwright shards only what can run in parallel: whole files by default, individual tests with `fullyParallel: true` (preferred for even balance). Without it keep files small and evenly sized.
- Use `reporter: process.env.CI ? 'blob' : 'html'`, collect every shard's `blob-report` into one directory (names include the shard number), then run `merge-reports`. Use `fail-fast: false` in the GitHub Actions matrix and `if: ${{ !cancelled() }}` on the merge job. Details in `computing-software.devops-ci-cd.ci-pipeline-design.test-parallelisation-and-sharding`.
- Cypress: `cypress run --record --key=<key> --parallel`. `--record` is required. Parallelisation is per spec file, balanced by Cypress Cloud using each spec's previous run history, so spec order is not guaranteed; specs of similar duration parallelise best. Cypress does not recommend parallel runs on a single machine.
- Cypress links CI machines into one run by CI build ID, read from provider variables (for example `CIRCLE_WORKFLOW_ID`, `CI_PIPELINE_ID`, `BUILD_NUMBER`); override with `--ci-build-id $BUILD_TAG` if another variable is more unique.
- After the last machine finishes, Cypress Cloud waits the Run Completion Delay (60 seconds by default, set in project settings) before closing the run.
- `--group <name>` labels several `cypress run` calls inside one run (browsers, or parts of a monorepo with `--spec`); the name must be unique within the run and machines must share a CI build ID.

## Verify
- [ ] Running the suite twice in parallel (two pipelines) produces no cross-test failures; merged report shows all tests once.
- [ ] No test depends on file or test order.

## Checked
Method: docs-checked 2026-11-09 against the Playwright parallelism page and sharding page (both full) and the Cypress Cloud parallelization page (full).
Removed as unconfirmed: the account-pool-per-worker, tenant-per-worker, serial-project-for-global-settings and never-truncate-shared-tables rows, the `order-${workerIndex}-${uuid}` id recipe, the 6 shards x 4 workers = 24 sessions rate-limit, DB-connection and payment-sandbox advice and per-PR ephemeral environments, and the `$RUN_ID` build id (Cypress documents `$BUILD_TAG` as an example). Serial mode was changed from a recommended tool to a not-recommended one per the Playwright note.
