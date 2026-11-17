---
id: computing-software.software-engineering.prolog.profile-statistics
name: profile-statistics
category: computing-software
field: software-engineering
product: prolog
tags: [prolog, profile-statistics, time-1]
level: practitioner
status: docs-checked
description: "Measure SWI-Prolog programs with time/1, statistics/2, profile/1,2 and call_with_time_limit/2."
sources:
  - https://www.swi-prolog.org/pldoc/man?predicate=time/1
  - https://www.swi-prolog.org/pldoc/man?predicate=call_with_time_limit/2
  - https://www.swi-prolog.org/pldoc/man?predicate=garbage_collect/0
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Measuring
```prolog
?- time(fib(25, F)).                         % inferences, CPU time, LIPS
?- statistics(cputime, T).
?- profile(run_benchmark).                   % GUI if XPCE is loaded, else a text report
?- profile(run_benchmark, [top(20)]).
:- use_module(library(time)).
?- catch(call_with_time_limit(2, loop), time_limit_exceeded, writeln(timeout)).
?- call_time(run_benchmark, Dict).           % dict with cpu, wall, inferences
```
- `time/1` prints inferences, CPU time and LIPS for the user; use `call_time/2,3` when a program needs the numbers.
- Compare algorithms by inference counts rather than wall time.
- `statistics(Key, Value)` keys include `cputime` (user CPU seconds), `inferences`, `localused`, `globalused`, `trailused`.
- `profile(Goal, Options)`: `time(Which)` (cpu or wall), `sample_rate(Rate)`, `ports(Bool)`, `top(N)`, `cumulative(Bool)`, `exact(Exact)`.
- `call_with_time_limit/2` limits wall time, calls Goal like `once/1` and raises `time_limit_exceeded`.
- `garbage_collect/0` and `prolog_stack_property/2` for stack inspection.
## Gotchas
- `profile/1` runs `once(Goal)`.
- Repeat measurements; one run is a noisy sample.
## Self-check
Compare naive and accumulator `reverse` with `time/1` on 100,000 elements.

## Checked

2026-11-03. SWI-Prolog manual: profile/1,2 options (execution profiling section), time/1 page (LIPS output, call_time/2,3), statistics/2 key table, call_with_time_limit/2 page (library(time), time_limit_exceeded, once semantics), garbage_collect/0 and prolog_stack_property/2 pages. Removed: "first call includes autoload and compile time", "profile slows execution", `statistics/0` description (not read) and the "verify options" hedge.

Method: documentation only; no commands were run.
