---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.performance-regression
name: performance-regression
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, performance-engineering, performance-regression, ci-performance-tests, k6, change-point-detection]
level: practitioner
status: draft
description: "Detect performance regressions in CI: stable test environments, benchmark suites, thresholds versus statistical comparison, and gating releases."
sources: ["https://grafana.com/docs/k6/latest/using-k6/thresholds/", "https://github.com/benchmark-action/github-action-benchmark", "https://arxiv.org/abs/2003.00584"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Performance regression detection in CI

## Layers
1. **Micro-benchmarks** (JMH, BenchmarkDotNet, Go `testing.B`, pytest-benchmark) on hot code
   paths, per PR.
2. **Service load tests** (k6, Gatling, Locust) against a deployed test environment, nightly
   or per release candidate.
3. **Production canaries** comparing latency and CPU per request between canary and baseline.

## Steps
1. **Stabilise the environment**: dedicated (non-burstable) runners or instances, fixed
   sizes, no co-tenants; run the baseline and candidate on the same machine if possible.
2. **Choose comparison**: fixed thresholds (k6 `thresholds: { http_req_duration: ['p(95)<300'] }`)
   for SLO-style gates; relative comparison against the last N main-branch runs for drift.
3. **Statistics**: repeat runs; compare distributions (Mann-Whitney U) or use change-point
   detection on the time series (MongoDB's approach) to avoid alert fatigue from noise.
4. **Gate**: fail PRs on large confident regressions; warn on small ones; require an
   explicit override label with justification.
5. **Track resource efficiency** too: CPU-seconds and memory per request, which drive cost.
6. **Store history** and plot trends per benchmark.

## Gotchas
- Noisy shared CI runners make results meaningless; variance above the regression you want to detect means the test is useless.
- Tests with tiny data sets miss regressions that appear at scale.

## Verify
- [ ] Run-to-run variance measured and below detection threshold.
- [ ] Regression gate has caught at least one seeded slowdown.
