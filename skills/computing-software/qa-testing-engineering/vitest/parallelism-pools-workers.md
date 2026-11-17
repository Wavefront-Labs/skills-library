---
id: computing-software.qa-testing-engineering.vitest.parallelism-pools-workers
name: parallelism-pools-workers
category: computing-software
field: qa-testing-engineering
product: vitest
tags: [pool, file-parallelism, max-workers, vm-forks]
level: practitioner
status: docs-checked
description: "Control how Vitest runs test files in parallel: pool choice (forks, threads, vmForks, vmThreads), maxWorkers, and turning file parallelism off for debugging."
sources:
  - https://raw.githubusercontent.com/vitest-dev/vitest/main/docs/guide/parallelism.md
  - https://raw.githubusercontent.com/vitest-dev/vitest/main/docs/guide/debugging.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Test files run in parallel, each in a worker, according to the `pool` option: `forks` (default), `threads`, `vmForks`, `vmThreads`. The worker count is capped by `maxWorkers`.

```ts
export default defineConfig({
  test: {
    pool: 'threads',
    maxWorkers: 4,
    fileParallelism: false, // one file at a time
  },
})
```

CLI equivalents: `--no-file-parallelism` and `--isolate false`.

Inside a single file, tests run one after another in definition order unless you opt into concurrency (`test.concurrent`, `describe.concurrent`).

Use `vitest doctor` to measure alternative pool, isolate and maxWorkers settings against your own suite instead of guessing.

When debugging, use `--no-file-parallelism` (and `--test-timeout=0`) so breakpoints do not race other files.

`vitest doctor` validates an `isolate: false` candidate by running the suite twice with a shuffled file order; a test that depends on isolation makes the candidate fail instead of being recommended.

## Checked

2026-11-04. Confirmed against guide/parallelism.md, guide/debugging.md and guide/cli.md: the four pools and the forks default, `maxWorkers`, `fileParallelism`, `--no-file-parallelism`, `--isolate false`, `--test-timeout=0`, sequential tests within a file, and the vitest doctor behaviour. Removed: an unstated gotcha, replaced by the documented doctor validation.

Method: documentation only; no commands were run.
