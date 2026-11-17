---
id: computing-software.search-and-information-retrieval.elasticsearch-opensearch.similarity-dfs-query-then-fetch
name: similarity-dfs-query-then-fetch
category: computing-software
field: search-and-information-retrieval
product: elasticsearch-opensearch
tags: [search-and-information-retrieval, elasticsearch-opensearch, elasticsearch, opensearch, similarity-dfs-query-then-fetch]
level: advanced
status: docs-checked
description: "Use the search_type dfs_query_then_fetch in Elasticsearch to score with global term and document frequencies instead of per-shard statistics."
sources:
  - https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-search
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Shard-level statistics and dfs_query_then_fetch (Elasticsearch)

**Goal:** comparable scores across shards.
- The `search_type` parameter sets how distributed term frequencies are calculated for relevance scoring. Values: `query_then_fetch` and `dfs_query_then_fetch`.
- `query_then_fetch` scores with local term and document frequencies for each shard: usually faster, less accurate.
- `dfs_query_then_fetch` scores with global term and document frequencies across all shards: usually slower, more accurate.
- Use `GET my-index/_search?search_type=dfs_query_then_fetch` where ranking accuracy matters, for example small multi-shard test indices where per-shard statistics skew scores (inference from the two descriptions above).
- OpenSearch: not checked. Its search page was fetched but the `search_type` row was too long to read; it lists a `dfs_pre_query` and `dfs_query` phase in `phase_took`.

## Verify
- [ ] Run the same query with and without `dfs_query_then_fetch` on a multi-shard index and compare `_score` values.

## Checked
Checked 2026-11-08 against the Elasticsearch "Search" API page. Only Elasticsearch was checked. Removed: the "extra round trip" cost claim, the routing and single-primary-shard workarounds, and the high-QPS latency warning, none of which the page states beyond "usually slower".
Method: documentation only; no commands were run.
