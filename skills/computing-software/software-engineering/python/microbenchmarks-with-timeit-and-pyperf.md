---
id: computing-software.software-engineering.python.microbenchmarks-with-timeit-and-pyperf
name: microbenchmarks-with-timeit-and-pyperf
category: computing-software
field: software-engineering
product: python
tags: [python, timeit, pyperf, microbenchmarks, pytest-benchmark, python-performance, benchmark-noise]
level: practitioner
status: verified
description: "Measure small Python code paths reliably: timeit CLI and API, min vs mean, setup and globals, pyperf for stable numbers and comparisons, and pytest-benchmark in suites."
sources: ["https://docs.python.org/3/library/timeit.html", "https://pyperf.readthedocs.io/en/latest/", "https://pytest-benchmark.readthedocs.io/en/latest/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Microbenchmarks with timeit and pyperf

**Goal:** settle "which version is faster" with numbers you can trust, not one noisy run.

## timeit CLI
```bash
python -m timeit -s "data = list(range(10_000))" "sum(x*x for x in data)"
python -m timeit -s "data = list(range(10_000))" "sum([x*x for x in data])"
# example output shape: 1000 loops, best of 5: 338 usec per loop (numbers differ per machine; the list version ran faster)
```
`-s` setup runs once and is not timed. timeit auto-picks the loop count and reports the
best of 5 repeats. It disables GC during timing by default (`-s "import gc; gc.enable()"`
to include it).

## timeit API
```python
import timeit
t = timeit.repeat("parse(s)", setup="from mymod import parse; s = load()", repeat=7, number=1000)
print(min(t) / 1000)                 # seconds per call
timeit.timeit(lambda: parse(s), number=1000)    # callables avoid string code
```
Report the **minimum** for "how fast can it go" (noise only adds time); look at spread too.
Jupyter: `%timeit` / `%%timeit`.

## pyperf: stable and comparable
```bash
python -m pyperf timeit -s "import json; d = {'a': list(range(100))}" "json.dumps(d)" -o before.json
# change code / Python version
python -m pyperf timeit ... -o after.json
python -m pyperf compare_to before.json after.json --table
sudo python -m pyperf system tune     # pin CPU frequency, disable turbo (Linux); `system reset` after
```
pyperf spawns multiple worker processes, calibrates, discards warmups, and tells you if the
result is unstable (std dev too high).

## In the test suite
```python
def test_parse_speed(benchmark):
    result = benchmark(parse, SAMPLE)
    assert result.ok
```
`pytest --benchmark-autosave` then `--benchmark-compare --benchmark-compare-fail=mean:10%`
to fail CI on regressions (use dedicated, quiet runners).

## Pitfalls
- Benchmarking with toy inputs: performance characteristics change with size; test realistic N.
- Constant folding / caching: `"a" + "b"` in a timeit string is folded at compile time;
  `lru_cache` makes the second call free.
- Laptop on battery, browser running, thermal throttling: compare only within one session
  or use pyperf's tuning.
- A 5% microbenchmark win in a function using 1% of runtime is irrelevant - profile first.

## Verify
- [ ] Results reported as min/median with repeats and input sizes stated.
- [ ] pyperf `compare_to` says the difference is significant before claiming a win.

## Checked
- Python 3.14.0, pyperf and pytest-benchmark current pip releases: `python -m timeit` output shape confirmed (list comprehension 217 usec vs generator 338 usec here); timeit disables GC (`gc.isenabled()` False inside) unless `gc.enable()` in setup; `timeit.repeat` and callable forms work; `'a'+'b'` timed 4.4 ns (constant folded) vs 24 ns for variables; `pyperf timeit -o` and `compare_to --table` worked; `pyperf system tune` reported no operation for Windows (Linux only); the three `--benchmark-*` flags appear in pytest `--help`. The benchmark fixture test body and CI regression gate were not run end-to-end.
