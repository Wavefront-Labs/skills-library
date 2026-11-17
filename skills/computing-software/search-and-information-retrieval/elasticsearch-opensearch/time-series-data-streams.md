---
id: computing-software.search-and-information-retrieval.elasticsearch-opensearch.time-series-data-streams
name: time-series-data-streams
category: computing-software
field: search-and-information-retrieval
product: elasticsearch-opensearch
tags: [search-and-information-retrieval, elasticsearch-opensearch, elasticsearch, opensearch, time-series-data-streams]
level: advanced
status: docs-checked
description: "Configure index.mode time_series with dimensions and metrics for metrics data in Elasticsearch."
sources:
  - https://www.elastic.co/docs/manage-data/data-store/data-streams/time-series-data-stream-tsds
  - https://www.elastic.co/docs/manage-data/data-store/data-streams/set-up-tsds
  - https://www.elastic.co/docs/manage-data/data-store/data-streams/time-bound-tsds
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Time series data streams (TSDS)

**Goal:** compact storage for metrics.
- The matching index template must include a `data_stream` object with `index.mode` set to `time_series`. Mark dimension fields with `"time_series_dimension": true` and metric fields with `time_series_metric` (`counter`, `gauge` or `histogram`).
- Routing uses the dimension fields so all data points of one time series go to the same shard. The set-up page also shows `index.routing_path` in the component template, with its fields marked as dimensions; the Time bound page describes a newer automatic `index.dimensions` strategy and `index.routing_path` as a fallback or manual setting, so check which applies to your version.
- A backing index accepts only `@timestamp` values inside its window: from `now` minus `index.look_back_time` (inclusive, stored in `index.time_series.start_time`) to `now` plus `index.look_ahead_time` (exclusive, `index.time_series.end_time`). If no backing index can accept a timestamp, the document is rejected; future timestamps and those outside the window are still rejected.
- Elasticsearch generates the document `_id` from the dimensions and timestamp, so two documents with the same dimensions and timestamp are duplicates; duplicates are rejected with `409 Conflict`.

## Verify
- [ ] Index two documents with the same dimensions and timestamp; the second is rejected.

## Scope
The Elasticsearch documentation was checked; OpenSearch behaviour was not.

## Checked

Checked 2026-11-02 against the Elasticsearch docs pages Time series data streams, Set up a TSDS and Time bound TSDS. Confirmed: all statements above. Removed: the claim that OpenSearch has no equivalent, and the OpenSearch source root. Corrected: `index.routing_path` is no longer the only routing mechanism.

Method: documentation only; no commands were run.
