---
id: computing-software.cloud-infrastructure-engineering.cortex.ruler-evaluates-rules-via-query-frontend
name: ruler-evaluates-rules-via-query-frontend
category: computing-software
field: cloud-infrastructure-engineering
product: cortex
tags: [ruler, query-frontend, rule-evaluation, protobuf, experimental]
level: advanced
status: docs-checked
description: "Point the Cortex ruler at the query frontend for rule evaluation and adjust response format and stats tracking."
sources:
  - https://github.com/cortexproject/cortex/blob/master/docs/guides/rule-evaluations-via-query-frontend.md
  - https://github.com/cortexproject/cortex/blob/master/docs/configuration/v1-guarantees.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
By default the ruler queries ingesters and the store-gateway directly, depending on the rule's time range. Setting `-ruler.frontend-address` makes it query the Query Frontend instead. The address is the frontend's gRPC listen address in host:port form:

```
-ruler.frontend-address=query-frontend.svc.cluster.local:9095
```

or in YAML `ruler.frontend_address`. The gRPC client from ruler to frontend is tuned in the `frontend_client` section of the ruler config.

`-ruler.query-response-format` chooses how results come back: `protobuf` (default, recommended, because native histograms are only supported on protobuf) or `json`.

Tracking: with a frontend address set, query stats in ruler logs and metrics are all 0. Enable `-frontend.enabled-ruler-query-stats` (off by default) to log them at the frontend. Use alternative metrics: `cortex_ruler_query_seconds_total` becomes `cortex_query_seconds_total{source="ruler"}`.

The query path becomes Ruler, Query Frontend, Query Scheduler, Querier, then Ingester or Store Gateway: more hops. Pros: with enough queriers pulling from the scheduler, evaluation can be faster (frontend features such as vertical query sharding apply) and the ruler needs fewer resources because it runs no query engine. Con: with too few queriers, rule queries can starve in the scheduler queue so rules are not evaluated in time. The guide suggests watching `cortex_prometheus_rule_evaluation_duration_seconds` to decide whether to use `-ruler.frontend-address`.

The other relocated metrics are `cortex_ruler_samples_total`, `cortex_ruler_fetched_chunks_bytes_total` and `cortex_ruler_fetched_data_bytes_total`, which become `cortex_query_samples_total`, `cortex_query_fetched_chunks_bytes_total` and `cortex_query_fetched_data_bytes_total` with `source="ruler"`; `cortex_ruler_fetched_series_total` becomes `cortex_query_fetched_series_total{source="ruler"}`.

## Checked

Method: docs-checked 2026-11-09 against the Cortex rule evaluations via query frontend guide (raw markdown, read in full). The guide itself does not call the feature experimental; the Cortex v1 guarantees page lists it, with `-ruler.query-response-format`, as experimental, so expect no backward compatibility promise.
