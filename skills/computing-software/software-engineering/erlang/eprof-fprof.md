---
id: computing-software.software-engineering.erlang.eprof-fprof
name: eprof-fprof
category: computing-software
field: software-engineering
product: erlang
tags: [erlang, erl-profiling, eprof-fprof]
level: advanced
status: draft
description: "Erlang eprof and fprof profilers: time per function, call counts, fprof trace overhead and analysis files."
sources:
  - https://www.erlang.org/doc/apps/tools/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# eprof and fprof
**Goal:** find time-consuming functions.

```erlang
eprof:start(),
eprof:profile(fun() -> work() end),
eprof:analyze(total),              % table by time
eprof:stop().
fprof:apply(fun work/0, []),
fprof:profile(),
fprof:analyse([{dest, "fprof.analysis"}, {totals, true}]).
```
- eprof reports time per function and call counts with moderate overhead; fprof gives call trees and callers with much higher overhead.
- Profile with representative load, a small scope, and a fixed number of iterations.
- Use `cprof` for call counts only (low overhead).

## Gotchas
- Profilers perturb timings; use them to find shapes, not microseconds.

## Self-check
Profile a naive and an optimised implementation and compare totals.
