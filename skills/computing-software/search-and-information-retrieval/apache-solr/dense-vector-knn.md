---
id: computing-software.search-and-information-retrieval.apache-solr.dense-vector-knn
name: dense-vector-knn
category: computing-software
field: search-and-information-retrieval
product: apache-solr
tags: [dense-vector, knn-query, hnsw, vector-search, densevectorfield]
level: advanced
status: docs-checked
description: "Do vector search in Solr: DenseVectorField with vectorDimension and similarityFunction, HNSW settings, the knn and vectorSimilarity parsers, preFilter, topK and quantized fields."
sources:
  - https://solr.apache.org/guide/solr/latest/query-guide/dense-vector-search.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# dense-vector-knn

Embeddings are produced outside Solr. Declare `<fieldType name="knn_vector" class="solr.DenseVectorField" vectorDimension="4" similarityFunction="cosine"/>` and a field using it.

Properties: `vectorDimension` (required), `similarityFunction` (`euclidean` default, `cosine`, `dot_product`), `knnAlgorithm` (`hnsw` default, `flat`, `cagra_hnsw` with GPU), `hnswM`, `hnswEfConstruction` (need the schema codec factory), `vectorEncoding`. Prefer normalizing vectors to unit length and using `dot_product`; Solr's cosine scores are normalized as (1 + cosine) / 2. Quantized types: `ScalarQuantizedDenseVectorField` (FLOAT32 only) and `BinaryQuantizedDenseVectorField` (no `flat`).

Query parsers:
- `{!knn f=vector topK=10}[1.0, 2.0, 3.0, 4.0]` returns the nearest k.
- `{!vectorSimilarity}` matches all documents above a minimum similarity.
- `{!knn_text_to_vector model=a-model f=vector topK=10}text` encodes text with a configured model.

Tuning: `preFilter` (explicit) or implicit pre-filtering from `fq`, tag-based `includeTags` and `excludeTags`, `efSearchScaleFactor`, `earlyTermination`, `seedQuery`, `filteredSearchThreshold`.

Nested vectors use `childrenOf` and `parents.preFilter`.

## Checked

2026-11-04. Confirmed against the Dense Vector Search page: field type properties, the three query parsers including the `knn_text_to_vector` example, pre-filtering and tuning parameters, quantized field types. Nothing removed.

Method: documentation only; no commands were run.
