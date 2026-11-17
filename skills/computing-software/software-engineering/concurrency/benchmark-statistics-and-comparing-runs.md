---
id: computing-software.software-engineering.concurrency.benchmark-statistics-and-comparing-runs
name: benchmark-statistics-and-comparing-runs
category: computing-software
field: software-engineering
product: concurrency
tags: [performance, benchmark-statistics, benchstat, confidence-intervals, variance, hyperfine]
level: advanced
status: gated
description: "Compare benchmark runs statistically: multiple samples, medians and confidence intervals, significance tests with benchstat or criterion, and avoiding false wins from noise."
sources: ["https://pkg.go.dev/golang.org/x/perf/cmd/benchstat", "https://bheisler.github.io/criterion.rs/book/analysis.html", "https://github.com/sharkdp/hyperfine", "https://pyperf.readthedocs.io/en/latest/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Benchmark statistics and comparing runs

One run of each version proves nothing: noise between runs is often 2-10%, larger than the change
you're measuring.

## Collect enough samples
- Run each benchmark many times (10-30 samples; run with `-count=10`: identical 200 us sleeps gave `~ (p=0.796 n=10)`, a 260 us variant `+4.55% (p=0.011 n=10)`, Windows timer granularity swamps the nominal 30%), interleaving A and B when possible so drift
  (thermal, background load) affects both equally.
- Warm up first (JIT, caches, page faults); discard warm-up iterations.
- Record the environment (CPU, governor, commit, flags) with the results.

## Summarise robustly
- Report **median** and spread (IQR or min/max), or mean with a **confidence interval**. Latency-
  like data is skewed; means are pulled by outliers.
- Look at the distribution (histogram) for bimodality (e.g. GC in some runs, frequency changes).
- Relative change with uncertainty: "-7.2% +/- 1.1% (p=0.002, n=20)".

## Significance tools
```
go test -bench=. -count=20 > old.txt   # then new.txt
benchstat old.txt new.txt              # median and 95% CI per benchmark; Mann-Whitney U test for A/B; '~' means no significant difference
hyperfine --warmup 3 --runs 30 './old input' './new input' --export-json r.json
python -m pyperf compare_to old.json new.json --table
```
- Rust criterion: bootstraps confidence intervals and reports "Performance has regressed/improved"
  or "No change in performance detected" against a saved baseline (`cargo bench -- --save-baseline <name>`, `-- --baseline <name>`; `--save-baseline` overwrites, `--baseline` does not).
- pyperf `compare_to --table` hides benchmarks whose difference is not significant (run: two identical `time.sleep` runs printed "Benchmark hidden because not significant"); `--min-speed` filters small changes.
- JMH: reports score +/- error (99.9% CI) per benchmark; use multiple forks (`-f 3`) (gated: unconfirmed, source is paywalled or blocked).
- BenchmarkDotNet: mean, error, stddev, median, and statistical tests between jobs (gated: unconfirmed, source is paywalled or blocked).

## Interpreting
- Non-overlapping CIs or p < 0.05 with a meaningful effect size; a statistically significant 0.3%
  change may not matter.
- Many benchmarks compared at once: expect ~1 in 20 false positives at p<0.05; re-run suspicious ones.
- If variance is huge, fix the environment before drawing conclusions (CPU scaling, noisy
  neighbours, turbo).
- Microbenchmark wins must be confirmed with an end-to-end measurement.
