---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.prometheus-metric-design-and-cardinality-control
name: prometheus-metric-design-and-cardinality-control
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [prometheus, metric-design, metric-naming, base-units, counter, gauge, histogram, summary, labels, cardinality, high-cardinality, series-count, tsdb-status, promtool-tsdb-analyze, sample-limit, label-limit, metric-relabel-configs, write-relabel-configs, remote-write, info-metrics, exemplars, histogram-buckets, native-histograms]
level: advanced
status: verified
description: "Design Prometheus metrics that stay cheap: naming and base units, choosing counter/gauge/histogram, bounded labels, bucket budgets, finding series hogs, and scrape limits plus relabel drops."
sources: ["Prometheus documentation - Metric and label naming", "Prometheus documentation - Instrumentation best practices", "Prometheus documentation - Configuration (scrape limits, relabeling)", "Prometheus documentation - TSDB status API and promtool"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Prometheus metric design and cardinality control — every series earns its keep

**Goal:** metrics whose names and labels are self-explanatory and aggregatable, with a
known series budget per service, and guardrails that stop one bad deploy from
exploding TSDB memory. Query patterns over these metrics are in
`computing-software.cloud-infrastructure-engineering.prometheus-grafana.promql-query-patterns`;
cross-signal instrumentation strategy is in
`computing-software.cloud-infrastructure-engineering.observability.instrumentation-strategy`.

## 1. Naming
`<namespace>_<subsystem>_<what>_<unit>[_total]`, snake_case, base units:
- Time in **seconds**, size in **bytes**, ratios 0–1 (`_ratio`), temperature in celsius.
  Never `_ms` or `_kb` — dashboards then mix units silently.
- Counters end in `_total` (`app_http_requests_total`); the Python client appends it itself (`Counter('app_x', ...)`
  exposes `app_x_total`, and the OpenMetrics output declares the family without the suffix: `# TYPE app_x counter`).
- A metric name means one thing: `sum()` over all its labels must make sense. If
  summing is nonsense (e.g. mixing queue depth and queue capacity), split the metric.
- `_info` gauges with value 1 carry build/version metadata as labels:
  `app_build_info{version="1.8.2", commit="<SHA>"} 1`, joined in queries with `group_left`.

## 2. Choosing a type
| Measuring | Type |
|---|---|
| Things that happen (requests, errors, bytes sent) | Counter |
| Current level (queue depth, in-flight, temperature) | Gauge |
| Distribution you will aggregate across instances (latency, size) | Histogram |
| Pre-computed quantile from one process only | Summary (rarely right) |
| Last time something succeeded | Gauge of Unix seconds (`..._last_success_timestamp_seconds`) |

Prefer "timestamp of last success" over "seconds since" — the latter needs constant updates.

## 3. Labels and the series budget
Series for one metric = product of distinct values of each label (× buckets + 2 for
histograms). Example: 12 buckets (including `+Inf`) + `_sum` + `_count` = 14 series × 20 routes × 5
methods × 5 status classes × 30 pods = **210,000** series for one latency histogram.
Reduce: status *class* (`2xx`) not code, drop `method` if unused, fewer buckets.
- Allowed label values: bounded and known in advance (route template, region, status class).
- Forbidden: user/tenant IDs (unless few and fixed), request IDs, raw paths, emails,
  error message text, timestamps. Put IDs on **exemplars** or traces instead.
- Initialise known label combinations to 0 at startup so `rate()` and absence alerts
  work before the first event.
- Budget rule of thumb (assumption, tune to your hardware): keep any single metric
  under ~10k series and a service under ~50k without explicit sign-off.

## 4. Histogram buckets
- Place boundaries around SLO thresholds and the expected range, roughly exponential:
  `[0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1, 2.5, 5, 10]` is the client default — often too many for low-traffic services, too coarse near a 300 ms SLO.
- Native histograms (stable since Prometheus 3.8; enable per scrape config with `scrape_native_histograms`)
  store high-resolution buckets in one series and reduce this trade-off.

## 5. Finding the hogs
```promql
topk(10, count by (__name__) ({__name__=~".+"}))          # heavy metric names
topk(10, count by (job) ({__name__=~".+"}))               # heavy jobs
prometheus_tsdb_head_series                                 # total head series
```
- UI `Status → TSDB status` (`/api/v1/status/tsdb`) lists top label names by value count.
- Offline: `promtool tsdb analyze <DATA_DIR>` shows churn and highest-cardinality labels.
- Watch **churn** too (`rate(prometheus_tsdb_head_series_created_total[1h])`): pod
  labels on short-lived jobs create new series constantly even at low head count.

## 6. Guardrails at scrape time
```yaml
scrape_configs:
  - job_name: app
    sample_limit: 20000             # whole scrape fails if exceeded
    label_limit: 30
    label_value_length_limit: 200
    metric_relabel_configs:
      - source_labels: [__name__]
        regex: "app_debug_.*"
        action: drop
      - regex: "request_id|session_id"
        action: labeldrop
      - source_labels: [path]
        regex: "/users/[0-9]+"
        target_label: path
        replacement: "/users/:id"
```
- Exceeding `sample_limit` fails the scrape (`up == 0`) — loud by design; alert on
  `prometheus_target_scrapes_exceeded_sample_limit_total`.
- `labeldrop` can create duplicate series that then collide; drop only labels that are
  not part of identity, or aggregate with recording rules instead.
- For remote write, filter with `write_relabel_configs` and ship recording-rule
  aggregates rather than raw high-cardinality series.

## Gotchas
- Fixing labels in code is the real fix; relabel rules are a tourniquet.
- Renaming a metric breaks every dashboard and alert; emit both names for a deprecation window.
- A label added later to an existing metric changes series identity — queries using `by` keep working, joins using `on()` may not.
- Kubernetes service discovery adds pod/instance labels automatically; account for them in the budget.

## Verify
- [ ] New metrics pass `promtool check metrics` (`curl -s <TARGET>/metrics | promtool check metrics`).
- [ ] Each new metric's worst-case series count is computed in the PR description.
- [ ] Every scrape job sets `sample_limit`, and an alert watches limit breaches.
- [ ] Top-10 metrics by series are reviewed monthly; none carry IDs.
- [ ] Head series and churn graphs exist on the Prometheus self-monitoring dashboard.
