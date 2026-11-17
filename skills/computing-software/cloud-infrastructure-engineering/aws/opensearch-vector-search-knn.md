---
id: computing-software.cloud-infrastructure-engineering.aws.opensearch-vector-search-knn
name: opensearch-vector-search-knn
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, opensearch, vector-search, knn, hnsw, faiss, semantic-search, embeddings]
level: practitioner
status: draft
description: "Vector search on Amazon OpenSearch: knn_vector mappings, HNSW parameters and engines, filtered k-NN, quantisation and memory sizing, and neural search with Bedrock embeddings."
sources: ["OpenSearch documentation - k-NN search and k-NN index", "OpenSearch documentation - Approximate k-NN (methods and engines)", "Amazon OpenSearch Service Developer Guide - Vector search and k-NN", "OpenSearch documentation - Neural search and ML connectors"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# OpenSearch vector search (k-NN)

## Index mapping
```json
PUT products
{"settings":{"index":{"knn":true,"number_of_shards":2,"number_of_replicas":1}},
 "mappings":{"properties":{
   "embedding":{"type":"knn_vector","dimension":1024,
     "method":{"name":"hnsw","engine":"faiss","space_type":"innerproduct",
               "parameters":{"m":16,"ef_construction":256}}},
   "category":{"type":"keyword"},"title":{"type":"text"}}}}
```
- `dimension` must match the embedding model (e.g. 1024 for Titan Text Embeddings v2 default, 1536 for some others).
- `space_type`: `l2`, `cosinesimil`, `innerproduct` (use with normalised vectors).
- Engines: `faiss` (recommended, supports quantisation and efficient filtering), `lucene` (good filtering, smaller scale), `nmslib` (deprecated for new indices).

## Query
```json
GET products/_search
{"size":10,"query":{"knn":{"embedding":{"vector":[0.01,0.02],"k":10,
  "filter":{"term":{"category":"shoes"}}}}}}
```
- Efficient filtering (faiss/lucene) applies the filter during search rather than after, so you still get k results.
- `ef_search` (index setting `knn.algo_param.ef_search`, or method parameter) trades latency for recall.
- Hybrid search: combine `knn` with BM25 `match` using a search pipeline with a normalization processor.

## Memory sizing (HNSW, float32)
Approximate native memory: `1.1 x (4 x dimension + 8 x m) x vectors` bytes. 10 M vectors x 1024 dims, m=16:
~1.1 x (4096 + 128) x 10 M = ~46 GB, plus replicas. Graphs must fit in the k-NN memory circuit breaker
(a share of off-heap RAM): choose instances accordingly or reduce with quantisation:
- faiss scalar quantisation (fp16) halves memory; byte vectors quarter it; binary quantisation / disk-based mode (`mode: on_disk`, compression levels) cuts much further with rescoring.

## Neural search with Bedrock
- Create an ML connector to Bedrock embeddings, register and deploy the model, then an ingest pipeline with `text_embedding` processor so documents are embedded at index time; `neural` queries embed the query text.
- Or embed in your application and index vectors directly (simpler to reason about).
- OpenSearch Serverless offers a **vector search** collection type for managed scaling.

## Verify
- [ ] Recall measured against exact k-NN on a sample (target > 0.95) at the chosen ef_search.
- [ ] k-NN stats (`GET _plugins/_knn/stats`) show graph memory under the circuit breaker limit.
