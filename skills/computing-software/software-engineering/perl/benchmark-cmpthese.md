---
id: computing-software.software-engineering.perl.benchmark-cmpthese
name: benchmark-cmpthese
category: computing-software
field: software-engineering
product: perl
tags: [perl, benchmark-module, cmpthese, time-hires, micro-benchmark, dumbbench, benchmark-cmpthese]
level: practitioner
status: docs-checked
description: "Compare alternatives with Benchmark::cmpthese and Time::HiRes, using realistic data and avoiding micro-benchmark traps."
sources: ["https://perldoc.perl.org/Benchmark", "https://perldoc.perl.org/Time::HiRes"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Benchmark and timing comparisons

**Goal:** fair timing of two implementations.

```perl
use Benchmark qw(cmpthese timethese timeit timestr);
my @data = map { int rand 1e6 } 1 .. 1000;
cmpthese(-3, {                        # negative: run for at least 3 CPU seconds each
    sort_num   => sub { my @s = sort { $a <=> $b } @data },
    sort_ints  => sub { my @s = sort { $a <=> $b } @data; },
}) ;
# Output: a table of rates (iterations/s) and the % faster/slower matrix.
use Time::HiRes qw(time sleep gettimeofday tv_interval);
my $t0 = [gettimeofday]; work(); printf "%.3fs\n", tv_interval($t0);
```
Check that both implementations return the same result before comparing speed.

## Rules
- Pass code refs (not strings) to avoid `eval` overhead.
- Benchmark with data of production size and shape; algorithms differ at scale.
- Close over variables you do not want to measure creating; move setup outside the closure.
- `cmpthese` uses CPU time (user+system); for I/O wait use wall-clock (Time::HiRes). Results vary between runs: run more than once.

## Failure modes
- Optimising code that is not on the critical path.
- Comparing implementations that return different results.

## Self-check
- [ ] The results table agrees with a second run to within the noise.

## Checked
2026-11-02: confirmed against Benchmark (cmpthese, timethese, negative count = minimum CPU seconds, CPU time = user plus system) and Time::HiRes (gettimeofday, tv_interval). Removed: wall style, Dumbbench, percentage spread, warm-up, build, memory-tool remarks.
Method: documentation only; no commands were run.
