---
id: computing-software.software-engineering.perl.devel-nytprof-profiling
name: devel-nytprof-profiling
category: computing-software
field: software-engineering
product: perl
tags: [perl, devel-nytprof, nytprofhtml, profiling, flame-graph, hot-spots, devel-nytprof-profiling, perl-profiling-performance]
level: advanced
status: draft
description: "Find hot spots with Devel::NYTProf: run, generate HTML reports, read statement and sub timings, and profile web apps."
sources: ["https://metacpan.org/pod/Devel::NYTProf", "https://perldoc.perl.org/perlperf"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Profiling with Devel::NYTProf

**Goal:** measure before optimising.

```bash
cpanm Devel::NYTProf
perl -d:NYTProf script.pl args                  # writes ./nytprof.out
nytprofhtml --open                              # HTML report in ./nytprof/index.html
nytprofcsv ; nytprofmerge a.out b.out           # CSV export / merge several runs
NYTPROF=start=begin:addpid=1:file=/tmp/nytprof.out perl -d:NYTProf script.pl   # options via env
NYTPROF=sigexit=int:blocks=1 ...                # also write on SIGINT; block-level timing
perl -MDevel::NYTProf -e '...' ; DB::enable_profile(); ...; DB::disable_profile(); DB::finish_profile()   # profile a region
plackup -MDevel::NYTProf app.psgi               # or use Devel::NYTProf::Apache, Plack middleware NYTProf
```

## Reading the report
- Start with "Top 15 Subroutines" by exclusive time (time inside the sub excluding children); inclusive time shows total cost.
- Drill into the per-file HTML to see times per line and per statement; check the "calls" count (a cheap sub called a million times).
- Report links include per-sub callers; spot slow I/O, regex, DB or string concatenation.
- Compare runs before and after a change with the same input.

## Rules
- Profiling overhead is substantial (several times slower); use representative data and report ratios, not absolute times.
- Use `Benchmark` to compare small alternatives, NYTProf to find where time goes.
- Statement-level timing includes time spent in the operating system; use `blocks=1` or `trace` options carefully.
- Long-lived servers: enable/disable profiling per request, or start with `start=no`.
- Alternatives: `Devel::DProf` (obsolete), `Devel::SmallProf` (line-level, slower), `Devel::Size`, `Devel::MAT` for memory, `perf`/`strace`/DTrace for system-level views.
- Optimise algorithms and I/O first; micro-optimising Perl syntax rarely matters.

## Self-check
- [ ] `nytprofhtml` lists the known slow sub at the top of the exclusive-time table.
