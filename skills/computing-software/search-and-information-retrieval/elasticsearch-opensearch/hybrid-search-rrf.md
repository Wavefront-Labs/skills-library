---
id: computing-software.search-and-information-retrieval.elasticsearch-opensearch.hybrid-search-rrf
name: hybrid-search-rrf
category: computing-software
field: search-and-information-retrieval
product: elasticsearch-opensearch
tags: [search-and-information-retrieval, elasticsearch-opensearch, elasticsearch, opensearch, hybrid-search-rrf]
level: advanced
status: docs-checked
description: "Combine BM25 and kNN results with the Elasticsearch rrf retriever; OpenSearch uses a hybrid query with a normalization processor instead."
sources:
  - https://www.elastic.co/docs/reference/elasticsearch/rest-apis/reciprocal-rank-fusion
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Hybrid search with reciprocal rank fusion

**Goal:** lexical plus semantic ranking.
- Elasticsearch: `"retriever":{"rrf":{"retrievers":[{"standard":{"query":{"match":{"body":"q"}}}},{"knn":{"field":"emb","query_vector":[...],"k":50,"num_candidates":200}}],"rank_window_size":50,"rank_constant":60}}`.
- RRF scores each document as the sum of `1 / (rank_constant + rank)` over every result set that contains it (rank starts at 1). It needs no tuning and the signals need not be related.
- At least two child retrievers are required; each has equal weight.
- `rank_constant` defaults to 60 (minimum 1; higher values give lower-ranked documents more influence). `rank_window_size` defaults to the request `size`, must be at least `size` and 1; larger improves relevance but costs performance.
- Supported with rrf: aggregations, `from`, suggesters, highlighting, collapse, profiling. Not supported: scroll, sort, rescore (they raise an exception). Do not pass a point in time; RRF creates one internally.
- OpenSearch has no rrf retriever in this scheme: use a `hybrid` query with a search pipeline normalization processor (see the hybrid-query-normalization skill).

## Verify
- [ ] A judged query set shows hybrid beats either alone on your data.

## Checked
Date: 2026-11-08
Method: Read the Elasticsearch reciprocal rank fusion page in full; the knn retriever parameters in the example were not separately checked. OpenSearch was not checked here.
