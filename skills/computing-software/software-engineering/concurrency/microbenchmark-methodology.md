---
id: computing-software.software-engineering.concurrency.microbenchmark-methodology
name: microbenchmark-methodology
category: computing-software
field: software-engineering
product: concurrency
tags: [concurrency, benchmarking, microbenchmarks, jmh, benchmarkdotnet, criterion, go-benchmarks, dead-code-elimination, warmup, statistical-significance]
level: advanced
status: gated
description: "Write microbenchmarks that measure what you think: harnesses (JMH, BenchmarkDotNet, criterion, go test -bench), warmup, dead-code elimination, noise control and significance."
sources: ["https://github.com/openjdk/jmh", "https://benchmarkdotnet.org/articles/guides/good-practices.html", "https://bheisler.github.io/criterion.rs/book/", "https://pkg.go.dev/golang.org/x/perf/cmd/benchstat", "Systems Performance, 2nd ed. (Gregg), ch12 Benchmarking"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Microbenchmark methodology

**Goal:** numbers you can trust when comparing two implementations, instead of
measuring the JIT, the cache or the noise.

## Use a harness, never a hand-rolled timing loop
| Language | Harness |
|---|---|
| Java/Kotlin | JMH (`@Benchmark`, `@Fork`, `@Warmup`, `Blackhole`) (not run (gated: unconfirmed, source is paywalled or blocked)) |
| .NET | BenchmarkDotNet (`[MemoryDiagnoser]`, multiple jobs/runtimes) (not run (gated: unconfirmed, source is paywalled or blocked)) |
| Rust | criterion / divan |
| Go | `go test -bench=. -benchmem -count=10` + `benchstat` |
| Python | `pyperf` / `pytest-benchmark` (both on PyPI; `pyperf.Runner().bench_func` and `compare_to --table` run) |
| JS | `mitata`, `tinybench` (both on npm) |
Harnesses handle warmup (JIT tiers), iterations, forking (fresh JVM per fork) and
statistics.

## Classic traps
- **Dead-code elimination**: if the result is unused, the optimiser deletes the work (run on Go 1.26: `work(i)` with the result dropped measured 0.14 ns/op and 0 allocs; accumulating into a package-level sink measured 0.37 ns/op, so even a sink can be folded into a tiny loop and needs real inputs).
  Return results / `Blackhole.consume()` / `std::hint::black_box` / assign to a package-level sink (Go).
- **Constant folding**: inputs known at compile time get precomputed; load inputs from
  state fields.
- **Warmup**: first iterations run interpreted/unoptimised; harnesses discard them.
- **Unrealistic data**: benchmarking with 10 elements that fit in L1 when production
  sees 10 million; sorted vs random input changes branch prediction dramatically.
- **Measuring setup**: reset timers (`b.ResetTimer()`, JMH `@Setup` levels).
- **GC and allocation**: report bytes/op; a faster but allocation-heavy version may lose
  under real load.

## Noise control
- Quiet machine: no browser/IDE builds; fixed CPU frequency (disable turbo/power saving
  where possible), pin cores (`taskset`), AC power on laptops.
- Repeat runs (`-count=10`, multiple JMH forks) and compare distributions with
  benchstat (run, prints `~` with p and n when no significant difference) / BenchmarkDotNet's statistical output; report confidence intervals, not a
  single number.
- CI benchmarks on shared runners are noisy: track trends with tolerance thresholds,
  or use instruction counts (iai-callgrind, Cachegrind) for stable signals (iai-callgrind exists on crates.io; Valgrind-based tools not run on Windows (gated: unconfirmed, source is paywalled or blocked)).

## Keep perspective
A 30% win in a function that takes 0.1% of request time is irrelevant: profile the
real workload first, microbenchmark the hotspot second, then confirm with an end-to-end
load test.

## Verify
- [ ] Benchmark consumes its results and uses non-constant inputs.
- [ ] Improvement is statistically significant (benchstat p < 0.05 or non-overlapping CIs).
- [ ] End-to-end metric confirms the gain.
