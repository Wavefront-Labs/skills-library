---
id: computing-software.qa-testing-engineering.jmeter-k6.k6-prometheus-grafana-output
name: k6-prometheus-grafana-output
category: computing-software
field: qa-testing-engineering
product: jmeter-k6
tags: [k6, k6-prometheus, k6-outputs, prometheus-remote-write, grafana-dashboards, influxdb, real-time-results]
level: practitioner
status: verified
description: "Stream k6 metrics in real time to Prometheus (remote write) or InfluxDB and view them in Grafana alongside server metrics; tags, trend stats and cardinality."
sources:
  - https://grafana.com/docs/k6/latest/results-output/real-time/prometheus-remote-write/
  - https://grafana.com/docs/k6/latest/results-output/real-time/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# k6 output to Prometheus / Grafana

**Goal:** see load-test metrics live, correlated with the system's own metrics.

## Prometheus remote write
Prometheus must accept remote write (`--web.enable-remote-write-receiver`).
```bash
K6_PROMETHEUS_RW_SERVER_URL=http://prometheus:9090/api/v1/write \
K6_PROMETHEUS_RW_TREND_STATS="p(50),p(95),p(99),max" \
k6 run -o experimental-prometheus-rw --tag testid=checkout-2026-10-16 script.js
```
- Trends are exported as the configured stats; the default is only `p(99)` (k6 docs). Run on k6 2.3.0 against Prometheus 3.13.4 started with `--web.enable-remote-write-receiver`: the command above created `k6_http_req_duration_p50`, `_p95`, `_p99`, `_max`, plus `k6_http_reqs_total`, `k6_http_req_failed_rate`, `k6_vus`, and each series carried `testid="checkout-..."` and the request `name` label.
- Native histograms: on k6 2.3.0 use `k6 run --features native-histograms -o experimental-prometheus-rw ...`; `K6_PROMETHEUS_RW_TREND_AS_NATIVE_HISTOGRAM=true` still works but logs `Legacy env var detected, use --features or K6_FEATURES instead`. The series are named `k6_http_req_duration_seconds` and `histogram_quantile(0.95, k6_http_req_duration_seconds{testid="..."})` returned a value on Prometheus 3.13.4 with no extra server flag (the k6 docs still tell you to start Prometheus with `--enable-feature=native-histograms`; Prometheus 3.13 logs that flag as a no-op, so it matters only on old 2.x servers).
- Grafana: import the official k6 Prometheus dashboard (ID 19665, titled "k6 Prometheus" on grafana.com) and filter by `testid`.

## Other outputs
- `-o influxdb=http://influx:8086/k6` (v1, built in); InfluxDB v2 via the xk6-output-influxdb extension (not built in: `-o xk6-influxdb` is rejected by stock k6 2.3.0). Built-in output names in 2.3.0 (from the error text for an unknown output): `cloud, csv, experimental-opentelemetry, experimental-prometheus-rw, influxdb, json, opentelemetry, statsd, web-dashboard`.
- `-o json=results.json` / `-o csv=results.csv` for offline analysis (large files).
- `--out cloud` / Grafana Cloud k6 (needs a token: an anonymous run fails with `(403/E4) Missing Authorization token`).
- Several outputs at once: repeat `-o`.

## Tagging
Add `testid` (and `environment`, `build`) tags so runs are separable; tag requests by endpoint name (`tags: { name: 'GET /orders/:id' }`) to avoid URL cardinality explosion from ids in URLs.

## Gotchas
- High-cardinality tags (raw URLs, user ids) overload Prometheus.
- Percentiles averaged across instances in Grafana are wrong; use histograms or k6's own aggregated end-of-test summary for final numbers.

## Verify
During a run, the Grafana dashboard shows RPS, p95 and errors for this testid next to server CPU/latency panels.
