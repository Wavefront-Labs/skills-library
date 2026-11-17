---
id: computing-software.devops-ci-cd.ci-pipeline-design.test-parallelisation-and-sharding
name: test-parallelisation-and-sharding
category: computing-software
field: devops-ci-cd
product: ci-pipeline-design
tags: [ci-pipeline-design, test-parallelisation, test-sharding, sharding, test-splitting, timing-based-splitting, pytest-xdist, jest-shard, playwright-shard, merge-reports, circleci-tests-split, matrix-jobs, fail-fast]
level: practitioner
status: docs-checked
description: "Cut test wall-clock by parallelising in-process and sharding across machines: pytest-xdist, Jest and Playwright shards, CircleCI timing splits."
sources: ["https://pytest-xdist.readthedocs.io/en/stable/distribution.html", "https://jestjs.io/docs/cli", "https://playwright.dev/docs/test-sharding", "https://circleci.com/docs/parallelism-faster-jobs/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Test parallelisation and sharding

**Goal:** the test stage finishes in a target time regardless of suite growth, with shards of similar length and no new flakiness from concurrency.

(Where tests sit in the pipeline and flaky-test policy are in `computing-software.devops-ci-cd.ci-pipeline-design.fast-feedback-pipeline-design`.)

## 1. Two levels
1. **In-process workers on one machine** (cheap, no extra checkout): `pytest -n auto` (pytest-xdist), Jest `--maxWorkers`.
2. **Sharding across machines** when one machine is saturated: CI matrix jobs each running a slice.

Max out level 1 first.

## 2. Tool behaviour
- **pytest-xdist:** `-n auto` uses physical CPU cores; `-n logical` uses logical cores (needs psutil); `-n 8` is explicit; `-n 0` disables xdist. Override auto with `PYTEST_XDIST_AUTO_NUM_WORKERS` or the `pytest_xdist_auto_num_workers` hook. Distribution via `--dist`: `load` (default), `loadscope` (group by module or class, useful with expensive module- or class-level fixtures), `loadfile` (all tests of a file on one worker), `loadgroup` (by `xdist_group` mark), `worksteal` (better for tests of very different duration, similar or better fixture reuse), `no`.
- **Jest:** `--shard=1/3` selects shard index of count (both 1-based, index <= count); the configured `testSequencer` must implement a `shard` method. `--maxWorkers=<num>` defaults to cores minus one in single-run mode; percentages like `--maxWorkers=50%` suit variable-CPU environments. `--randomize` shuffles test order inside `describe` blocks using `--seed`; rerun with the same seed to reproduce flaky failures.
- **Playwright:** `npx playwright test --shard=x/y`. By default it shards test files; with `fullyParallel: true` it shards individual tests for more even balance. Without it, keep test files small and evenly sized. Statically skipped tests are not counted when balancing.
- **CircleCI:** `parallelism: N` creates N executors; `circleci tests run` (Cloud only; `circleci tests split` on Server) splits by name, `--split-by=filesize`, or `--split-by=timings` using historic timing data from the previous run (`--timings-type` picks granularity). With self-hosted runners you need at least as many runners as the parallelism or tasks queue.

## 3. Merge the results
- Playwright: use the `blob` reporter on CI (`reporter: process.env.CI ? 'blob' : 'html'`), upload each shard's `blob-report`, download them into one directory and run `npx playwright merge-reports --reporter html ./all-blob-reports`. Blob names include the shard number, so they do not clash. Use `fail-fast: false` in the matrix so all shards' failures are visible, and run the merge job with `if: ${{ !cancelled() }}`.
- A GitHub Actions matrix such as `shardIndex: [1, 2, 3, 4]` with `shardTotal: [4]` passes `--shard=${{ matrix.shardIndex }}/${{ matrix.shardTotal }}`.

## Verify
- [ ] Shard durations are close to each other across recent main runs.
- [ ] Shard failures are all visible (fail-fast off) and reports merge into one view.
- [ ] The suite is green with random order (Jest `--randomize`) before and after turning on parallelism.

## Checked
Method: docs-checked 2026-11-09 against the pytest-xdist distribution page, the Jest CLI page (`--shard`, `--maxWorkers`, `--randomize`), the Playwright sharding page (full) and the CircleCI test splitting page (parallelism and splitting sections).
Removed as unconfirmed: the claim that Jest and Playwright shard by file count/hash not time, `pytest-split` flags (`--splits`, `--group`, `--durations-path`), Knapsack Pro and dynamic-queue descriptions, the cgroup CPU oversubscription remark, Go, JUnit 5 and RSpec parallel settings, per-worker database, port and tmp-file isolation advice (including `PYTEST_XDIST_WORKER` and `JEST_WORKER_ID` use), coverage combine instructions and `--fail-under`, the Amdahl and setup-time guidance and the within-20% shard spread target, and `pytest -p randomly`.
