---
id: computing-software.search-and-information-retrieval.qdrant.hybrid-rrf-prefetch
name: hybrid-rrf-prefetch
category: computing-software
field: search-and-information-retrieval
product: qdrant
tags: [hybrid-search, prefetch, rrf, fusion, rel-hybrid]
level: advanced
status: docs-checked
description: "Fuse dense, sparse and BM25 results in Qdrant with prefetch and reciprocal rank fusion (RRF, k and weights) or DBSF, and size prefetch limits."
sources:
  - https://qdrant.tech/documentation/search/hybrid-queries/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Hybrid and multi-stage queries (available as of v1.10.0) are built on the `prefetch` parameter: when a query has at least one prefetch, Qdrant runs the prefetch queries, then applies the main query to their results. Prefetches can themselves have prefetches.

```json
{
  "prefetch": [
    { "query": { "text": "time travel" }, "using": "title", "limit": 20 },
    { "query": [0.01, 0.45, 0.67], "using": "dense", "limit": 20 }
  ],
  "query": { "rrf": {} },
  "limit": 10
}
```

Points from the docs:

- Fusion methods are `rrf` and `dbsf`.
- RRF scores a document as the sum of 1/(k + rank) over each result list, using zero-based ranks; `k` defaults to 2. It uses ranks, not raw scores, so different score scales do not matter.
- Set the constant with `{ "rrf": { "k": 60 } }` (as of v1.16.0).
- Weighted RRF (as of v1.17.0): `{ "rrf": { "weights": [3.0, 1.0] } }`, one weight per prefetch in order, count must match. Without an evaluation set, leave the weights at the default of 1.0.
- DBSF: `{ "fusion": "dbsf" }` keeps raw scores but normalizes each retriever's distribution (mean and 3-sigma extremes) before combining; it is stateless and does not clip to 0..1. With no evaluation set and no strong score priors the docs call RRF the safe default; DBSF suits trust in raw scores.
- `offset` only affects the main query, so each prefetch `limit` must be at least the main `limit` plus `offset`, otherwise results can be empty.
- Fusion placed inside a prefetch of a multi-shard collection is computed per shard on local results; to fuse across all shards, make it the top-level `query` with the retrievers as its prefetches.
- A weighted linear combination of raw dense and BM25 scores is unreliable because the scales differ; use RRF or DBSF instead.
- Multi-stage example: prefetch candidates with a cheap query, then re-score with a more accurate one such as a multivector.

## Checked

2026-11-08. Confirmed against the Hybrid and Multi-Stage Queries page: prefetch semantics, RRF formula, defaults, `k` and weights with version gates, DBSF, shard note, offset rule, multi-stage section headings. Page read by section (hybrid, RRF, DBSF and notes); client-language tabs skipped. Source changed from the Search Relevance page, which does not cover fusion. Removed unconfirmed claims: prefetch limits of 100 to 200 as tuning-page guidance, `"fusion": "rrf"` as default syntax, per-prefetch filters, and the reranker advice.
Method: documentation only; no commands were run.
