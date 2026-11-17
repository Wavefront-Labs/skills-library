---
id: computing-software.database-administration.elasticsearch.bucket-and-metric-aggregations
name: bucket-and-metric-aggregations
category: computing-software
field: database-administration
product: elasticsearch
tags: [database-administration, elasticsearch, query-dsl, elasticsearch-aggregations, terms-aggregation, date-histogram, composite-aggregation, cardinality, percentiles, shard-size, doc-count-error]
level: practitioner
status: verified
description: "Build Elasticsearch analytics with terms, date_histogram, composite, cardinality and percentiles aggregations, and avoid the accuracy and memory traps."
sources:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations.html
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-bucket-terms-aggregation.html
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-bucket-composite-aggregation.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Bucket and metric aggregations

**Goal:** dashboards and reports from Elasticsearch that are fast and correctly understood.

## Typical request
```json
GET logs-*/_search
{ "size": 0,
  "query": { "range": { "@timestamp": { "gte": "now-24h" } } },
  "aggs": {
    "per_hour": { "date_histogram": { "field": "@timestamp", "fixed_interval": "1h", "time_zone": "Australia/Sydney" },
      "aggs": {
        "p95_latency": { "percentiles": { "field": "latency_ms", "percents": [95, 99] } },
        "top_services": { "terms": { "field": "service.keyword", "size": 5 } },
        "uniq_users": { "cardinality": { "field": "user.id", "precision_threshold": 3000 } }
      } } } }
```
`size: 0` skips hits; aggregations run over all matched docs.

## Terms accuracy
Each shard returns its top `shard_size` (default `size * 1.5 + 10`) terms; merged counts can be wrong or miss terms. Response shows `doc_count_error_upper_bound` and `sum_other_doc_count`. Raise `shard_size` for accuracy, or use one shard for small indexes. Never `size: 10000` to "get all terms".

## All buckets: composite
```json
"aggs": { "all_services": { "composite": { "size": 1000,
  "sources": [ { "svc": { "terms": { "field": "service.keyword" } } }, { "day": { "date_histogram": { "field": "@timestamp", "calendar_interval": "1d" } } } ] } } }
```
Page with `"after": <after_key from the response>`.

## Metrics
- `cardinality` is HyperLogLog++: approximate; near-exact below `precision_threshold` (default 3000; maximum supported 40000, higher values act as 40000).
- `percentiles` (TDigest) approximate; `hdr` option for fixed precision.
- `avg`, `sum`, `min`, `max`, `stats`, `extended_stats`, `value_count`, `top_hits`, `top_metrics`.
- Pipeline aggs: `derivative`, `cumulative_sum`, `bucket_sort`, `bucket_selector`, `moving_fn`.

## Memory and speed
- Aggregate on `keyword`/numeric/date fields (doc values); `text` fields need fielddata (heap explosion: leave disabled).
- High-cardinality terms with deep sub-aggregations create millions of buckets: `search.max_buckets` (65,536) rejects them.
- `execution_hint: map` for small filtered sets; `"eager_global_ordinals": true` on a keyword mapping builds global ordinals at refresh.
- The shard request cache serves repeated `size: 0` aggregation requests (`GET <index>/_stats/request_cache` shows `hit_count`).

## Verify
For a known period, `terms` counts with large `shard_size` match a `_count` query per term; `doc_count_error_upper_bound` is 0.
