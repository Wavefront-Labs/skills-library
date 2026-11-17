---
id: computing-software.search-and-information-retrieval.elasticsearch-opensearch.stats-and-percentiles-aggs
name: stats-and-percentiles-aggs
category: computing-software
field: search-and-information-retrieval
product: elasticsearch-opensearch
tags: [search-and-information-retrieval, elasticsearch-opensearch, elasticsearch, opensearch, stats-and-percentiles-aggs, es-aggs-metrics]
level: practitioner
status: docs-checked
description: "Use the stats and percentiles aggregations: defaults, TDigest vs HDR accuracy trade-offs, compression, missing values and script-based values."
sources:
  - https://www.elastic.co/docs/reference/aggregations/search-aggregations-metrics-percentile-aggregation
  - https://www.elastic.co/docs/reference/aggregations/search-aggregations-metrics-stats-aggregation
  - https://raw.githubusercontent.com/opensearch-project/documentation-website/main/_aggregations/metric/percentile.md
  - https://raw.githubusercontent.com/opensearch-project/documentation-website/main/_aggregations/metric/stats.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Stats and percentiles aggregations

**Goal:** numeric summaries per query or bucket, with an honest view of how approximate they are. Both Elasticsearch and OpenSearch document the same request shapes below.

## stats
- `GET my-index/_search {"size":0,"aggs":{"s":{"stats":{"field":"latency_ms"}}}}` returns `count`, `min`, `max`, `avg` and `sum` together.
- `field` must be numeric. A `script` (OpenSearch) or a runtime field (Elasticsearch) can supply derived values. `missing` sets a value for documents without the field; by default they are ignored.
- `size: 0` keeps hits out of the response when you only need aggregations.

## percentiles
- `{"percentiles":{"field":"latency_ms","percents":[50,95,99]}}`. Each value must be between 0 and 100 inclusive. The default set is 1, 5, 25, 50, 75, 95, 99.
- `keyed: false` returns an array of `{key, value}` instead of an object (default is keyed).
- Results are approximate and the docs say they can differ slightly between runs on the same data. Accuracy is proportional to q(1-q), so extreme percentiles (99th) are more accurate than the median. Small data sets are exact or close to it; the error with large data depends on distribution and volume.
- Default algorithm is TDigest. `tdigest.compression` defaults to `100`: more compression means better accuracy, more memory and slower. Elasticsearch documents that the node count is capped at 20 x compression, roughly 32 bytes per node (about 64KB worst case at the default), and an `execution_hint` of `high_accuracy` that costs 2x-10x the time.
- Alternative: `hdr` with `number_of_significant_value_digits` (default 3, valid 0-5 in OpenSearch). Choose one of `tdigest` or `hdr`, not both. HDR supports non-negative values only and is a poor choice when the value range is unknown (high memory use). OpenSearch describes HDR as faster but using more memory than TDigest.
- `missing`: documents without the field are ignored unless you set a value. A script that reads `doc['f'].value` fails on documents missing the field; check `doc['f'].size() == 0` first.

## Verify
- [ ] Compare `percentiles` against an exact calculation on a small subset: on small data they should match.
- [ ] Repeat the same query twice and expect tiny differences on large data.

## Checked
2026-11-08. Confirmed from the Elasticsearch and OpenSearch documentation pages for the stats and percentiles aggregations: returned stats, defaults for `percents`, `keyed` and `compression`, q(1-q) accuracy statement, non-determinism, node cap and memory estimate, `high_accuracy` cost, HDR digits and limits. Removed: the claim that aggregating a text field fails (no page read states it), `percentile_ranks` and extended stats (their pages were not read), and generic notes.
Method: documentation only; no commands were run.
