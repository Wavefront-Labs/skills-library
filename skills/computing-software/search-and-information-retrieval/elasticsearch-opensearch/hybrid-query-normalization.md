---
id: computing-software.search-and-information-retrieval.elasticsearch-opensearch.hybrid-query-normalization
name: hybrid-query-normalization
category: computing-software
field: search-and-information-retrieval
product: elasticsearch-opensearch
tags: [search-and-information-retrieval, elasticsearch-opensearch, elasticsearch, opensearch, hybrid-query-normalization]
level: advanced
status: docs-checked
description: "Run an OpenSearch hybrid query of BM25 and k-NN sub-queries with a normalization-processor to combine scores."
sources:
  - https://docs.opensearch.org/latest/query-dsl/compound/hybrid/
  - https://docs.opensearch.org/latest/search-plugins/search-pipelines/normalization-processor/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Hybrid query with score normalization

**Goal:** lexical plus vector ranking in OpenSearch.
- Pipeline: `{"phase_results_processors":[{"normalization-processor":{"normalization":{"technique":"min_max"},"combination":{"technique":"arithmetic_mean","parameters":{"weights":[0.3,0.7]}}}}]}`.
- Query: `POST my-index/_search?search_pipeline=<name>` with `{"query":{"hybrid":{"queries":[{"match":{"text":"q"}},{"knn":{"emb":{"vector":[...],"k":50}}}]}}}`. The knn clause shape comes from the k-NN docs, not checked here.
- `hybrid` must be a top-level query (not inside function_score, constant_score, script_score or boosting), takes 1 to 5 `queries`, and a document must match at least one. Optional `filter` applies to all sub-queries; `pagination_depth` (up to `index.max_result_window`) is required when `from` is above 0.
- Normalization `technique`: `min_max` (default; lowest score becomes 0.001), `l2`, or `z_score` (only works with `arithmetic_mean`). Combination `technique`: `arithmetic_mean` (default), `geometric_mean`, `harmonic_mean`.
- `weights`: floats in [0.0, 1.0], one per sub-query in query order, summing to 1.0; omitted means equal weight.
- `ignore_failure` has no effect on this processor: a failure fails the pipeline.
- Hybrid queries are enabled by default through the neural-search plugin; `plugins.neural_search.hybrid_search_disabled: true` in `opensearch.yml` turns them off.
- Failure mode: weights not summing to 1 or the count not matching the sub-queries.

## Verify
- [ ] Changing weights shifts ranking between lexical and vector hits as expected.

## Checked
Date: 2026-11-08
Method: Read the OpenSearch hybrid query and normalization processor pages in full (the latter in three fetched chunks); the knn sub-query syntax was not checked.
