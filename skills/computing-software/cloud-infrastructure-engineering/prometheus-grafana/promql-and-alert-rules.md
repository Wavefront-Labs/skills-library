---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.promql-and-alert-rules
name: promql-and-alert-rules
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [prometheus, grafana, promql, rate, irate, increase, histogram-quantile, native-histograms, recording-rules, alerting-rules, alertmanager, for-clause, keep-firing-for, cardinality, labels, counters, gauges, promtool, mimir, thanos, victoriametrics, rate-interval, absent, slo-alerts, grafana-panels]
level: practitioner
status: verified
description: "Write PromQL that is correct under counter resets and scrape jitter, latency quantiles from histograms, recording rules, and alerts with sane for: windows and bounded cardinality."
sources: ["Prometheus docs - Querying basics and functions", "Prometheus docs - Recording rules and alerting rules", "Prometheus docs - Histograms and summaries", "Grafana docs - Prometheus data source and $__rate_interval"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# PromQL and alert rules — correct queries, quiet pagers

**Goal:** dashboards and alerts built from queries that mean what they say, evaluated
cheaply via recording rules, and alerts that fire on user pain, not scrape noise.

## 1. Counters: rate, irate, increase
- Always wrap counters (`*_total`) in a function; raw counters only ever go up.
- `rate(x[5m])` = per-second average over the window, handling resets. Use for alerts and most graphs.
- `irate(x[5m])` = last two samples only; spiky, fine for zoomed-in debugging, wrong for alerts.
- `increase(x[1h])` = `rate × window`, extrapolated, so it can return non-integers.
- `rate()` needs two samples in the window (tested: `rate(c[15s])` with 15 s scrapes returned nothing); use at
  least 4 scrape intervals (with 15 s scrapes, `[1m]` minimum; `[5m]` typical). Grafana's docs say
  `$__rate_interval` guarantees a window of at least four scrape samples.
- **Aggregate after rate**, never before: `sum by (service) (rate(http_requests_total[5m]))`.
  Summing first and then taking `rate` over a subquery, `rate(sum(...)[5m:])`, breaks reset handling (tested: with one of two
  counters resetting it gave 3.0/s against the correct 1.96/s).

## 2. Ratios and histograms
```promql
# error ratio
sum by (service) (rate(http_requests_total{code=~"5.."}[5m]))
/
sum by (service) (rate(http_requests_total[5m]))

# p99 latency from classic histogram
histogram_quantile(0.99,
  sum by (le, service) (rate(http_request_duration_seconds_bucket[5m])))
```
- Keep `le` in the `by` clause or the quantile is meaningless.
- Quantile accuracy is limited by bucket boundaries (linear interpolation within a bucket).
  Put boundaries near your SLO threshold (e.g. 0.3 s if the target is 300 ms).
- To measure "percent of requests under 300 ms", use the bucket directly — exact, cheaper:
  `sum(rate(..._bucket{le="0.3"}[5m])) / sum(rate(..._count[5m]))`.
- Summaries' quantiles cannot be aggregated across instances; prefer histograms.
- **Native histograms** (stable since Prometheus 3.8, opt-in per scrape config with `scrape_native_histograms`; behind a feature flag before) give
  high-resolution buckets with one series; query with `histogram_quantile(0.99, sum(rate(x[5m])))` without `le`.

## 3. Recording rules
```yaml
groups:
- name: http.rules
  interval: 30s
  rules:
  - record: service:http_requests:rate5m
    expr: sum by (service) (rate(http_requests_total[5m]))
  - record: service:http_errors:ratio_rate5m
    expr: |
      sum by (service) (rate(http_requests_total{code=~"5.."}[5m]))
      / sum by (service) (rate(http_requests_total[5m]))
```
Naming convention `level:metric:operations`. Use for anything on a busy dashboard or
alert, and to pre-aggregate away high-cardinality labels.

## 4. Alert rules
```yaml
  - alert: HighErrorRate
    expr: service:http_errors:ratio_rate5m > 0.05 and service:http_requests:rate5m > 1
    for: 10m
    keep_firing_for: 5m
    labels: {severity: page}
    annotations:
      summary: "{{ $labels.service }} 5xx ratio {{ $value | humanizePercentage }}"
      runbook_url: "https://runbooks.example.com/high-error-rate"
```
- `for:` requires the condition true on every evaluation for that long; it filters blips
  but delays detection. Typical 5-15 m for pages.
- `keep_firing_for` (Prometheus 2.42+) stops flapping resolve/fire cycles.
- Guard ratios with a traffic floor (`and ... > 1`) to avoid paging on 1 of 2 requests.
- Missing data: `absent(up{job="api"})` or `absent_over_time(...)`, since a vanished series makes the main alert silently stop.
- Page on symptoms (error ratio, latency, SLO burn); route cause alerts (disk, CPU) to tickets.
- Alertmanager: `group_by: [alertname, service]`, `group_wait: 30s`, `group_interval: 5m`,
  `repeat_interval: 4h`; inhibit warnings when the matching critical fires.

## 5. Cardinality
- Series count = product of label value counts. Never label with user IDs, request IDs,
  full URLs or unbounded error messages; normalise routes (`/users/:id`).
- Find offenders: `topk(10, count by (__name__) ({__name__=~".+"}))` and the TSDB
  status page (`/tsdb-status`).
- Drop at scrape with `metric_relabel_configs` (`action: labeldrop` / `drop`), and set `sample_limit` per job.

## Gotchas
- `rate()` over a window shorter than 2 samples returns nothing — gaps in panels at short ranges.
- Binary operators match on all labels; mismatched label sets give empty results. Use `on()`/`ignoring()` and `group_left`.
- `sum without (instance)` keeps everything else — safer than `by` when labels may be added later, but riskier for cardinality.
- Grafana computes `$__rate_interval` as max($__interval + scrape_interval, 4 * scrape_interval): at long time ranges `$__interval` grows, so the window widens and short spikes are averaged out. The scrape interval used is the query's Min step or the data source's Scrape interval setting, which must match the real one; the panel Min interval is not part of the calculation (Grafana docs).
- Alert `$value` is the last expression result; with `and`, it is the left side's value.
- Restarts of a target show as counter resets; a target that *never* exports zero first will under-count its first increment.

## Verify
- [ ] `promtool check rules rules/*.yml` passes, and `promtool test rules` covers each page alert.
- [ ] No alert uses `irate` or an un-rated counter.
- [ ] Every `histogram_quantile` keeps `le` in its aggregation.
- [ ] Every paging alert has `for:`, a traffic floor where it is a ratio, and a runbook URL.
- [ ] Top-10 metrics by series count are known and none carry unbounded labels.
- [ ] An `absent()` alert exists for each critical scrape job.

Related: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.slos-and-error-budgets
