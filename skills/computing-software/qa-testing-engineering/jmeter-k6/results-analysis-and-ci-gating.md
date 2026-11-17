---
id: computing-software.qa-testing-engineering.jmeter-k6.results-analysis-and-ci-gating
name: results-analysis-and-ci-gating
category: computing-software
field: qa-testing-engineering
product: jmeter-k6
tags: [jmeter, k6, results-analysis, aggregate-report, percentiles, p95, p99, html-dashboard, k6-thresholds, ci-gating, performance-regression, grafana, influxdb, backend-listener, coordinated-omission, error-rate, response-time-distribution]
level: advanced
status: docs-checked
description: "Read JMeter/k6 results correctly (percentiles over averages, coordinated omission), and gate CI on performance thresholds without flaking on unrelated infrastructure noise."
sources:
  - https://grafana.com/docs/k6/latest/using-k6/scenarios/concepts/open-vs-closed/
  - https://grafana.com/docs/k6/latest/using-k6/thresholds/
  - https://grafana.com/docs/k6/latest/results-output/real-time/influxdb/
  - https://jmeter.apache.org/usermanual/generating-dashboard.html
  - https://jmeter.apache.org/usermanual/component_reference.html#Backend_Listener
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Reading load-test results and gating CI on them

**Goal:** turn raw JMeter/k6 output into a correct pass/fail decision — not one
skewed by averages, missed timeouts, or a threshold so loose it never catches a
regression.

## 1. Never report the average
Response time distributions are long-tailed: a handful of slow requests (GC pause,
cold cache, lock contention) pull the mean up a little but say nothing about what
most users experience. Report **percentiles**: p50 (typical), p95 and p99 (the
experience of the unlucky tail, which is often the one users complain about).
JMeter's Aggregate Report shows 90%, 95% and 99% lines per sampler; k6 exposes percentiles such as `p(95)` to `thresholds` and prints them in the end-of-test summary.

## 2. Coordinated omission — the metric that lies by default
Both tools' default "closed model" (fixed number of threads/VUs, each waiting for
a response before sending the next request) ties throughput to response time (the k6 docs call this problem coordinated omission): when the system under test slows,
the arrival rate of new iterations tapers off, so a stall produces fewer slow samples than it would with real arrivals. Fix: use an
**open/arrival-rate model** that issues requests on a schedule regardless of
whether earlier ones finished — k6's arrival-rate executors (`constant-arrival-rate`,
`ramping-arrival-rate`) do this natively; in JMeter use the Open Model Thread Group (core, experimental), the plugin Arrivals Thread Group, or a Concurrency Thread Group with a Throughput Shaping Timer, or the Precise Throughput Timer for pacing.

## 3. Interpreting the error rate alongside latency
A rising error rate *and* rising latency together usually means saturation
(connection pool, thread pool, or OS file-descriptor exhaustion) — latency alone
without errors can mean the system is slow but stable; errors without a latency
rise often mean a hard limit (rate limiter, quota) was hit cleanly. Break errors
down by status code/exception type, not just a single "error %" — a load test
whose errors are all `429 Too Many Requests` from a test-environment rate limiter
is a configuration problem, not a capacity finding.

## 4. Dashboards without a time-series backend
`jmeter -n -t plan.jmx -l results.jtl -e -o report/` generates a static HTML
dashboard from the JTL log — enough for a one-off run. For trend-over-time
(is p95 drifting release to release?), stream to a time-series store and graph in
Grafana: JMeter via the Backend Listener (Graphite by default, plus an InfluxDB implementation), k6 via `k6 run --out influxdb=<url>`, `--out experimental-prometheus-rw`, or `k6 cloud run --local-execution` for Grafana Cloud k6. Without a time series, every run is judged in isolation
and slow regressions creep in unnoticed.

## 5. Gating CI correctly
Set the gate **in the tool**, not by eyeballing a report after the fact — k6
`thresholds` fail the test when violated (exit code 99):
```js
export const options = { thresholds: { http_req_duration: ['p(95)<800'], http_req_failed: ['rate<0.01'] } }
```
Run load tests against a dedicated, consistently sized environment: a shared, noisy staging environment makes thresholds flap for reasons unrelated to the code under test. Cold caches and JIT skew the start of every run, so warm up and exclude the ramp from the evaluated window (JMeter dashboard `start_date`/`end_date`; in k6, scope thresholds with tags or abort conditions such as `delayAbortEval`).

## Verify
- [ ] Report leads with p95/p99, not just average or median.
- [ ] Test uses an open/arrival-rate model if tail latency under load is the question.
- [ ] Errors broken down by status/type, cross-checked against latency trend.
- [ ] CI gate is a tool-native threshold (k6 exit code 99 on failure), not manual report review.
- [ ] Gate runs against a dedicated environment with the warm-up excluded from the evaluated window.

## Checked
Checked against the Grafana k6 docs sources (grafana/k6-docs, docs/sources/k6/next, last commit 2026-10-13, which document k6 v2) and the k6 Operator repository (grafana/k6-operator, last commit 2026-10-21). Also Apache JMeter user manual sources (apache/jmeter, xdocs/usermanual, master as of 2026-10-01). Confirmed: coordinated omission described in the k6 open-versus-closed model docs, arrival-rate executor names, threshold failure and exit code 99, `p(95)` threshold syntax, JMeter Aggregate Report 90/95/99% lines, Backend Listener Graphite and InfluxDB implementations, `k6 run --out influxdb=<url>` and Prometheus remote write output names, `k6 cloud run --local-execution`, dashboard `start_date`/`end_date`, Open Model Thread Group. Removed the unconfirmed warm-up duration and the external video source.

Method: documentation only; no commands were run.
