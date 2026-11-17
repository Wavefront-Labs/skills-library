---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.promql-timestamp-function-and-sample-age
name: promql-timestamp-function-and-sample-age
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [timestamp-function, sample-age, staleness-markers, promql-timestamps, freshness-alerts]
level: practitioner
status: gated
description: "Use timestamp() to find how old the latest sample of each series is, detect stale exporters and pushed metrics, and compare scrape vs exposed timestamps."
sources: ["https://prometheus.io/docs/prometheus/latest/querying/functions/#timestamp", "https://prometheus.io/docs/prometheus/latest/querying/basics/#staleness", "https://prometheus.io/docs/practices/pushing/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# timestamp() and sample age

`timestamp(v instant-vector)` returns the timestamp of each sample (seconds since epoch), not its value.

## Uses
```promql
# seconds since the last sample of each series (stale exporter / stuck pusher)
time() - timestamp(my_metric)
# targets whose last scrape is older than 2 minutes (should be rare; up==0 is usually better)
time() - timestamp(up) > 120
# Pushgateway: last push per group (push_time_seconds is a gauge holding the push time in epoch seconds)
time() - push_time_seconds
# metric exposes its own timestamps (honor_timestamps): lag behind wall clock
time() - timestamp(sensor_reading)
```
Run on Prometheus 3.15.1: `time() - timestamp(up)` returned 1-3 s for every target (the age of the last scrape sample); `time() - timestamp(fresh)` in a `promtool test rules` case returned 0. The `honor_timestamps` example was not run (gated: unconfirmed, source is paywalled or blocked).

## How it interacts with the lookback
An instant query only finds samples within the lookback delta (5m default). If a series stopped more than 5m ago (or got a staleness marker) it returns nothing (run: `time() - timestamp(ma)` for a pushed series whose group had just been wiped returned an empty result), so `time() - timestamp(x) > 600` can never fire. Wrapping the selector in `last_over_time` does NOT fix it the way the original text said: `time() - timestamp(last_over_time(ma[1h]))` returned 0 for every series, because `timestamp()` of a function result is the evaluation time, not the original sample time. Two forms that did return the real age:
```promql
# experimental: needs --enable-feature=promql-experimental-functions (run: 92 s for a series last written 92 s earlier)
time() - ts_of_last_over_time(my_metric[1h]) > 600
# no feature flag: a subquery over timestamp() (run: 110.7 s with a 15 s step; precision is the subquery step)
time() - max_over_time(timestamp(my_metric)[1h:15s]) > 600
```
Or alert with `absent_over_time(my_metric[10m])` (run in a unit test: returned 1 with `{}` labels when the series had no sample in the window).

## Gotchas
- `timestamp()` is only the sample time for a plain vector selector. For `timestamp(rate(...))`, `timestamp(last_over_time(...))` and other function results it returns the evaluation time (run: `time() - timestamp(rate(...))` was 0), which is not useful.
- Prefer exported `*_timestamp_seconds` gauges for "last success" over sample age: a job that runs but fails still produces fresh samples.

## Verify
- [ ] Freshness alerts for pushed or federated data use `ts_of_last_over_time`, the subquery form or `absent_over_time` (not `timestamp(last_over_time(...))`) and are unit-tested.

## Checked
Prometheus 3.15.1 (windows-amd64) run locally against a live server with experimental functions enabled, plus `promtool test rules`: `timestamp(up)`, a stale pushed series versus the lookback window, `timestamp(last_over_time(...))` (returned 0), `ts_of_last_over_time` (real age), the `max_over_time(timestamp(x)[1h:15s])` subquery (real age), `timestamp(rate(...))`, and `absent_over_time`. Docs read: querying/functions.md at tag v3.15.1 (`timestamp()`, experimental `ts_of_*_over_time`). Not run: `honor_timestamps` series, federation.
