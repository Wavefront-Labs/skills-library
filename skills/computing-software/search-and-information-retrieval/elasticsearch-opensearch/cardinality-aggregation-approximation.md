---
id: computing-software.search-and-information-retrieval.elasticsearch-opensearch.cardinality-aggregation-approximation
name: cardinality-aggregation-approximation
category: computing-software
field: search-and-information-retrieval
product: elasticsearch-opensearch
tags: [search-and-information-retrieval, elasticsearch-opensearch, elasticsearch, opensearch, cardinality-aggregation-approximation]
level: advanced
status: docs-checked
description: "Count distinct values with cardinality (HyperLogLog++) and set precision_threshold knowing it is approximate."
sources:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-metrics-cardinality-aggregation.html
  - https://docs.opensearch.org/latest/aggregations/metric/cardinality/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cardinality (distinct count) aggregation

**Goal:** unique counts without huge memory.
- `{"aggs":{"users":{"cardinality":{"field":"user_id","precision_threshold":3000}}}}`.
- `precision_threshold` trades memory for accuracy: counts below it are expected to be close to accurate (not guaranteed), above it they get fuzzier. Default 3000, maximum 40000 (higher values behave as 40000).
- It is based on HyperLogLog++; memory depends only on the configured precision, not on the number of distinct values. Elasticsearch's example shows error of roughly 1-6% even with a threshold of 100 on millions of items.
- Failure mode: assuming exact counts for billing or compliance; use a composite aggregation or an external system for exact numbers.

## Verify
- [ ] Compare with a composite-aggregation exact count on a day of data.

## Notes
- Try every request on a test index first; syntax and defaults differ between Elasticsearch and OpenSearch versions, so check the linked reference for yours.

## Checked
2026-11-08. Read the Elasticsearch and OpenSearch cardinality aggregation pages: approximate count, HyperLogLog++, `precision_threshold` default 3000 and maximum 40000, fixed memory. Replaced "memory proportional to the threshold" and the vague error wording with the figures on the pages.
Method: documentation only; no commands were run.
