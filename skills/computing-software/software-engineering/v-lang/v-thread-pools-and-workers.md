---
id: computing-software.software-engineering.v-lang.v-thread-pools-and-workers
name: v-thread-pools-and-workers
category: computing-software
field: software-engineering
product: v-lang
tags: [v-thread-pools-and-workers, shared-state-and-sync, thread pool, worker pool, sync.pool, parallel, nr_cpus, job queue, pool processor, v-lang]
level: advanced
status: docs-checked
description: "Build worker pools with channels, use sync.pool's PoolProcessor, and size workers to the CPU count."
sources:
  - https://docs.vlang.io/
  - https://modules.vlang.io/
  - https://github.com/vlang/v
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Worker pools and parallel processing

Goal: process many tasks with bounded parallelism.

- Manual pool: `jobs := chan Job{cap: 100}`, `results := chan Res{cap: 100}`; spawn `runtime.nr_cpus()` workers each looping `for j in jobs { results <- work(j) }`; close `jobs` after enqueueing; wait for workers then close `results`.
- `import sync.pool`: `mut pp := pool.new_pool_processor(callback: handler, maxjobs: 4)` then `pp.work_on_items(items)` and collect with `pp.get_results[T]()`; the config struct also has `maxjobs` and `callback` and the processor has `set_max_jobs`.
- CPU count: `import runtime; runtime.nr_cpus()` (also `runtime.nr_jobs()`).
- Return partial results through result structs containing the error.

Gotchas:
- Close channels from the one owner only.
- Do not share a plain `mut` slice among workers; give each worker its own range.

Verify: process 1000 items with 4 workers and compare to the sequential sum.

## Checked

2026-11-03. Confirmed against the V repository source (vlib modules and doc/docs.md) read in this batch: sync.pool PoolProcessor, PoolProcessorConfig (maxjobs, callback), new_pool_processor, work_on_items, get_results[T], set_max_jobs (vlib/sync/pool/pool.c.v), runtime.nr_cpus and nr_jobs (vlib/runtime), buffered channels with cap (doc/docs.md, Channels).
Removed or corrected: 'arrays parallel helpers' from the description (none in the body), '(confirm API shape)', and the unverified I/O-bound vs CPU-bound sizing advice.
Method: documentation only; no commands were run.
