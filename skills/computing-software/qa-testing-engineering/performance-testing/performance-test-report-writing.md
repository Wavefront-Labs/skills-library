---
id: computing-software.qa-testing-engineering.performance-testing.performance-test-report-writing
name: performance-test-report-writing
category: computing-software
field: qa-testing-engineering
product: performance-testing
tags: [performance-test-report, results-reporting, executive-summary, performance-recommendations]
level: practitioner
status: draft
description: "Write a performance test report stakeholders act on: executive summary against SLOs, test conditions, results by scenario, bottlenecks with evidence, risks and recommendations."
sources:
  - https://www.istqb.org/certifications/performance-tester
  - https://sre.google/workbook/implementing-slos/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Writing the performance test report and recommendations

## Structure
1. **Executive summary (half a page)**: verdict per objective (pass/fail/at risk), headline numbers, top 3 risks, go/no-go recommendation.
2. **Objectives and acceptance criteria**: SLOs and targets with their sources (forecast, contract).
3. **Test conditions**: build/version, environment and its differences from production (sizes, data volume, stubs), workload model (mix, rates, open/closed), test types run, dates, generator setup.
4. **Results by scenario**: table of throughput, p50/p95/p99, error rate per key transaction vs target; time-series charts of load, latency, errors with resource utilisation aligned on the same time axis.
5. **Analysis**: bottlenecks found, with evidence (traces, GC logs, DB stats), knee/capacity figures, anomalies and their explanation.
6. **Risks and limitations**: what wasn't tested, environment caveats, confidence level.
7. **Recommendations**: prioritised actions with expected impact and owners; retest plan.
8. **Appendix**: scripts version, raw data location, configuration.

## Example executive summary
> Checkout meets its p95 < 800 ms objective at forecast peak (650 req/s): p95 610 ms, errors 0.08%. Search does **not**: p95 1.4 s above 400 req/s due to an unindexed sort on `products.updated_at` (evidence: pg_stat_statements, trace sample). Recommend: add composite index (expected p95 < 300 ms), retest search before release. Soak (8 h) showed no memory growth.

## Writing rules
- Lead with decisions, not methodology.
- Compare against targets, not just numbers in isolation.
- Every claim about a cause links to evidence.
- Percentiles, not averages; state sample sizes and steady-state windows.
- Consistent units (ms, req/s) and time zones.

## Gotchas
- Results from an environment 4x smaller than production need explicit scaling assumptions, or don't extrapolate.
- Omitting failed or aborted runs hides instability; include them with reasons.

## Verify
A reader who skips everything but the summary can state whether to release and what must be fixed.
