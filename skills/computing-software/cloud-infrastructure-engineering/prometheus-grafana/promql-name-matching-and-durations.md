---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.promql-name-matching-and-durations
name: promql-name-matching-and-durations
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [promql, name-label-matching, metric-name-regex-selector, utf8-metric-names, range-duration-choice, duration-units, pca]
level: practitioner
status: gated
description: "Write PromQL selectors on __name__ (regex across metrics, UTF-8 quoted names) and pick range durations correctly: units, combined durations, and the 'at least 4 scrapes' rule."
sources: ["https://prometheus.io/docs/prometheus/latest/querying/basics/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Selecting by metric name and choosing durations

## __name__ matching
`http_requests_total{job="api"}` is sugar for `{__name__="http_requests_total", job="api"}`.
```promql
{__name__=~"node_network_(receive|transmit)_bytes_total", device!="lo"}   # several metrics at once
count by (__name__) ({job="api"})                                        # list metrics of a job with series counts
{__name__=~"job:.*"}                                                     # all recording-rule outputs of a level
```
- A selector must contain at least one matcher that doesn't match the empty string:
  `{job=~".*"}` is rejected (run: `vector selector must contain at least one non-empty matcher`); `{__name__=~".+"}` works (run: `count({__name__=~".+"})` was 2068 on a small server) but is expensive.
- Functions like `rate()` drop `__name__` from results (run: `rate(up[1m])` returned only `instance` and `job`); binary ops on multiple names need `on()`/`ignoring()`.
- `label_replace(..., "__name__", ...)` can rename metrics in results (use sparingly).

## UTF-8 names (Prometheus 3)
```promql
{"http.server.request.duration_count", "service.name"="checkout"}
sum by ("k8s.namespace.name") (rate({"http.server.request.duration_count"}[5m]))
```
The quoted name goes inside the braces as the first, label-less term (run: `{"up", job="prom"}` and `sum by ("job") (rate({"prometheus_http_requests_total"}[5m]))` returned data; a dotted name with a dotted label, as in the examples, parsed and returned nothing because no such series existed).

## Durations
Units: `ms`, `s`, `m`, `h`, `d` (24h), `w` (7d), `y` (365d) (basics docs). Combine largest-first: `1h30m` and `2d12h` ran; `30m1h` fails (`not a valid duration string`) and `1.5h` fails (`unknown unit "." in duration`).
Arithmetic in durations works on 3.15.1 with no feature flag: `up[5m * 2]` returned a 10-minute range (run; the basics docs list it without a flag). It is newer syntax, so don't rely on it for rules that must also run on older servers.

## Choosing a range for rate/increase
- Window >= 4x scrape interval (2x is the bare minimum to have two samples; 4x tolerates one missed scrape).
  30 s scrape -> `[2m]`; in Grafana use `$__rate_interval` (gated: unconfirmed, source is paywalled or blocked; Grafana not run). Run with a 5 s scrape interval: `rate(x[4s])` returned nothing, while `[6s]`, `[11s]`, `[16s]` and `[21s]` returned results (a window shorter than the interval can hold one sample at most).
- Longer windows smooth; shorter windows react faster. Alerts: 5m is a common balance; SLO burn rates use
  the windows the math dictates (5m/1h/6h/3d).
- `*_over_time` functions use all samples in the window: `max_over_time(x[1h])` really scans an hour of data (functions docs: all values in the interval have the same weight).

## Verify
- [ ] No selector is rejected for matching the empty string.
- [ ] Rate windows in dashboards and rules are >= 4x the job's scrape interval.

## Checked
Prometheus 3.15.1 (windows-amd64) live queries via `/api/v1/query` against a small local server: the `__name__` regex selectors, `count by (__name__)`, rejected `{job=~".*"}`, `{__name__=~".+"}`, `rate` name dropping, UTF-8 quoted names, duration literals (`1h30m`, `2d12h`, `1y`, `30m1h`, `1.5h`), duration arithmetic (`5m * 2`, no flag), and rate windows of 4 s to 21 s against a 5 s scrape. Docs read: querying/basics.md and functions.md at tag v3.15.1. Not run: Grafana `$__rate_interval`, SLO burn-rate windows.
