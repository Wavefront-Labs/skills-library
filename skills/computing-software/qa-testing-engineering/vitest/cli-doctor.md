---
id: computing-software.qa-testing-engineering.vitest.cli-doctor
name: cli-doctor
category: computing-software
field: qa-testing-engineering
product: vitest
tags: [vitest-doctor, pool-benchmark, isolate-false-check, happy-dom-swap]
level: advanced
status: docs-checked
description: "Use vitest doctor to time your suite under alternative pool, isolate, environment and maxWorkers settings and read its recommendation and caveats."
sources:
  - https://raw.githubusercontent.com/vitest-dev/vitest/main/docs/guide/cli.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`vitest doctor` runs the full suite under candidate configurations picked from your current config and reports timings, taking the best of several runs for short suites. It needs a passing baseline; if the suite fails, doctor aborts and shows the errors.

```
baseline (pool: forks · isolate: true)  4.08s
pool: 'vmThreads'                       1.33s (-67%)
Recommendation: pool: 'vmThreads' (-67%)
```

Details from the docs:
- `isolate: false` is validated by running twice with shuffled file order; a test that depends on isolation makes the candidate fail.
- Close results prefer the candidate that keeps per-file isolation.
- It probes lower `maxWorkers` by halving while the suite is at least 5% faster, because every worker funnels transforms through one main-thread Vite server.
- DOM or custom-environment suites are measured under `vmThreads` and `vmForks`.
- `jsdom` projects are also tried as `happy-dom` when installed; verify layout or navigation tests before adopting it.
- Browser projects are included in measurements.

Doctor takes a multiple of one normal run's time.

## Checked

2026-11-04. Confirmed against guide/cli.md, section vitest doctor: baseline requirement, best-of-runs for short suites, isolate false validation by shuffled double run, isolation preference on close results, maxWorkers halving with the 5% threshold, vm pools for DOM or custom environments, jsdom to happy-dom swap, browser projects.

Method: documentation only; no commands were run.
