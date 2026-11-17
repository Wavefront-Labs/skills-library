---
id: computing-software.software-engineering.python.free-threaded-python
name: free-threaded-python
category: computing-software
field: software-engineering
product: python
tags: [python, python-concurrency, free-threading, pep-703, nogil, python313t, gil, thread-safety, c-extensions]
level: advanced
status: verified
description: "Evaluate and adopt free-threaded CPython (PEP 703, 3.13t/3.14t): installing it, checking extension support, thread-safety risks and measuring real speedups."
sources: ["https://docs.python.org/3/howto/free-threading-python.html", "https://peps.python.org/pep-0703/", "https://py-free-threading.github.io/", "https://peps.python.org/pep-0779/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Free-threaded Python (PEP 703)

**Goal:** decide whether the no-GIL build helps your CPU-bound threaded code, and adopt
it without data races in code that silently relied on the GIL.

## Status
- 3.13: experimental build `python3.13t`.
- 3.14: officially supported but optional (PEP 779, "phase II"); default builds still
  have the GIL. Single-thread overhead on pyperformance averages about 1% (macOS aarch64) to 8% (x86-64 Linux) per the free-threading HOWTO.

## Getting it
```bash
uv python install 3.14t          # or the official installer's "free-threaded" option
python3.14t -VV                  # shows "free-threading build"
python -c "import sys; print(sys._is_gil_enabled())"
```
Importing a C extension that does not declare free-threading support RE-ENABLES the GIL
at runtime with a warning. Force-disable for testing with `PYTHON_GIL=0` or `-X gil=0`.

## Checking your dependencies
- Extensions must be built for the `t` ABI (wheel tag `cp314t`). Check PyPI wheel files
  or the community tracker at py-free-threading.github.io.
- Pure-Python packages work, but may have races previously masked by the GIL.

## What breaks
- Check-then-act on shared objects (`if k not in d: d[k] = make()`) was already racy
  but rarely bit; now it does. Use `threading.Lock` or `dict.setdefault`.
- Built-in containers are internally locked (no crashes), but compound operations are
  not atomic.
- Iterating a list/dict while another thread mutates it can give inconsistent results.
- Lazy module-level caches/singletons initialised without locks.

## Measuring
Benchmark the same `ThreadPoolExecutor` workload on GIL and `t` builds:
```python
with ThreadPoolExecutor(8) as ex: list(ex.map(cpu_work, chunks))
```
Expect near-linear scaling for pure-Python CPU loops with little shared state; little
gain for I/O-bound or numpy-heavy code (already releases the GIL). Contended shared
objects scale poorly; give each thread its own data and merge.

## Verify
- [ ] `sys._is_gil_enabled()` is False in the deployed process (no extension re-enabled it).
- [ ] Test suite passes under the `t` build, including a thread-stress run (pytest-run-parallel).
- [ ] Measured speedup justifies the build's overhead and packaging cost.

## Checked
- Installed CPython 3.14.8 free-threaded via `uv python install 3.14t` (scratch dir): `-VV` says "free-threading build"; `sys._is_gil_enabled()` False; `PYTHON_GIL=1` turned it True and `-X gil=0` kept False; `Py_GIL_DISABLED` is 1 and ext suffix is `.cp314t-win_amd64.pyd`; 8 pure-Python CPU jobs in a 8-thread pool took 0.14 s vs 0.63 s serial on 12 cores (GIL build 0.55 s vs 0.57 s). Extension GIL re-enable warning, 1-8% overhead and PEP 779 phase II status quoted from the free-threading HOWTO and PEP 779; the extension warning itself was not triggered here.
