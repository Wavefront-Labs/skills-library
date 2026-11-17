---
id: computing-software.software-engineering.python.profiling-and-performance
name: profiling-and-performance
category: computing-software
field: software-engineering
product: python
tags: [python, profiling, cprofile, py-spy, performance, memory-profiler, tracemalloc, line-profiler, gil, flame-graph, scalene, snakeviz, optimization]
level: advanced
status: verified
description: "Find real Python bottlenecks with cProfile/py-spy/scalene and memory leaks with tracemalloc before guessing at optimizations."
sources: ["Python docs - profile and pstats", "py-spy README (benfred/py-spy)", "Scalene paper/README (plasma-umass/scalene)", "personal profiling of production services"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Profiling and performance — measure before you optimise

**Goal:** locate the actual hot path (CPU, memory, or GIL contention) in minutes,
without rewriting code based on intuition.

## 1. Pick the right tool for the question
- **"Where does CPU time go?"** → `python -m cProfile -o out.prof script.py`, then
  `python -m pstats out.prof` or visualise with `snakeviz out.prof` (flame-graph-ish
  call tree). cProfile adds real overhead (about 5% on a loop-heavy test, 6x on call-heavy recursion) and is noisy for tight loops —
  fine for "which function," wrong for microbenchmark numbers.
- **"What's a *running* process doing right now, no restart?"** → `py-spy dump --pid
  <PID>` (one-shot stack sample) or `py-spy record -o out.svg --pid <PID>` (flame
  graph over time; add `--native` for C extension frames). On Windows attach to the real
  interpreter PID, not a venv launcher (the launcher gave "Failed to find python version"). Works without any
  instrumentation — attach to prod if you're desperate, it's sampling-based and low
  overhead.
- **"CPU and memory in one view"** → `scalene run script.py`, then `scalene view --cli`
  (or `scalene view` for the browser UI; scalene 2.x replaced the old `scalene script.py`
  form) — per-line CPU split into Python, native and system time, plus memory and copy
  volume. It has no GIL column. Runs shorter than a second or so are rejected ("did not run
  for long enough to profile").
- **Per-line hotspot inside one function you already suspect** → `line_profiler`:
  `@profile` decorator + `kernprof -lv script.py`.

## 2. Memory: leaks vs legitimate growth
```python
import tracemalloc
tracemalloc.start()
# ... run workload ...
snapshot = tracemalloc.take_snapshot()
for stat in snapshot.statistics('lineno')[:10]:
    print(stat)
```
Take two snapshots across a request/iteration boundary and diff
(`snapshot2.compare_to(snapshot1, 'lineno')`) — steady per-iteration growth is a leak;
a one-time jump at startup usually isn't. Common real leaks: module-level caches with
no eviction, closures capturing large objects, `functools.lru_cache` without
`maxsize`, circular references involving `__del__` (uncollectable before Python 3.4's PEP 442; the 3.14 collector freed them).
For C-extension leaks (numpy, PIL), tracemalloc may not see the native allocation — watch
the OS-level RSS trend or use a native memory profiler instead.

## 3. The GIL is usually the real bottleneck, not "Python is slow"
A CPU-bound function run via `threading` gets zero parallelism (GIL), masquerading as
"the thread didn't help." Diagnose by comparing wall time of
`ThreadPoolExecutor` vs `ProcessPoolExecutor` for the same workload — if threads give
no speedup but processes do, it's GIL contention, not I/O wait. The free-threaded build
(PEP 703; experimental in 3.13, officially supported but optional in 3.14) removes the GIL, but
an extension that does not declare support re-enables it — check `sys._is_gil_enabled()`.

## 4. Before profiling at all
- Reproduce with a representative workload size — profiling a 10-item test case
  hides O(n²) behaviour that only matters at 10,000.
- Check it isn't I/O: add timing around the suspected network/DB call first; profilers under-represent time spent in blocking syscalls.
- `timeit` for isolated snippet comparisons, never for "is this function fast" — it
  measures a tight loop with warmed-up caches, not production conditions.

## Gotchas
- cProfile's `cumulative` vs `tottime`: a wrapper function shows huge cumulative time
  even if it does nothing — check `tottime` for where cycles are actually spent.
- Multiprocessing/async code isn't profiled by default cProfile on the main process
  only; profile inside each worker (`cProfile.runctx` per process) or use py-spy
  which can sample native threads/processes directly.
- Decorators and `functools.wraps` can obscure the real function name in profiler
  output — check `__wrapped__` before concluding the wrong function is hot.

## Verify
- [ ] A flame graph or pstats sorted by `tottime` names the actual hot function(s),
      not just the entry point.
- [ ] Memory growth was measured with two tracemalloc snapshots across repeated
      iterations, not a single reading.
- [ ] If parallelism didn't help, GIL contention vs I/O wait was explicitly ruled in/out.
- [ ] The optimization was re-measured with the same profiler, same workload, after the change.

Related: computing-software.software-engineering.concurrency.profiling-before-optimising,
computing-software.software-engineering.python.asyncio-concurrency-patterns

## Checked
- Python 3.14.0 with cProfile, pstats, py-spy 0.4.2, scalene 2.3.0, line_profiler (current pip releases): `pstats` sort by `tottime` names the hot function; cProfile overhead measured at about 5% (loop-heavy) and 6x (recursive calls); `py-spy dump` and `record -o out.svg` worked on the real interpreter PID and failed on a venv launcher PID; `--native` and `--subprocesses` flags exist; `scalene run` then `scalene view --cli` replaced the bare `scalene script.py` form, short runs are rejected, and its columns are Python/native/system time, memory and copy (no GIL column); `kernprof -lv` with `@profile` printed per-line times; tracemalloc `compare_to` reported growth; an unreferenced `__del__` cycle was collected. Thread-vs-process speedups were shown in the free-threading check (GIL build threads equal serial). `snakeviz` was installed but not opened (browser UI).
