---
id: computing-software.database-administration.elasticsearch.knn-vector-search-and-hybrid-ranking
name: knn-vector-search-and-hybrid-ranking
category: computing-software
field: database-administration
product: elasticsearch
tags: [database-administration, elasticsearch, query-dsl, knn-search, dense-vector, hnsw, rrf, hybrid-search, quantization]
level: practitioner
status: verified
description: "Run approximate kNN search on Elasticsearch dense_vector fields: mapping and quantization, k and num_candidates, filtered kNN, and hybrid BM25 plus vector ranking with RRF."
sources:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/knn-search.html
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/dense-vector.html
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/rrf.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# kNN vector search and hybrid ranking

## Mapping
```json
PUT docs
{ "mappings": { "properties": {
  "title":     { "type": "text" },
  "tenant":    { "type": "keyword" },
  "embedding": { "type": "dense_vector", "dims": 768, "index": true, "similarity": "cosine",
                 "index_options": { "type": "int8_hnsw", "m": 16, "ef_construction": 100 } }
} } }
```
- `similarity`: `cosine`, `dot_product` (vectors must be unit length: `[3.0, 4.0]` was rejected, `[0.6, 0.8]` accepted), `l2_norm`, `max_inner_product`.
- `index_options.type`: `hnsw` (float), `int8_hnsw` (about 4x less memory), `int4_hnsw`, `bbq_hnsw` (binary quantization), and `flat`, `int8_flat`, `int4_flat`, `bbq_flat` for brute force; all of these were accepted on 9.5.5.
- If you omit `index_options` for float vectors the default depends on dimensions: `bbq_hnsw` at 384 dimensions or more, `int8_hnsw` below (confirmed on 9.5.5 with 768 and 4 dims; the docs also describe `bbq_disk` as the default where the licence allows).
- HNSW graphs must fit in the **filesystem cache** (off-heap) for good latency; size RAM for
  vectors (quantized size x docs) plus overhead.

## Query
```json
POST docs/_search
{ "knn": { "field": "embedding", "query_vector": [0.12, ...], "k": 10, "num_candidates": 100,
           "filter": { "term": { "tenant": "acme" } } },
  "_source": ["title"] }
```
- `num_candidates` per shard controls recall vs latency (start ~10x k).
- `filter` is applied **during** the HNSW search (pre-filtering), so you still get k results.
- `query_vector_builder` (`text_embedding` with a `model_id` of a deployed model or inference endpoint) computes the vector server-side; an unknown model id returns a 404 status_exception.

## Hybrid search (lexical + vector)
Reciprocal Rank Fusion via retrievers. RRF is a licensed feature: on the Basic licence the request returned 403 "current license is non-compliant for [Reciprocal Rank Fusion (RRF)]"; it ran after starting a trial licence:
```json
POST docs/_search
{ "retriever": { "rrf": {
    "retrievers": [
      { "standard": { "query": { "match": { "title": "reset password" } } } },
      { "knn": { "field": "embedding", "query_vector": [...], "k": 50, "num_candidates": 200 } }
    ],
    "rank_window_size": 50, "rank_constant": 60 } } }
```
RRF combines rankings without needing comparable scores. Alternative: a linear combination
(`knn` + `query` with boosts) when scores are calibrated.

## Operations
- Bulk load with `refresh_interval: -1` and replicas 0, then restore; HNSW building is CPU heavy.
- Force merge read-only indices to few segments: each segment has its own graph, and searching
  many segments is slower.
- Measure recall against exact search (`script_score` with `cosineSimilarity` on a sample).

## Verify
Profile (`"profile": true`) shows the `DenseVectorQuery`/knn phase; latency at target recall
is acceptable, and node memory stats show vector data served from page cache (low disk reads).
