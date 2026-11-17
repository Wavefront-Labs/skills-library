---
id: computing-software.search-and-information-retrieval.elasticsearch-opensearch.opensearch-knn-index-and-query
name: opensearch-knn-index-and-query
category: computing-software
field: search-and-information-retrieval
product: elasticsearch-opensearch
tags: [search-and-information-retrieval, elasticsearch-opensearch, elasticsearch, opensearch, opensearch-knn-index-and-query, os-knn]
level: advanced
status: docs-checked
description: "Create an OpenSearch index with index.knn true and a knn_vector field, run approximate knn queries, and understand k versus size, filters, engines and native memory."
sources:
  - https://raw.githubusercontent.com/opensearch-project/documentation-website/main/_vector-search/creating-vector-index.md
  - https://raw.githubusercontent.com/opensearch-project/documentation-website/main/_vector-search/vector-search-techniques/approximate-knn.md
  - https://raw.githubusercontent.com/opensearch-project/documentation-website/main/_query-dsl/specialized/k-nn/index.md
  - https://raw.githubusercontent.com/opensearch-project/documentation-website/main/_vector-search/api/knn.md
  - https://raw.githubusercontent.com/opensearch-project/documentation-website/main/_vector-search/vector-search-techniques/index.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OpenSearch k-NN index and query

**Goal:** vector similarity search in OpenSearch (the k-NN plugin).

## Create the index
```
PUT my-vectors
{"settings":{"index.knn":true},
 "mappings":{"properties":{"emb":{"type":"knn_vector","dimension":384,"space_type":"l2","method":{"name":"hnsw","engine":"faiss"}}}}}
```
- `index.knn: true` makes OpenSearch build native library indexes for the index. `knn_vector` holds floats by default; half-float, byte and binary vectors exist for smaller storage.
- `dimension` must equal the vector size you ingest (the model output size when embeddings are generated in a pipeline). The docs state a limit of 16,000 for the NMSLIB, Faiss and Lucene engines.
- `space_type` examples in the docs: `l2`, `cosinesimil`, `innerproduct`. Methods include HNSW and IVF; the docs also show a field-level `mode` of `on_disk` for compressed storage.
- The docs examples use `faiss` and `lucene`; `nmslib` is marked deprecated. A model-based (trained) field needs the Train API first.

## Query
```
GET my-vectors/_search
{"size":10,"query":{"knn":{"emb":{"vector":[...],"k":10}}}}
```
- `k` is not the same as `size`. For Faiss and NMSLIB, `k` is the maximum documents returned per segment of a shard; for Lucene it is per shard. Maximum `k` is 10,000. Each shard returns `size` results to the coordinating node, so set `size` to what you want returned.
- Instead of `k` you can use `min_score` or `max_distance` (radial search).
- A query `filter` works only with the `faiss` or `lucene` engines. For the native-library ANN method the docs say filters are applied to the ANN results, because the graphs are built at indexing time. For small data sets where you want pre-filtering, the docs point to the scoring-script (exact) method.

## Memory and operations
- Native library indexes are loaded into native memory (not heap) on first search and managed by a cache. `GET _plugins/_knn/stats` shows `graph_memory_usage` (KB) and `graph_memory_usage_percentage` per node.
- The warmup API preloads them to avoid slow first queries; it works for `faiss` and `nmslib` indexes only and has no effect on `lucene` indexes. Make sure the indexes fit in native memory first or the cache thrashes.
- The docs recommend approximate search once a data set reaches hundreds of thousands of vectors.

## Verify
- [ ] A stored vector queried with `k` 1 returns itself.
- [ ] `_plugins/_knn/stats` shows graph memory growing after the first query (faiss) and stays below the circuit-breaker limit.

## Checked
2026-11-08. Confirmed from the OpenSearch documentation source pages on creating a vector index, approximate k-NN search, the knn query, the k-NN API (stats, warmup) and vector search techniques: `index.knn`, field options, 16,000 dimension limit, `k` semantics and the 10,000 maximum, filter engine restriction, native memory behaviour, stats fields, warmup scope. Removed: the statement that `lucene` is the default or that engine availability follows version (not stated as such), the unqualified "filtering supported with some engines" wording, and generic notes.
Method: documentation only; no commands were run.
