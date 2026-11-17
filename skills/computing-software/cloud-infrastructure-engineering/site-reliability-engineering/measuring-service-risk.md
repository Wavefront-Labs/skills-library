---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.measuring-service-risk
name: measuring-service-risk
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [measuring-service-risk, unplanned-downtime-metric, aggregate-availability, time-based-availability, request-success-rate, embracing-risk, promql]
level: practitioner
status: docs-checked
description: "Measure service risk as time-based or aggregate (request) availability, choose the right one for distributed services, and compute it from Prometheus counters."
sources: ["https://sre.google/sre-book/embracing-risk/", "https://prometheus.io/docs/prometheus/latest/querying/functions/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Measuring service risk

The SRE Book represents risk tolerance as the acceptable level of **unplanned downtime**, expressed as the
availability target in "nines"; each additional nine is an order-of-magnitude improvement toward 100 percent.

## Time-based availability
```
availability = uptime / (uptime + downtime)
```
Traditional for serving systems. Over a year it converts a target into allowed downtime minutes (the book's
Availability Table). The book says it is usually not meaningful for globally distributed services: fault
isolation means a subset of traffic is almost always being served somewhere, so the service is at least
partially up at all times.

## Aggregate (request) availability
```
availability = successful_requests / total_requests     over a rolling window
```
This yield-based metric is what the book uses instead. Its example: a system serving 2.5M requests a day with a
daily target of 99.99 percent can serve up to 250 errors and still hit the target for that day.

## Implementation (Prometheus)
Metric and label names below are examples; use your own. `increase()` handles counter resets and extrapolates
to the range window (Prometheus functions page).
```promql
# 28-day aggregate availability, 5xx counted as failure
1 - (
  sum(increase(http_requests_total{job="api",code=~"5.."}[28d]))
  /
  sum(increase(http_requests_total{job="api"}[28d]))
)
```
`avg_over_time` and `sum_over_time` aggregate a range vector, so a recorded series can be rolled up over long
windows instead of scanning raw samples on every dashboard load.

## Decisions to document
- What counts as unplanned downtime (is announced maintenance excluded?).
- How partial outages are counted (weight by affected traffic).
- Which data source is the denominator; a server that is fully down records no requests, so pair server-side
  ratios with a probe or load-balancer data.

## Checked
2026-11-01. Confirmed against the SRE Book chapter Embracing Risk (unplanned downtime, nines, time-based and
aggregate formulas, the 2.5M-request example, why time-based is poor for global services) and the Prometheus
functions page (`increase`, `avg_over_time`, `sum_over_time`). Removed: blackbox probe query, the workbook
latency-as-failure advice, recording-rule recipe and verify targets, not confirmed in the fetched pages.
Method: documentation only; no commands were run.
