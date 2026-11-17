---
id: computing-software.search-and-information-retrieval.qdrant.query-api-basics
name: query-api-basics
category: computing-software
field: search-and-information-retrieval
product: qdrant
tags: [query-api, nearest-neighbour, limit, search, search-query]
level: intro
status: docs-checked
description: "Run nearest-neighbour search through the Qdrant Query API with limit, offset, score_threshold, using, hnsw_ef and exact."
sources:
  - https://qdrant.tech/documentation/search/search/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

The Query API (available as of v1.10.0) is the single interface for search and exploration requests.

```http
POST /collections/{collection_name}/points/query
{
  "query": [0.2, 0.1, 0.9, 0.7],
  "limit": 3,
  "with_payload": true
}
```

Query types listed in the docs: nearest neighbours, search by id, full-text (BM25), recommendations, discovery, scroll, grouping, order by, hybrid, multi-stage, score boosting, maximal marginal relevance, relevance feedback and random sampling.

Common parameters:

- `limit` (alias `top`) is the number of most similar results to return.
- `offset` skips the first results (see the pagination skill); large offsets cost more.
- `score_threshold` excludes results with a worse score. Whether this removes lower or higher numbers depends on the metric (for Euclidean, higher scores are more distant and are excluded).
- `params.hnsw_ef` sets the `ef` parameter of the HNSW algorithm.
- `params.exact: true` skips approximate search and does a full scan, which can run for a long time.
- `params.indexed_only` skips segments where the vector index is not built yet; results may be partial, so use it only if eventual consistency is acceptable.
- `using` selects a named vector.
- `filter` restricts candidates by payload.
- `with_payload` and `with_vectors` control what is returned; by default no payload or vectors are returned.

Pass a point id as `query` instead of a vector to use that point's stored vector as the query (this skips embedding inference). With `using`, the named vector is used; `lookup_from` can take the vector from another collection, and it must match the characteristics of the `using` vector or an error is returned.

Use `exact` only on small collections or for measuring recall.

The same endpoint accepts `prefetch` stages, which is how hybrid, multi-stage and score-boosting queries are built.

## Checked

2026-11-08. Confirmed against the Similarity Search page (query-type table, `limit`/`top`, `hnsw_ef`, `exact`, `indexed_only`, `score_threshold`, `with_vectors`/`with_payload` defaults, query by id, `using`, `lookup_from`; v1.10.0). Page read by section, not every client-language code tab. Corrected: REST field is `with_vectors`, not `with_vector`. Removed: a claim that prefetch is introduced on this page, and the hybrid/prefetch details (covered by other skills).
Method: documentation only; no commands were run.
