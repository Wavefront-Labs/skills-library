---
id: computing-software.search-and-information-retrieval.elasticsearch-opensearch.bucket-script-derivative-aggs
name: bucket-script-derivative-aggs
category: computing-software
field: search-and-information-retrieval
product: elasticsearch-opensearch
tags: [search-and-information-retrieval, elasticsearch-opensearch, elasticsearch, opensearch, bucket-script-derivative-aggs, es-aggs-pipeline]
level: advanced
status: docs-checked
description: "Use derivative, cumulative_sum, moving_fn, bucket_script and bucket_selector over sibling or parent aggregations."
sources:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-pipeline.html
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-pipeline-derivative-aggregation.html
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-pipeline-bucket-script-aggregation.html
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-pipeline-movfn-aggregation.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Pipeline aggregations

**Goal:** rates and trends computed inside the query.
- Parent pipeline aggregations sit inside the multi-bucket aggregation and add to its buckets: `{"derivative":{"buckets_path":"sales"}}`, `bucket_script`, `bucket_selector`, `moving_fn` (its script calls functions from the `MovingFunctions` namespace, e.g. `MovingFunctions.unweightedAvg(values)`).
- Derivative needs a numeric metric and an enclosing histogram with `min_doc_count` 0 (the default for histograms); the first bucket has no derivative because two data points are needed. `unit` (for example `day`) adds `normalized_value`.
- Sibling pipeline aggregations sit next to the aggregation they read: `{"max_bucket":{"buckets_path":"sales_per_month>sales"}}`.
- `bucket_script` runs a script over several metrics via a map of variable names to paths (`params.my_var1 / params.my_var2`) and must return a numeric value; `bucket_selector` drops buckets whose script is false.
- `buckets_path` uses `>` between aggregation names and `.` before a metric property; `_count` reads the document count and `_bucket_count` (on a multi-bucket aggregation) the number of buckets. Paths are relative to the pipeline aggregation and cannot go back up the tree.
- Pipeline aggregations cannot have sub-aggregations but can be chained (derivative of a derivative).
- `gap_policy` (default `skip`) controls missing data; the other documented values are `insert_zeros` and `keep_values`.

## Verify
- [ ] The derivative of a known series matches differences computed by hand.

## Notes
- Try every request on a test index first; syntax and defaults differ between Elasticsearch and OpenSearch versions, so check the linked reference for yours.
- The pages cited are the Elasticsearch reference; the OpenSearch pipeline aggregation page could not be read, so OpenSearch behaviour is not covered here.

## Checked
2026-11-08. Confirmed against the Elasticsearch Pipeline, Derivative, Bucket script and Moving function pages: parent/sibling families, `buckets_path` syntax, `_count` and `_bucket_count`, derivative requirements and `unit`, `gap_policy` default and values, chaining. Removed the quoted `buckets_path must reference...` error text (not on the pages) and the "Painless" wording for `moving_fn`.
Method: documentation only; no commands were run.
