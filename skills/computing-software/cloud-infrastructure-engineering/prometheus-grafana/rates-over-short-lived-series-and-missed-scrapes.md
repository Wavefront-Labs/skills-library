---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.rates-over-short-lived-series-and-missed-scrapes
name: rates-over-short-lived-series-and-missed-scrapes
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [short-lived-series-rate, missed-scrape-rate, rate, extrapolation, scrape-interval, promql]
level: advanced
status: docs-checked
description: "Handle rate() for short-lived series (batch pods, new counters) and missed scrapes: size windows with $__rate_interval, export default zeros, and know the function limits."
sources: ["https://prometheus.io/docs/prometheus/latest/querying/functions/#rate", "https://grafana.com/docs/grafana/latest/datasources/prometheus/template-variables/", "https://prometheus.io/docs/practices/instrumentation/#avoid-missing-metrics", "https://prometheus.io/docs/prometheus/latest/feature_flags/", "https://prometheus.io/docs/introduction/faq/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Rates over short-lived series and missed scrapes

## What the docs say about rate(), increase() and irate()
- `rate(v range-vector)` calculates the per-second average rate of increase over the range. Counter resets are adjusted for, and the calculation extrapolates to the ends of the time range, "allowing for missed scrapes or imperfect alignment of scrape cycles with the range's time period".
- `rate` is only for counters and is best suited for alerting and for graphing slow-moving counters.
- `increase(v range-vector)` is extrapolated to cover the full range, so it can return non-integer results even for integer increments. It is syntactic sugar for `rate(v)` times the seconds in the range, for human readability; use `rate` in recording rules.
- `irate(v range-vector)` uses only the last two data points in the range. Use it only for volatile, fast-moving counters; use `rate` for alerts, since brief changes can reset the `for` clause.
- When combining with `sum()` or any `_over_time` function, apply `rate()` or `irate()` first, then aggregate, otherwise counter resets cannot be detected when a target restarts.

## Short-lived series
A pod that lives 40s with 15s scrapes gives only two or three samples, so a range function has little to work with. Batch jobs and CI pods are therefore easy to undercount, and the first occurrence of a new label value may be missed.

Mitigations:
- Export a default value such as 0 for any series you know may exist in advance: "time series that are not present until something happens are difficult to deal with". Most client libraries (including Go, Java and Python) export 0 automatically for metrics with no labels.
- For jobs you cannot scrape long enough, the FAQ says to use the Pushgateway for batch jobs.
- The `created-timestamp-zero-ingestion` feature flag (experimental, off by default) injects start timestamps as 0-valued samples when appropriate. Prometheus recommends the Prometheus protobuf format for this; OpenMetrics 1.0 start timestamps travel in a `<metric>_created` series that is expensive to parse, and the application must expose start timestamps.
- Aggregate at a longer-lived layer, such as a controller that counts job outcomes.

## Missed scrapes
A failed scrape leaves a gap in the range. In Grafana use `$__rate_interval`, which guarantees a window large enough to capture at least four scrape samples. It is calculated as `max($__interval + scrape_interval, 4 * scrape_interval)`, where `scrape_interval` is the per-query Min step if set, otherwise the data source's Scrape interval setting. Set the data source Scrape interval to match your Prometheus `scrape_interval` (the longest in use if they differ). If it stays at the default 15s while the real interval is 60s, the window is too small and `rate()` returns no data. Do not use `$__rate_interval` in recording rules; use a fixed range such as `[5m]`.

## Check
```promql
count_over_time(up{job="batch"}[10m])          # samples per window actually collected
```

## Checked
Date: 2026-11-07.
Read: the Prometheus functions page sections for `changes()`, `increase()`, `irate()` and `rate()` (the page is large, so other sections were read only where searched, for example `count_over_time`), the Grafana Prometheus template variables page (the `$__rate_interval` section and its pitfalls), the Prometheus instrumentation practices "Avoid missing metrics" section, the whole Feature flags page (start timestamp section) and the whole FAQ (Pushgateway for batch jobs).
Removed because no cited page confirms them: "needs at least two samples", the "half an average interval" and "not below zero" extrapolation limits, the `changes(process_start_time_seconds[1h])` check, the textfile collector advice, the "window >= 4 x scrape interval" formula as a standalone rule (replaced with Grafana's documented formula), and the invented Verify checklist.
Method: documentation only; no commands were run.
