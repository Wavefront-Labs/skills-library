---
id: computing-software.software-engineering.perl.performance-idioms-memory
name: performance-idioms-memory
category: computing-software
field: software-engineering
product: perl
tags: [perl, performance-tuning, performance-idioms-memory]
level: advanced
status: docs-checked
description: "Apply Perl performance idioms from perlperf: baseline first, Benchmark, NYTProf, hashes for lookup, tr, sort keys and compile-time DEBUG constants."
sources: ["https://perldoc.perl.org/perlperf", "https://perldoc.perl.org/perlreftut"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Performance idioms

**Goal:** speed wins that survive measurement. Source: perlperf.

## Process
1. Get the program correct first, with a working test suite, then optimise.
2. Establish a reliable, repeatable baseline with `Benchmark`, `Devel::NYTProf` or the Unix `time` utility.
3. Change one thing at a time under version control, so you can tell which change mattered.
4. Re-run the same benchmark or profile and confirm the task takes less time. Repeat.

## Guidelines from perlperf (no golden bullets)
- Inline code is faster than sub or method calls but is less maintainable and uses more memory.
- Searching a list: storing data in a hash and testing the key can be more efficient than looping with `grep`.
- `substr` can be much faster than a regex but is less flexible; weigh the trade-off.
- A line costing 0.01 s called 100,000 times dominates the run; find those lines with a profiler.
- A sort subroutine is usually slower than the built-in `cmp` and `<=>` ordering. To cut cost, cache sort keys ahead of time (the Orcish Maneuver, whose cache costs a second pass) or `pack` the key into one string and use plain `sort` (the Guttman Rossler Transform; some string combinations make it too complex to pay off).
- With database backends: always use SQL placeholders, consider pre-fetching, and note that the DBIx namespace tries to delay querying until the last moment.
- Splitting one large file across processes (POE, threads, fork) can use more CPU but brings concurrency issues.

## Benchmarks and profilers
- `Benchmark` with `timethese(N, { name => sub {...} })`: run enough iterations that results settle on an average. Direct multi-level access like `$ref->{ref}->{x}` measured slightly faster than a local dereference in perlperf's example, but the gain is tiny, so choose readability unless a profile says otherwise.
- `tr/aeiou/xxxxx/` can beat `s/[aeiou]/x/g` for simple character replacement; the regex is more flexible. Assign through a global in test code so perl cannot optimise the work away.
- NYTProf: `perl -d:NYTProf script`, writes `nytprof.out` by default; `nytprofhtml` and `nytprofcsv` produce reports. `Devel::NYTProf::Apache` hooks it into mod_perl. perlperf also lists Devel::DProf, Devel::Profiler, Devel::SmallProf and Devel::FastProf.
- Debug logging: `use constant DEBUG => 0;` and `if (DEBUG) {...}` is optimised away at compile time; `perl -MO=Deparse` shows the removed code.

## Self-check
- [ ] A before/after benchmark on production-sized input shows the claimed speedup.
- [ ] Only the hot spots found by the profiler were changed.

## Checked
2026-11-09. Read in full: perlperf lines 1-110 (overview, general guidelines, dereference and tr benchmarks) plus its profiling-tool, NYTProf and DEBUG constant sections by search. Confirmed everything above. Removed as not stated in perlperf or perlreftut: precompiled `qr//` advice, `join` versus `.=`, `List::Util` speed claims, `sysread` buffers, `make_immutable`, lazy `require`, memory-size figures, `pack`/`vec`/Sereal/PDL, `weaken`, Devel::Cycle, Test::LeakTrace, Devel::Size, Devel::MAT and `/usr/bin/time -v`.
Method: documentation only; no commands were run.
