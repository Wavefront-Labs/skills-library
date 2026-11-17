---
id: computing-software.search-and-information-retrieval.elasticsearch-opensearch.filter-context-and-caching
name: filter-context-and-caching
category: computing-software
field: search-and-information-retrieval
product: elasticsearch-opensearch
tags: [search-and-information-retrieval, elasticsearch-opensearch, elasticsearch, opensearch, filter-context-and-caching]
level: advanced
status: docs-checked
description: "Use filter context for reusable yes/no conditions and understand the node query cache and request cache."
sources:
  - https://www.elastic.co/docs/reference/query-languages/query-dsl/query-filter-context
  - https://www.elastic.co/docs/reference/elasticsearch/configuration-reference/node-query-cache-settings
  - https://www.elastic.co/docs/reference/elasticsearch/rest-apis/shard-request-cache
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Filter context and query caching

**Goal:** cheaper, cacheable queries.
- Filter context applies to the `filter` and `must_not` parameters of `bool`, the `filter` parameter of `constant_score`, and `filter` aggregations. Filters compute no relevance score and frequently used ones are cached automatically.
- Node query cache: one per node, shared by all shards, LRU eviction; caches results of queries used in filter context (term queries and queries outside filter context are not eligible). Default: up to 10000 queries in up to 10% of heap; `indices.queries.cache.size` (static, set on every data node) accepts a percentage or exact value and defaults to `10%`. Caching is per segment (segments with at least 10000 documents and at least 3% of the shard's documents), so merging segments can invalidate cached queries. `index.queries.cache.enabled` (index creation or closed index) defaults to `true`.
- Shard request cache: by default caches only requests with `size=0` (`hits.total`, aggregations, suggestions, not `hits`); invalidated when the shard refreshes or the mapping changes; per-request override `?request_cache=true` (also needed to cache `size` greater than 0); index setting `index.requests.cache.enable`. The cache key is a hash of the whole JSON body, so reordering keys misses the cache.
- Most queries that use `now` cannot be request-cached.
- Monitor: `GET /_nodes/stats/indices/request_cache?human` (and `GET /_stats/request_cache?human`) show cache size and evictions.

## Verify
- [ ] Run the same `size:0` aggregation twice with `?request_cache=true` and compare the request cache stats.

## Scope
The Elasticsearch reference pages were checked; OpenSearch behaviour was not.

## Checked

Checked 2026-11-02 against the Elasticsearch reference pages: Query and filter context, Node query cache settings, Shard request cache. Confirmed: all statements above. Removed: "unrounded `now` yields a different cache key each request" and "rounded `now/d` is cacheable" (the page says only that most `now` queries cannot be cached), `hit_count` in stats and `_nodes/stats/indices/query_cache` (not shown on the pages), and the OpenSearch source root.

Method: documentation only; no commands were run.
