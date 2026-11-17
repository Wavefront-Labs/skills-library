---
id: computing-software.software-engineering.v-lang.v-time-durations-sleep-stopwatch
name: v-time-durations-sleep-stopwatch
category: computing-software
field: software-engineering
product: v-lang
tags: [v-time-durations-sleep-stopwatch, time-module, duration, sleep, stopwatch, time.second, millisecond, elapsed, benchmark, since, add, v-lang]
level: practitioner
status: docs-checked
description: "Use time.Duration constants, add and subtract durations, sleep, measure elapsed time with StopWatch and schedule with timers."
sources:
  - https://docs.vlang.io/
  - https://modules.vlang.io/
  - https://github.com/vlang/v
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Durations, sleep, tickers and stopwatch

Goal: measure and wait.

- Constants: `time.nanosecond`, `microsecond`, `millisecond`, `second`, `minute`, `hour`, `time.infinite` (Duration).
- Sleep: `time.sleep(250 * time.millisecond)`.
- Arithmetic: `t2 := t.add(2 * time.hour)`, `d := t2 - t1` (Duration), `d.seconds()`, `d.minutes()`, `d.milliseconds()`.
- Stopwatch: `mut sw := time.new_stopwatch(); work(); println(sw.elapsed().milliseconds())` (starts immediately; `auto_start: false` defers); `sw.pause()`, `sw.start()`, `sw.restart()`, `sw.stop()`. Timers: `time.new_ticker(d)` / `time.new_timer(d)` with `stop()`.
- `time.ticks()` returns milliseconds since the UNIX epoch (on Windows, since system start); the stopwatch reads `sys_mono_now()`.
- Timeouts: a `select` block takes an optional duration branch such as `500 * time.millisecond { ... }`; it is mutually exclusive with `else`.

Gotchas:
- `Duration` is an `i64` nanosecond count (`pub type Duration = i64`).
- `time.sleep` suspends the calling thread.

Verify: sleep 100 ms and assert elapsed >= 100 ms.

## Checked

2026-11-03. Confirmed against the V repository source (vlib modules and doc/docs.md) read in this batch: Duration constants and accessors (vlib/time/duration.v), StopWatch API and auto_start (stopwatch.v), time.ticks and sleep docs (time.c.v, time_nix.c.v), Time.add/since/until, Ticker and Timer (ticker.v, timer.v), select timeout branch (doc/docs.md, Select section).
Removed or corrected: `(confirm)` on ticks (it is epoch ms, not 'since start' off Windows), the integer-size multiplication advice, and the 'blocks the process' claim (sleep suspends the calling thread).
Method: documentation only; no commands were run.
