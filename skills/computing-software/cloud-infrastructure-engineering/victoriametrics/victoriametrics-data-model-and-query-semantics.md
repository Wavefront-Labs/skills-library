---
id: computing-software.cloud-infrastructure-engineering.victoriametrics.victoriametrics-data-model-and-query-semantics
name: victoriametrics-data-model-and-query-semantics
category: computing-software
field: cloud-infrastructure-engineering
product: victoriametrics
tags: [data-model, labels, cardinality, metric-types, instant-query, range-query, lookbehind-window, staleness]
level: intro
status: docs-checked
description: "Understand VictoriaMetrics series, labels, samples, metric types, push versus pull and how instant and range queries fill gaps."
sources: ["https://docs.victoriametrics.com/victoriametrics/keyconcepts/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Victoriametrics data model and query semantics

A metric is a numeric measure such as `requests_total`; labels are string key-value pairs, for example `requests_total{path="/", code="200"}`. A time series is one unique metric name plus label set. The name is stored in the special `__name__` label. A raw sample is a `(value, timestamp)` pair: float64 values keep up to 12 significant decimal digits and timestamps are Unix milliseconds. If the timestamp is omitted the current time is used.

Cardinality is the number of unique series. Avoid volatile label values such as session or query IDs. Defaults: 40 labels per series (`-maxLabelsPerTimeseries`) and 4KiB per label value (`-maxLabelValueLen`).

VictoriaMetrics stores no metric type. Counters only increase except on reset (use `rate()` and `increase()`); gauges rise and fall; histograms are bucket counters with `_bucket`, `_sum`, `_count` and `vmrange` or `le` labels; summary quantiles are computed client-side and cannot be aggregated across instances.

Write models: push (client sends, for example `POST /api/v1/import`) or pull (VictoriaMetrics or vmagent scrapes at `scrape_interval`; `up == 0` flags unreachable targets and `/targets` lists them).

Read models:
- Instant query `/api/v1/query` returns one sample per series; if none exists at that exact time it looks back within `step` (default 5m).
- Range query `/api/v1/query_range` evaluates at `start + N*step`, filling missing points by repeating the previous raw sample. The lookbehind window is the median interval of the last 20 raw samples.
- Recent data is hidden for 30 seconds by default (`-search.latencyOffset`); override per query with `latency_offset`.

## Checked

2026-11-03. Flags, endpoints, HTTP paths, defaults, limits and version gates were checked against the official VictoriaMetrics documentation pages cited in `sources` (docs.victoriametrics.com, fetched this batch) with a phrase-by-phrase comparison. No wrong claims were found; no claims were removed.

Method: documentation only; no commands were run.
