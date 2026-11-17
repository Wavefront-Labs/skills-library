---
id: computing-software.cloud-infrastructure-engineering.vector.metric-event-data-model
name: metric-event-data-model
category: computing-software
field: cloud-infrastructure-engineering
product: vector
tags: [metric-events, counter, gauge, histogram, summary, distribution, set, vector]
level: practitioner
status: docs-checked
description: "Choose among Vector's metric types and know how they map to Prometheus and StatsD style metrics."
sources:
  - https://vector.dev/docs/architecture/data-model/metric/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A Vector metric event is a numerical operation performed on a time series. Metrics are first class: they are not structured logs, so they interoperate with metrics services without conversion. The model favours correctness over purity and combines types from Prometheus and StatsD.

Common fields: `name` (required), `namespace` (optional; prepended to the name or used as native namespacing depending on the service), `kind` (required), `tags` (required; a map of tag name to a string, null, or a list of those), `timestamp`, and optional `interval_ms`.

Value types, exactly one per event:

- `counter`: a value that can be incremented or reset to zero but not decremented; the value can only be positive.
- `gauge`: a point-in-time value that can go up or down, such as memory or CPU usage.
- `histogram` (also called a timer): observations counted into configurable `buckets`, plus a total `count` and `sum`.
- `summary`: like a histogram but with configurable `quantiles` calculated over a sliding window, plus `count` and `sum`.
- `distribution`: sampled values with a `statistic`, for services that support global histograms and summaries.
- `set`: an array of unique `values`.

Pick the type your destination understands. Converting logs into counters is done with the `log_to_metric` transform.

Verify with the `console` sink and JSON encoding to see `kind`, `name` and the value block of each metric.

## Checked

2026-11-03. Read architecture/data-model/metric and sinks/console. Confirmed: first-class metrics, the field list, counter, gauge, histogram (timer), summary, distribution and set semantics. Nothing removed.

Method: documentation only; no commands were run.
