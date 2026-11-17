---
id: computing-software.search-and-information-retrieval.elasticsearch-opensearch.rescore-top-window
name: rescore-top-window
category: computing-software
field: search-and-information-retrieval
product: elasticsearch-opensearch
tags: [search-and-information-retrieval, elasticsearch-opensearch, elasticsearch, opensearch, rescore-top-window]
level: advanced
status: docs-checked
description: "Run an expensive query, script or LTR model over only the top window_size hits per shard with the rescore section."
sources:
  - https://www.elastic.co/docs/reference/elasticsearch/rest-apis/rescore-search-results
  - https://docs.opensearch.org/latest/api-reference/search-apis/search/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Rescore the top N hits

**Goal:** cheap first pass, precise second pass. The `rescore` search parameter reorders just the top documents (the page suggests 100 to 500) from the initial retrieval phase (query or knn) with a more costly algorithm, instead of running it over the whole index.
```
{"query":{"match":{"message":{"operator":"or","query":"the quick brown"}}},"rescore":{"window_size":10,"query":{"rescore_query":{"match_phrase":{"message":{"query":"the quick brown","slop":2}}},"query_weight":0.7,"rescore_query_weight":1.2}}}
```
- A rescore runs on each shard before the shard returns its results, so `window_size` is a per-shard figure. The default `window_size` is 10.
- Three rescorers in Elasticsearch: `query` (runs a `rescore_query` on the top documents), `script` (a script that sees the original score and field values) and `learning_to_rank` (needs the `model_id` of a deployed model plus any named `params`).
- Query rescorer: original and rescore scores are combined linearly; `query_weight` and `rescore_query_weight` both default to 1. `score_mode` is one of `total` (default), `multiply` (useful for function-query rescores), `avg`, `max`, `min`.
- An explicit `sort` other than `_score` descending together with a rescore query throws an error.
- Several rescorers can be given as an array and run in sequence, each working on the previous one's output. The page's common practice is a larger window for the first rescorer and smaller windows for the more expensive later ones.
- Pagination: keep `window_size` the same across pages; changing it while moving `from` can shift the top hits.
- Failure mode: too large a window recreates the cost you wanted to avoid.

## Verify
- [ ] The rescored top window orders as expected on a sample query, and the same request with `from` advanced still returns consistent top hits.

## Scope
The Elasticsearch page was checked. The OpenSearch Search API page lists `rescore` as an object or array that reorders the top results with a second, typically more expensive, query. The OpenSearch Rescore page returned 404, so OpenSearch rescorer types, defaults and `score_mode` values are unconfirmed; check your version.

## Checked

Checked 2026-11-08 against the Elasticsearch Rescore search results page and the OpenSearch Search API page (rescore parameter row). Confirmed: per-shard execution, `window_size` default 10, the three rescorers, `query_weight` and `rescore_query_weight` defaults, `score_mode` values, the sort error, chained rescores and the pagination note. Removed: the claim that documents outside the window keep their original order (not stated on the pages) and OpenSearch-specific claims.

Method: documentation only; no commands were run.
