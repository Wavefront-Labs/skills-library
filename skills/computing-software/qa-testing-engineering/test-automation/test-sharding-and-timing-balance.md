---
id: computing-software.qa-testing-engineering.test-automation.test-sharding-and-timing-balance
name: test-sharding-and-timing-balance
category: computing-software
field: qa-testing-engineering
product: test-automation
tags: [test-sharding, timing-based-splitting, ci-parallelization, ci-integration, test-splitting]
level: practitioner
status: gated
description: "Shard test suites across CI machines and balance by historical timing: Playwright --shard, pytest-split, Jest --shard, CircleCI and Knapsack splitting, and merging results."
sources:
  - https://playwright.dev/docs/test-sharding
  - https://github.com/jerry-git/pytest-split
  - https://jestjs.io/docs/cli#--shard
  - https://circleci.com/docs/parallelism-faster-jobs/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Sharding and balancing suites by timing

**Goal:** cut wall-clock time by splitting tests across N machines so all shards finish at about the same time.

## Count-based sharding (simple)
```bash
npx playwright test --shard=2/4         # splits test files (or tests with fullyParallel) evenly
npx jest --shard=2/4
npx vitest run --shard=2/4
```
Even counts are uneven durations: one shard with the slow specs finishes last. Run on Playwright, Jest 30.5.2 and Vitest (`--shard <index>/<count>` is in each tool's `--help`): `jest --shard=2/4` over 4 test files ran exactly one file (file-level split), and `playwright test --shard=1/2` over a 2-test file and a 1-test file ran the 2-test file only. Playwright splits by file unless `fullyParallel: true` is set, in which case it balances individual tests (Playwright sharding docs).

## Timing-based splitting
**pytest-split**
```bash
pytest --store-durations                          # writes .test_durations (commit it, refresh weekly; run with pytest-split 0.11.0, it was created)
pytest --splits 4 --group 2 --splitting-algorithm least_duration
```
pytest-split with `--splits 2 --group 1` and `--group 2` over 8 tests ran 4 and 4 (`--splitting-algorithm` accepts `duration_based_chunks` or `least_duration`).
**CircleCI**
```bash
circleci tests glob "tests/**/*_test.py" | circleci tests run --command="xargs pytest" --split-by=timings
```
needs `store_test_results` so timings are recorded.
**Knapsack Pro / split_tests / gotestsum**: queue mode hands tests to whichever node is free (dynamic balancing).
**Cypress Cloud** `--parallel --record` balances spec files by history.

## GitHub Actions matrix
```yaml
strategy:
  fail-fast: false
  matrix: { shard: [1, 2, 3, 4] }
steps:
  - run: npx playwright test --shard=${{ matrix.shard }}/4 --reporter=blob
  - uses: actions/upload-artifact@v4   # v4 was current in older guides; the latest release was v7.0.2 on 2026-10-07, check the release page
    with: { name: blob-${{ matrix.shard }}, path: blob-report }
```
Merge results afterwards (Playwright `merge-reports`, JUnit XML collected per shard). `--reporter=blob` wrote `blob-report/report-1.zip` and `npx playwright merge-reports --reporter=list blob-report` printed the merged results locally. The CircleCI, Knapsack Pro, gotestsum, Cypress Cloud and GitHub Actions matrix steps were not run (gated: unconfirmed, source is paywalled or blocked). Reason: no CI or paid-account access here.

## Choosing N
Total time ~ setup per shard + longest shard. Adding shards stops helping when setup (install, build, browser download) dominates; cache dependencies first.

## Gotchas
- `fail-fast: true` cancels other shards and hides failures.
- Stale timing data drifts; refresh durations regularly.
- Tests sharing state across files break when split differently each time; sharding exposes order dependence.

## Verify
Shard durations are within ~15% of each other, merged report shows all tests once, and total pipeline time dropped.
