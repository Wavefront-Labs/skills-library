---
id: computing-software.data-engineering.polars.multiprocessing-spawn-not-fork
name: multiprocessing-spawn-not-fork
category: computing-software
field: data-engineering
product: polars
tags: [polars-multiprocessing, multiprocessing, spawn, fork, deadlock, forkserver, threads, gpu-engine]
level: practitioner
status: docs-checked
description: "Use Python multiprocessing with Polars safely: choose the spawn start method to avoid fork deadlocks, and know when multiprocessing is pointless."
sources:
  - https://docs.pola.rs/user-guide/misc/multiprocessing/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Python multiprocessing with Polars

TLDR: if Python's `multiprocessing` with Polars raises an error about multiprocessing methods, use `spawn`, not `fork`.

```python
from multiprocessing import get_context

def my_fun(s):
    print(s)

with get_context("spawn").Pool() as pool:
    pool.map(my_fun, ["input1", "input2", ...])
```

## When not to use it
Polars already uses all CPU cores: two expressions in a `select` run in parallel, and `group_by().agg(<expr>)` evaluates each group separately. `multiprocessing` is very unlikely to help there. With the GPU engine also avoid manual multiprocessing; they compete for system memory and processing power.

## When to use it
When another, single-threaded library is the bottleneck and the problem is parallelizable.

## Why fork breaks
Polars is multithreaded, so it cannot be combined with `fork`. On Unix (Linux, BSD) `fork` is the default unless overridden. Safely forking a multithreaded process is problematic: the child copies the parent's address space including mutex states. In the guide's example, `pl.read_parquet` holds a file lock, then `os.fork()` copies it in the acquired state, so the children hang forever. `spawn` creates a fresh Python interpreter and inherits no mutex state.

It is tricky to debug because `fork` can appear to work: removing the `pl.read_parquet` call (building the frame with `pl.DataFrame`) makes the forked example run fine. A seemingly unrelated change can break it, so never use `fork` with multithreaded libraries unless unavoidable.

`spawn` is available on all platforms and is the recommended, safest choice; `forkserver` is the other alternative.

## Spawn gotchas
- All arguments must be pickleable.
- `spawn` has more start-up overhead than `fork`, usually negligible for jobs lasting minutes or hours.
- `spawn` requires importable code, so do not put the spawning code in global scope (notebooks, plain scripts). Define functions and run them from `if __name__ == "__main__":`; quick notebook experiments may fail.
- Example uses `multiprocessing.get_context("spawn").Process(target=..., args=(test_df, i))` with `proc.start()` and `proc.join()`.

## Checked
2026-11-07: every claim compared with the cited Polars user guide page(s). No unconfirmed claims found.

Method: documentation only; no commands were run.
