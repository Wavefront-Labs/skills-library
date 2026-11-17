---
id: computing-software.cloud-infrastructure-engineering.observability.red-dashboard-per-service
name: red-dashboard-per-service
category: computing-software
field: cloud-infrastructure-engineering
product: observability
tags: [red-dashboard, rate-errors-duration-dashboard, red-method, golden-signals, grafana, promql]
level: practitioner
status: draft
description: "Build a standard RED (rate, errors, duration) Grafana dashboard per service with templated PromQL, histogram percentiles and consistent row layout."
sources: ["https://grafana.com/blog/2018/08/02/the-red-method-how-to-instrument-your-services/", "https://grafana.com/docs/grafana/latest/dashboards/build-dashboards/best-practices/", "https://prometheus.io/docs/practices/histograms/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# RED dashboard per service

Goal: every service gets the same first dashboard so on-call can read any of them in seconds.

## Variables
- `datasource` (Prometheus), `service` (`label_values(http_server_request_duration_seconds_count, service_name)`), `route` (multi, include All).

## Panels (one row per signal, request-scoped)
```promql
# Rate (req/s) by route
sum by (http_route) (rate(http_server_request_duration_seconds_count{service_name="$service", http_route=~"$route"}[$__rate_interval]))
# Errors (ratio of 5xx)
sum(rate(http_server_request_duration_seconds_count{service_name="$service", http_response_status_code=~"5.."}[$__rate_interval]))
/ sum(rate(http_server_request_duration_seconds_count{service_name="$service"}[$__rate_interval]))
# Duration p50/p90/p99
histogram_quantile(0.99, sum by (le) (rate(http_server_request_duration_seconds_bucket{service_name="$service", http_route=~"$route"}[$__rate_interval])))
```
Metric names follow OTel HTTP semconv translated to Prometheus; adjust to your instrumentation (`http_requests_total` etc.).

## Layout rules
- Top row: stat panels for current rate, error ratio, p99 with thresholds equal to the SLO.
- Second row: time series of the same three, shared crosshair, same Y units (req/s, percent, seconds).
- Third row: per-route breakdown tables (topk 10 by rate and by error ratio).
- Link to the trace search for the service and to logs filtered by `service_name`.

## Gotchas
- Error ratio over a tiny denominator spikes to 100%; add `and sum(rate(...)) > 1` or show the count too.
- Averaging percentiles across instances is wrong; aggregate buckets with `sum by (le)` first.
- Client-side (outbound) RED belongs on a separate row; do not mix server and client spans.

## Verify
- [ ] Dashboard JSON is generated from one template (grafonnet/Foundation SDK) for all services.
- [ ] During a test error injection the error panel moves within one scrape interval.
