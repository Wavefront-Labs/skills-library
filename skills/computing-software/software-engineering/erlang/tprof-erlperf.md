---
id: computing-software.software-engineering.erlang.tprof-erlperf
name: tprof-erlperf
category: computing-software
field: software-engineering
product: erlang
tags: [erlang, erl-profiling, tprof-erlperf]
level: advanced
status: draft
description: "Erlang tprof (OTP 27) call count, time and memory profiling and erlperf micro-benchmarks."
sources:
  - https://www.erlang.org/doc/apps/tools/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# tprof and erlperf benchmarking
**Goal:** measure and compare implementations.

```erlang
tprof:profile(fun() -> work() end, #{type => call_time}).     % OTP 27; also call_count, call_memory
timer:tc(fun() -> work() end).
```
```
erlperf 'lists:sum(lists:seq(1,100)).' 'lists:foldl(fun(X,A)->X+A end,0,lists:seq(1,100)).'
```
- `tprof` (OTP 27+) unifies call count, call time and call memory profiling.
- `erlperf` (third-party) runs code concurrently for a time window and reports iterations per second; in the shell `erlperf:run(#{runner => fun() -> work() end})` (option shape unconfirmed).
- Benchmark in a release-like build (no `debug_info` penalty on hot paths, JIT on), warm up, and repeat.

## Gotchas
- One-shot `timer:tc` numbers are noisy; run many iterations.

## Self-check
Benchmark two list-sum implementations and check the ranking is stable across runs.
