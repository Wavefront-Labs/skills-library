---
id: computing-software.qa-testing-engineering.performance-testing.cpu-profiling-during-tests
name: cpu-profiling-during-tests
category: computing-software
field: qa-testing-engineering
product: performance-testing
tags: [profiling-in-tests, dynamic-analysis, py-spy, async-profiler, flame-graphs]
level: practitioner
status: docs-checked
description: "Profile CPU during test runs to find hot spots and slow tests: py-spy and cProfile for Python, async-profiler and JFR for JVM, and reading flame graphs."
sources:
  - https://github.com/benfred/py-spy
  - https://github.com/async-profiler/async-profiler
  - https://docs.python.org/3/library/profile.html
  - https://www.brendangregg.com/flamegraphs.html
  - https://github.com/async-profiler/async-profiler/blob/master/docs/ProfilingModes.md
  - https://docs.oracle.com/en/java/javase/21/troubleshoot/troubleshooting-memory-leaks.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CPU profiling during tests

**Goal:** dynamic analysis of where CPU time goes, during unit, integration or load tests, to find performance defects and slow tests.

## Find slow tests first
`pytest --durations=20` and the per-test timings in JUnit/Surefire XML. Profile the slowest.

## Python
```bash
py-spy record -o profile.svg --subprocesses -- python -m pytest tests/test_reports.py
py-spy top --pid 12345          # live view of a running server under load
py-spy dump --pid 12345         # one-off stack dump of all threads (hangs, deadlocks)
python -m cProfile -o out.prof -m pytest tests/test_reports.py
python -m pstats out.prof       # then: sort cumtime, stats 20   (or snakeviz out.prof)
```
py-spy is a sampling profiler that reads another process's memory, so attaching to an existing PID usually needs root on Linux (`sudo`) and `--cap-add SYS_PTRACE` in Docker; starting the program under py-spy (as above) avoids the root requirement on Linux. `--native` includes C/C++/Cython extension frames. `--format` also writes speedscope or raw data.

## JVM
```bash
asprof -d 30 -e cpu -f flame.html <pid>
asprof -d 30 -e alloc -f alloc.html <pid>             # allocation profiling
java -XX:StartFlightRecording=duration=60s,filename=rec.jfr,settings=profile -jar app.jar   # JFR, open in JDK Mission Control
```
Attach during a load test to see hot methods under realistic concurrency; `-e wall` samples all threads equally, so it shows blocked time too; `-e lock` profiles lock contention.

## Reading flame graphs
- Width = share of samples; look for wide plateaus near the top (the functions actually burning CPU).
- Wide towers of framework frames with a thin top often mean many small calls (N+1 queries, logging, serialization).
- Compare before/after (differential flame graphs) to confirm a fix.

## Gotchas
- Profiling with coverage or debuggers enabled distorts results; profile a clean run.
- JIT warm-up: discard the first part of JVM runs.
- Sampling misses very short functions; aggregate over long enough runs under load.

## Verify
A flame graph is attached to the performance defect, and a re-profile after the fix shows the hot frame reduced.

## Checked
2026-10-31. Confirmed on the py-spy README (record, top and dump with `--pid`, `--native`, root and `SYS_PTRACE` requirements), the async-profiler docs (`asprof -d 30 -f flamegraph.html <PID>`, `-e wall`, `-e lock`, `-e cpu,alloc`), the Oracle Java 21 page (`-XX:StartFlightRecording=...filename=...,settings=profile`, JDK Mission Control) and Brendan Gregg's flame graph page (differential flame graphs). Run here: `py-spy record --help` (0.4.2) lists `-o/--output`, `-s/--subprocesses` and `-n/--native`; `python -m cProfile -o out.prof -m pytest` works, and the `python -m pstats` browser accepts `sort cumtime` and `stats N`; `pytest --help` lists `--durations`. Removed: the async-profiler 3.x and `profiler.sh` remarks, the `/tmp` output paths, Jest `--verbose`, and the 30 s minimum.
Method: documentation plus local `--help` runs and a short cProfile/pstats run; profilers were not attached to a test suite.
