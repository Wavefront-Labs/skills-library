---
id: computing-software.cloud-infrastructure-engineering.grafana-mimir.grafana-mimir-out-of-order-samples
name: grafana-mimir-out-of-order-samples
category: computing-software
field: cloud-infrastructure-engineering
product: grafana-mimir
tags: [out-of-order, ingestion, time-window, query-cache, recording-rules]
level: practitioner
status: docs-checked
description: "Covers enabling Mimir out-of-order sample ingestion with out_of_order_time_window, per-tenant overrides, and the effects on query caching and recording rules."
sources: ["https://grafana.com/docs/mimir/latest/configure/configure-out-of-order-samples-ingestion/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Out-of-order sample ingestion

Mimir can accept samples older than the latest for a series within a time window. Samples inside the window are not dropped.

## Enable

```yaml
limits:
  out_of_order_time_window: 5m
```

Per tenant, use a runtime override (`tenant1: out_of_order_time_window: 2h`). Setting `0s` disables out-of-order ingestion while still allowing queries of out-of-order samples already ingested.

## Why it exists

Normally, if a series exists in the TSDB head, a new sample must be newer than the latest stored one or it is out-of-order. If the series is new, the sample must be within bounds, going back 1 hour from the head max time with a 2 hour block range, or it is out-of-bounds. Prometheus remote write and Grafana Alloy write each series in order, so you should not see out-of-order samples from them.

## Side effects

- **Query cache**: results cached earlier can change as late samples arrive. Pass the same limits config to the query-frontend; it then uses a 10 minute TTL for cache entries inside the window. To avoid caching that window, set `-query-frontend.max-cache-freshness` equal to the window, at the cost of more load.
- **Recording rules**: recorded samples can become outdated. With a window under 10 minutes, delay evaluation using `-ruler.evaluation-delay-duration`.

## Checked

2026-11-04. Confirmed against the Mimir page "Configure out-of-order samples ingestion": the setting, per-tenant override, `0s` behaviour, rules for in-order and out-of-bounds samples, cache TTL and rule delay. Nothing removed.
Method: documentation only; no commands were run.
