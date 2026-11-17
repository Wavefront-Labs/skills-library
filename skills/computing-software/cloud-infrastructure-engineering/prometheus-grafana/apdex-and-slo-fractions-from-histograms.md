---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.apdex-and-slo-fractions-from-histograms
name: apdex-and-slo-fractions-from-histograms
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [promql, apdex, apdex-score, latency-sli, histogram-buckets, slo, good-events]
level: practitioner
status: verified
description: "Compute Apdex and latency-SLI good-event fractions from Prometheus histogram buckets, including combining with error status and recording rules for SLO windows."
sources: ["https://prometheus.io/docs/practices/histograms/#apdex-score", "https://www.apdex.org/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Apdex and SLO fractions from histograms

## Apdex
Apdex = (satisfied + tolerating/2) / total, with satisfied <= T and tolerating <= 4T. Configure buckets with
boundaries at T and 4T (e.g. T = 0.3 s -> buckets 0.3 and 1.2).
```promql
(
  sum(rate(http_request_duration_seconds_bucket{le="0.3"}[5m]))
  +
  sum(rate(http_request_duration_seconds_bucket{le="1.2"}[5m]))
) / 2
/ sum(rate(http_request_duration_seconds_count[5m]))
```
Buckets are cumulative, so `le="1.2"` already includes the satisfied ones; adding both and halving gives
satisfied + tolerating/2.

## Latency SLI (fraction of good requests)
```promql
# good = fast AND successful
sum(rate(http_request_duration_seconds_bucket{le="0.3", code!~"5.."}[5m]))
/
sum(rate(http_request_duration_seconds_count[5m]))
```
Requires `code` on the histogram; otherwise combine a separate error ratio (approximate).

## Recording rules for SLO windows
```yaml
- record: job:sli_latency_good:rate5m
  expr: sum by (job) (rate(http_request_duration_seconds_bucket{le="0.3"}[5m]))
- record: job:sli_total:rate5m
  expr: sum by (job) (rate(http_request_duration_seconds_count[5m]))
- record: job:sli_latency:ratio_rate30d
  expr: sum_over_time(job:sli_latency_good:rate5m[30d]) / sum_over_time(job:sli_total:rate5m[30d])
```
Native histograms: `histogram_fraction(0, 0.3, sum by (job) (rate(x[5m])))` works for any threshold (an estimate when it is not a bucket boundary). The docs say `histogram_fraction` also accepts classic histograms (it returned 0.5 on 3.15.0 for `histogram_fraction(0, 0.3, rate(h_bucket[5m]))`), but off-boundary thresholds are estimates, so acting on the bucket series as above is more robust.

Measured on Prometheus 3.15.0 with 100 requests per minute (50 at or below 0.3 s, 90 at or below 1.2 s): the Apdex query returned 0.7, which is (50 + (90 - 50) / 2) / 100, and the fast-fraction query returned 0.5. The recording rules passed `promtool check rules`.

## Gotchas
- The `le` label value must match exactly as exposed (`"0.3"` vs `"0.30"`); check with `count by (le)`.
- Apdex hides distribution shape; keep a p99 panel next to it.
- Averaging Apdex across services is meaningless unless weighted by traffic; compute from summed rates.

## Verify
- [ ] Apdex stays within 0..1 and drops during a known slow incident.
- [ ] `le` values used in queries exist for all jobs.
