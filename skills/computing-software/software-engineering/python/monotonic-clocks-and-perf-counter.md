---
id: computing-software.software-engineering.python.monotonic-clocks-and-perf-counter
name: monotonic-clocks-and-perf-counter
category: computing-software
field: software-engineering
product: python
tags: [python, py-time, time-monotonic-perf-counter, monotonic, perf-counter, time-ns, wall-clock, deadlines, sleep]
level: practitioner
status: docs-checked
description: "Pick the right clock: time.monotonic for timeouts, perf_counter for benchmarks, time.time for timestamps, process_time for CPU; plus sleep accuracy and clock-jump hazards."
sources: ["https://docs.python.org/3/library/time.html#clock-id-constants", "https://docs.python.org/3/library/time.html#time.monotonic"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Monotonic clocks and perf_counter

| Need | Use | Why |
|---|---|---|
| timestamp for logs/records | `time.time()` / `datetime.now(timezone.utc)` | wall clock, can return a lower value if the system clock is set back |
| timeouts, deadlines, intervals | `time.monotonic()` | cannot go backwards, unaffected by system clock updates; reference point undefined |
| benchmarking short code | `time.perf_counter()` | highest available resolution; includes sleep time |
| CPU time of this process | `time.process_time()` | excludes sleep |
| integer nanoseconds (no float precision loss) | `time.time_ns()`, `monotonic_ns()`, `perf_counter_ns()` | the `_ns` functions (3.7) avoid the precision loss of `float` |

```python
import time
deadline = time.monotonic() + 30
while time.monotonic() < deadline:
    if try_once(): break
    time.sleep(0.5)

t0 = time.perf_counter()
work()
elapsed = time.perf_counter() - t0
print(f"{elapsed*1e3:.2f} ms")

time.get_clock_info("monotonic")      # implementation, resolution, adjustable
```
The asyncio event loop uses a monotonic clock, exposed as `loop.time()`.

## Gotchas
- Never compute durations as `time.time() - start`: a clock step makes negative or huge durations.
- Monotonic values are only meaningful as differences within one process; do not store or send them between machines/boots.
- `time.sleep(n)` sleeps *at least* n seconds even if a signal interrupts it (3.5, PEP 475), unless the handler raises; it may take arbitrarily longer because of scheduling.
- `perf_counter` includes sleep time and is the same clock for all processes; use `process_time` for CPU accounting (it excludes sleep).
- Mock time in tests via an injectable `clock` callable rather than sleeping.

## Verify
- [ ] Grep for `time.time()` used in subtraction or timeout loops and replace with `monotonic()`.
- [ ] A unit test injects a fake clock and asserts timeout behaviour without sleeping.

## Checked

- 2026-11-03: checked against the CPython docs `library/time.rst` and `library/asyncio-eventloop.rst`: `time`, `monotonic`, `perf_counter`, `process_time`, the `_ns` variants (3.7), `get_clock_info` names, `sleep` semantics (3.5), `loop.time()`.
- Removed: the 104-day figure, Linux/Windows sleep resolution figures, internals of `threading` and `queue` timeouts, `timeit`, freezegun/time-machine.

Method: documentation only; no commands were run.
