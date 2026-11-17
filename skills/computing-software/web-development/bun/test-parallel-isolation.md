---
id: computing-software.web-development.bun.test-parallel-isolation
name: test-parallel-isolation
category: computing-software
field: web-development
product: bun
tags: [test-parallel, test-isolate, test-shard, worker-id]
level: advanced
status: docs-checked
description: "Speed up large bun test suites with --parallel, --isolate modes, --shard across CI machines, timing files and per-worker IDs, and know their trade-offs."
sources:
  - https://raw.githubusercontent.com/oven-sh/bun/main/docs/test/parallel.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
```bash
bun test --parallel                  # one worker per core; implies --isolate
bun test --parallel=4 --isolate=modules
bun test --parallel --no-isolate     # fastest; files share a global per worker
bun test --shard=2/4 --parallel      # CI machine 2 of 4
bun test --timings=.bun-test-timings.json --update-timings
bun test --shard=2/8 --parallel --timings=.bun-test-timings.json
```

Isolation:
- `--isolate`: each file gets a fresh `globalThis` and module registry; leftover servers, sockets, timers and subprocesses are closed and `--preload` scripts rerun.
- `--isolate=modules`: one global, but per-file module copies (faster; built-in exports are shared).

Config and IDs: `concurrentTestGlob` in `bunfig.toml` enables concurrency only for matching files. Workers get `BUN_TEST_WORKER_ID` (1-based) plus `JEST_WORKER_ID`, `VITEST_POOL_ID`, `VITEST_WORKER_ID`; use them to pick per-worker databases, ports or temp dirs. `--parallel-delay=<ms>` defaults to 5.

Gotchas:
- A crashed worker (`process.exit`) fails that file and is replaced; a fatal signal aborts the run.
- `--bail` is per file: running files finish.
- Without `--timings`, `--shard` balances by file count, not duration.
- For many small files with a large shared import graph, plain `bun test` can beat `--parallel`; benchmark both.

## Checked

2026-11-04. Confirmed against the Bun docs page test/parallel: --parallel[=N] implying --isolate, --no-isolate, --isolate=modules and its comparison table, --shard distribution by file count, --timings and --update-timings, worker environment variables (1-based), --parallel-delay default 5, concurrentTestGlob, per-file --bail, crashed worker handling, and the small-files caveat. Nothing removed.
Method: documentation only; no commands were run.
