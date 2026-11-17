---
id: computing-software.search-and-information-retrieval.qdrant.sparse-vectors
name: sparse-vectors
category: computing-software
field: search-and-information-retrieval
product: qdrant
tags: [sparse-vectors, indices, values, idf, vec-sparse]
level: practitioner
status: docs-checked
description: "Store and search sparse vectors as index and value arrays, with the IDF modifier for BM25-style weighting."
sources:
  - "https://qdrant.tech/documentation/search/text-search/sparse-vector-search/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Sparse vectors have no fixed length. They are given as two equal-length arrays: `indices` of the non-zero dimensions and `values` for them.

```http
PUT /collections/docs
{
  "sparse_vectors": {
    "text": { "modifier": "idf" }
  }
}
```

```json
{ "id": 1, "vector": { "text": { "indices": [6, 7], "values": [1.0, 2.0] } } }
```

Facts from the docs:

- Sparse vectors must be named and live under `sparse_vectors` in the collection config.
- The number of non-zero entries is limited by the u32 range.
- The `idf` modifier configures the vector for queries that use inverse document frequency; by default the statistics are computed over all data in the shard being queried.
- The docs describe a more compact immutable sparse index built during the same optimization process as the dense vector index.

Search them with `using` set to the sparse vector name:

```json
{ "query": { "indices": [6, 7], "values": [1.0, 1.0] }, "using": "text", "limit": 10 }
```

SPLADE++, miniCOIL and BM25 produce these vectors. The docs recommend running BM25 on a full-text index rather than on sparse vectors; SPLADE++ cannot match terms outside its fixed vocabulary, such as product IDs.

## Checked

2026-11-03. Confirmed on the Qdrant sparse-vector search and vectors pages: u32 limit on non-zero values, `modifier: idf` and per-shard statistics, immutable sparse index, model families and the BM25 recommendation. Removed the unconfirmed 'stored separately' claim.

Method: documentation only; no commands were run.
