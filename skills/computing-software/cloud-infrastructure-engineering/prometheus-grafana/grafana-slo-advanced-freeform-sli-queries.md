---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.grafana-slo-advanced-freeform-sli-queries
name: grafana-slo-advanced-freeform-sli-queries
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [grafana-slo, grafana-slo-advanced-query, freeform-sli, latency-sli, promql]
level: advanced
status: docs-checked
description: "Write Advanced (freeform) SLI queries in Grafana SLO for latency thresholds from histograms, returning a 0-1 success ratio; pitfalls with bucket boundaries."
sources: ["https://grafana.com/docs/grafana-cloud/alerting-and-irm/slo/create/", "https://grafana.com/docs/grafana-cloud/alerting-and-irm/slo/introduction/", "https://prometheus.io/docs/practices/histograms/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Grafana SLO advanced (freeform) queries

**Goal:** express SLIs the Ratio query option cannot, such as "requests under 300 ms".

## Rules for an advanced query
- In the SLO wizard, the SLI step offers **Ratio query** (success metric and total metric from Prometheus counters, generates the full query with fallbacks) or **Advanced query** (graphical builder or manual PromQL).
- The SLI must return a success ratio between 0 and 1 for each evaluation period (1 = 100% success). For all SLO features to work, express it as `numerator / denominator`.
- The SLI query runs on the source data source; recording rules are written to the target data source (Mimir or another Prometheus-compatible source that accepts recording rules).
- Supported SLI sources: Mimir, Prometheus-compatible, Splunk, AppDynamics, Graphite. For others, record a metric into Mimir with a Grafana-managed recording rule and query that.

## Latency SLI from a classic histogram
```promql
sum(rate(http_request_duration_seconds_bucket{service="checkout", le="0.3"}[5m]))
/
sum(rate(http_request_duration_seconds_count{service="checkout"}[5m]))
```
- `le` means less-or-equal: the cumulative upper bound of the bucket. A bucket boundary must exist at exactly 0.3. If it does not, no interpolation happens and no result is returned; if only some series have it, the result is incomplete with no warning.
- Native histograms: `histogram_fraction(0, 0.3, sum(rate(http_request_duration_seconds{service="checkout"}[5m])))` interpolates, so it is exact only if a boundary sits at 0.3, and it is easier to change later.
- Use base units (seconds), so 300 ms is 0.3.
- Replace `[5m]` with the range your Grafana version expects for SLO queries (see the Grafana SLO examples); the sources read do not state a variable to use.

## Error-counter based
```promql
1 - (
  sum(rate(checkout_failures_total[5m]))
  /
  sum(rate(checkout_attempts_total[5m]))
)
```

## Design advice from Grafana
- Start with availability and latency; keep SLI queries simple. If metrics do not reflect user experience, change the instrumentation rather than writing a complex query.
- Prefer event-based SLIs over time-based; some dashboard views are not supported for time-based SLIs.
- Avoid percentiles in SLIs ("p95 under 2s"): count all requests meeting the target. Percentiles from histograms can be inaccurate.

## Checked
2026-11-08. Confirmed in the Grafana SLO Create SLOs page (Ratio vs Advanced, 0-1 ratio rule, data sources, source and target), the Grafana SLO best-practices page (simple queries, event-based, avoid percentiles) and the Prometheus histograms practices page (`le` semantics, exact boundary requirement, `histogram_fraction`, base units). Removed: the `$__rate_interval` substitution claim, the `group_by` label rule, the combined availability-and-latency query, the "no traffic is treated as missing" and "do not wrap in avg_over_time" pitfalls, the Verify checklist.
Method: documentation only; no commands were run.
