---
id: computing-software.qa-testing-engineering.performance-testing.performance-regression-gates-ci
name: performance-regression-gates-ci
category: computing-software
field: qa-testing-engineering
product: performance-testing
tags: [perf-regression-gate, performance-gates, ci-performance-testing, baseline-comparison-ci]
level: practitioner
status: docs-checked
description: "Gate CI on performance regressions: short repeatable load tests per build, thresholds plus baseline comparison, noise control, and failing the pipeline with useful output."
sources:
  - https://grafana.com/docs/k6/latest/using-k6/thresholds/
  - https://grafana.com/docs/k6/latest/testing-guides/automated-performance-testing/
  - https://bencher.dev/docs/explanation/thresholds/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Automated performance regression gates in CI

## Tiers
| Pipeline | Test | Gate |
|---|---|---|
| Every PR | short smoke/load at fixed low rate on an ephemeral env | absolute thresholds (p95, error rate) |
| Nightly | average-load on a stable perf env | thresholds + comparison to rolling baseline |
| Pre-release | full suite (load, stress, soak) | review by a human |

## Absolute thresholds (k6 fails the run on breach)
```js
thresholds: {
  http_req_failed: ['rate<0.01'],
  'http_req_duration{name:GET /products}': [{ threshold: 'p(95)<250', abortOnFail: true, delayAbortEval: '1m' }],
  checks: ['rate>0.99'],
},
```
CI step fails on non-zero exit.

## Baseline comparison
Store per-run summaries (p50/p95/p99/throughput per endpoint) as artifacts or in a time-series store (Bencher, InfluxDB, a simple JSON history). Fail when p95 is worse than the baseline median of the last N runs by more than a tolerance **and** beyond normal run-to-run noise.

Export the end-of-test summary (see the k6 end-of-test docs) and compare it with your stored history in your own script.

## Noise control
- Same environment size, same data snapshot, isolated generators, pinned versions.
- Run 2-3 repetitions for nightly gates and compare medians.
- Warm up before measuring; exclude warm-up from thresholds.

## Useful output
On failure, print the metric, baseline, delta and a link to the dashboard/report; upload the HTML report as an artifact.

## Gotchas
- Shared CI runners have noisy neighbours: PR-level gates must use generous thresholds or dedicated runners.
- Thresholds that never fail get ignored; ones that fail randomly get disabled. Calibrate from historical variance.

## Verify
Inject a deliberate 200 ms delay in one endpoint on a branch: the pipeline fails with the endpoint named in the output.

## Checked
2026-10-28. Confirmed in the k6 thresholds and automated-testing pages: `abortOnFail`, `delayAbortEval`, threshold syntax on tagged metrics, failing CI on threshold breach; Bencher thresholds page for baseline comparison. Removed: the exit-code figure, `--summary-export` and the invented compare script flags, Taurus `passfail` and `statistics.json` (not in the pages), the 10% and 3 MAD figures and test durations.
Method: documentation only; no commands were run.
