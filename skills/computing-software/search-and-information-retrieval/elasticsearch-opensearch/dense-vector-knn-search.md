---
id: computing-software.search-and-information-retrieval.elasticsearch-opensearch.dense-vector-knn-search
name: dense-vector-knn-search
category: computing-software
field: search-and-information-retrieval
product: elasticsearch-opensearch
tags: [search-and-information-retrieval, elasticsearch-opensearch, elasticsearch, opensearch, dense-vector-knn-search, es-vector-search]
level: advanced
status: docs-checked
description: "Map a dense_vector field, index embeddings and run approximate kNN search with k, num_candidates and filters."
sources:
  - https://www.elastic.co/docs/reference/elasticsearch/mapping-reference/dense-vector
  - https://www.elastic.co/docs/solutions/search/vector/knn
  - https://www.elastic.co/docs/solutions/search/vector/knn/approximate-knn
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Elasticsearch dense_vector and knn search

**Goal:** nearest-neighbour retrieval on embeddings.
```
"mappings":{"properties":{"emb":{"type":"dense_vector","dims":384,"index":true,"similarity":"cosine"}}}
GET my-index/_search {"knn":{"field":"emb","query_vector":[...],"k":10,"num_candidates":100,"filter":{"term":{"lang":"en"}}}}
```
- Query vectors must have the same dimension and come from the same model as the document vectors; a `lookup` query vector's dimensions must match the field searched.
- `similarity` defaults to `cosine` (to `l2_norm` for `element_type: bit`, which supports only `l2_norm`); `dot_product` and `l2_norm` are the other options shown on the page. Indexing is enabled by default for `dense_vector`.
- `knn` takes `k` and `num_candidates`, and an optional `filter` inside the `knn` object (the page's example excludes a document with a `bool`/`must_not` filter). The page excerpts read do not explain the `num_candidates` recall/latency trade-off or `post_filter` behaviour, so test both on your data.
- `dense_vector` fields are not returned in `_source` in responses by default.
- Vectors can come from `semantic_text`, the Elastic Inference Service, a model on an ML node, or be generated outside the cluster; keep the model name and version recorded.
- OpenSearch uses a different field type (`knn_vector`); it was not checked here.

## Verify
- [ ] Query with a stored document's own vector returns it first.

## Notes
- Try every request on a test index first; syntax and defaults differ between Elasticsearch and OpenSearch versions, so check the linked reference for yours.

## Checked
2026-11-08. Read the Elasticsearch dense_vector page (similarity default and options, indexing default, `_source` behaviour; partly, via targeted search), the kNN search overview and the Approximate kNN page (a short page). Removed the `num_candidates` trade-off, the `post_filter` claim and the indexing-error claim, which were not on the pages read. The OpenSearch k-NN vector field page returned only a stub, so OpenSearch is unverified.
Method: documentation only; no commands were run.
