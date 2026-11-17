---
id: computing-software.software-engineering.concurrency.performance-regression-testing-in-ci
name: performance-regression-testing-in-ci
category: computing-software
field: software-engineering
product: concurrency
tags: [performance, performance-regression-testing, continuous-benchmarking, ci, github-action-benchmark, bencher]
level: advanced
status: draft
description: "Catch performance regressions in CI: stable benchmark runners, baselines per branch, statistical thresholds, alerting on PRs, and avoiding flaky perf gates."
sources: ["https://bencher.dev/docs/", "https://github.com/benchmark-action/github-action-benchmark", "https://codspeed.io/docs", "https://pyperf.readthedocs.io/en/latest/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Performance regression testing in CI

## What to run
- A small, stable set of **microbenchmarks** for hot paths (JMH, criterion, BenchmarkDotNet, Go
  `testing.B`, pytest-benchmark/pyperf, Vitest bench).
- A few **macro benchmarks** (end-to-end request throughput, startup time, memory peak, bundle size)
  that reflect user-visible performance.
- Deterministic metrics where possible: instruction counts (Cachegrind/`iai-callgrind`, CodSpeed's
  simulation mode), allocation counts, bundle bytes. These have near-zero noise on shared runners.

## Runner stability
Shared CI runners vary 10-20% run to run: wall-clock gates there are flaky. Options: dedicated
bare-metal runners with tuned environments, instruction-count based measurement, or relative
comparison of base and PR **in the same job** on the same machine (interleaved).

## Baselines and thresholds
- Track history per benchmark on `main` (Bencher, github-action-benchmark storing to gh-pages,
  CodSpeed, Conbench). Compare PR results to the recent main baseline.
- Thresholds: statistical (t-test/percentile bands over the last N main runs; Bencher thresholds)
  rather than a fixed 5%. Require significance and a minimum effect size.
- Allocation and size budgets as hard limits (`size-limit` for JS bundles, `max allocations` asserts).

## Workflow
1. PR runs benchmarks, posts a comparison comment (table with change and confidence).
2. Significant regressions fail the check or require an explicit "perf-regression-accepted" label
   with justification.
3. Main runs nightly/per merge to keep history; alerts on regressions that slipped in (bisect with
   the history).
```yaml
- uses: benchmark-action/github-action-benchmark@v1
  with: {tool: 'cargo', output-file-path: output.txt, alert-threshold: '150%',
         comment-on-alert: true, fail-on-alert: true, github-token: ${{ secrets.GITHUB_TOKEN }}}
```

## Keep it trustworthy
Rerun-on-failure masks problems; investigate flaky benchmarks and remove or fix them. Review
benchmark code like production code (dead-code elimination, constant folding produce fake wins).
