---
id: computing-software.database-administration.elasticsearch.data-stream-lifecycle-and-downsampling
name: data-stream-lifecycle-and-downsampling
category: computing-software
field: database-administration
product: elasticsearch
tags: [database-administration, elasticsearch, data-stream-lifecycle, downsampling, data-streams, time-series, elasticsearch-lifecycle]
level: practitioner
status: docs-checked
description: "Manage Elasticsearch data stream retention with data stream lifecycle (DSL) instead of ILM, and downsample time series data streams to cut storage."
sources:
  - https://github.com/elastic/docs-content/blob/main/manage-data/lifecycle/data-stream.md
  - https://github.com/elastic/docs-content/blob/main/manage-data/data-store/data-streams/downsampling-concepts.md
  - https://github.com/elastic/docs-content/blob/main/manage-data/data-store/data-streams/run-downsampling.md
  - https://github.com/elastic/elasticsearch/blob/main/docs/reference/elasticsearch/configuration-reference/data-stream-lifecycle-settings.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Data stream lifecycle and downsampling

## Data stream lifecycle
A simpler alternative to ILM for data streams: you state retention, Elasticsearch handles rollover and merging.
```json
PUT _index_template/metrics-app
{ "index_patterns": ["metrics-app-*"], "data_stream": {},
  "template": { "lifecycle": { "data_retention": "30d" } } }

PUT _data_stream/metrics-app-prod/_lifecycle
{ "data_retention": "14d" }

GET _data_stream/metrics-app-prod/_lifecycle/explain   # per backing index state
```
- Rollover is automatic (`cluster.lifecycle.default.rollover`, documented as an implementation detail that may change; it currently defaults to `max_age=auto,max_primary_shard_size=50gb,min_docs=1,max_primary_shard_docs=200000000`, where `auto` age depends on the retention).
- There are no hot/warm/cold phases. From Stack 9.5 (not serverless) it can move older backing indices to partially mounted searchable snapshots; use ILM when you need phase-based tiering.
- If a template has both ILM policy and lifecycle, `index.lifecycle.prefer_ilm` (default true) decides.
- Global defaults: `data_streams.lifecycle.retention.default` / `.max` cluster settings.

## Downsampling (time series data streams)
Requires a TSDS (`index.mode: time_series` with dimensions and metric fields).
With DSL:
```json
PUT _data_stream/metrics-app-prod/_lifecycle
{ "data_retention": "365d",
  "downsampling": [ { "after": "1d", "fixed_interval": "5m" }, { "after": "30d", "fixed_interval": "1h" } ] }
```
With ILM: a `downsample` action in warm/cold phase (`"downsample": { "fixed_interval": "1h" }`).
Manual: `POST my-tsds-backing-index/_downsample/target-index { "fixed_interval": "1h" }` on a read-only backing index.

With the default `aggregate` method, each downsampled doc holds, per time series and interval, `min`/`max`/`sum`/`value_count` for gauge fields (mapped to `aggregate_metric_double`) and the first value for cumulative counters (plus up to two points when a reset is detected, from 9.4). A `downsampling_method` of `last_value` (preview from 9.3) keeps only the most recent value and uses the least storage. A downsampled index can be downsampled again at an interval that is a multiple of the previous one.

## Gotchas
- Downsampling replaces raw data: raw points are gone for that interval.
- Fields that are not time series metrics or dimensions keep the most recent value in each bucket.

## Verify
`GET _data_stream/metrics-app-prod/_lifecycle/explain` shows rollover and retention times; storage per day (`_cat/indices/.ds-metrics-app-*?v&h=index,store.size`) drops after downsampling.

## Checked

Checked 2026-10-25 against elastic/docs-content and elastic/elasticsearch `main` (Stack 9.5/9.6 docs). Confirmed: default `cluster.lifecycle.default.rollover` value; `index.lifecycle.prefer_ilm` defaults to true; `downsampling` array with `after` and `fixed_interval` in the lifecycle; downsampling requires read-only data; per-metric-type downsampled values; searchable snapshot transition from 9.5. Removed the unconfirmed 8.14 version claims. The `_downsample` manual API form and `_cat` verify command were not re-checked.

Method: documentation only; no commands were run.
