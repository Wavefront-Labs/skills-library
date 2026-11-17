---
id: computing-software.search-and-information-retrieval.elasticsearch-opensearch.knn-warmup-and-memory
name: knn-warmup-and-memory
category: computing-software
field: search-and-information-retrieval
product: elasticsearch-opensearch
tags: [search-and-information-retrieval, elasticsearch-opensearch, elasticsearch, opensearch, knn-warmup-and-memory]
level: practitioner
status: docs-checked
description: "OpenSearch k-NN plugin native memory: warmup and clear_cache APIs, knn.memory.circuit_breaker.limit, cache expiry settings and the stats API."
sources:
  - https://docs.opensearch.org/latest/vector-search/api/knn/
  - https://docs.opensearch.org/latest/vector-search/settings/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# k-NN memory, warmup and circuit breaker (OpenSearch)

**Goal:** predictable vector latency for approximate k-NN search on the native engines.
- Native library indexes (faiss, nmslib deprecated) are stored with the Lucene segment files and must be loaded into native memory. Unloaded files are loaded on the first search request, which can cause high latency on initial queries.
- Warmup: `GET /_plugins/_knn/warmup/index1,index2` loads all native library files for all shards (primaries and replicas) of the listed indexes. It is idempotent and the response gives `_shards` total, successful and failed. The call returns when warmup finishes or times out; after a timeout the operation continues, and `GET /_tasks` monitors it.
- Warmup best practices from the docs: do not merge indexes you want warmed (merging creates new segments whose graphs are not loaded); confirm all graphs fit in native memory; do not index documents into them (new writes keep native files from loading until searchable, so warm again after indexing).
- Clear cache (introduced 2.14): `POST /_plugins/_knn/clear_cache/index1,index2` (index patterns such as `index*` work) evicts the native files without deleting the index; it affects faiss and nmslib indexes, not the lucene engine.
- `knn.memory.circuit_breaker.limit` (dynamic, default 50%): native memory limit for native library indexes, applied to the memory left after the JVM; when usage exceeds it, the least recently used native indexes are removed. Per-node tiers: `node.attr.knn_cb_tier` in `opensearch.yml` plus `knn.memory.circuit_breaker.limit.<tier-name>` in cluster settings. `knn.memory.circuit_breaker.enabled` defaults to `true`.
- `knn.circuit_breaker.unset.percentage` (default 75) is the usage threshold, as a percentage of the limit, below which `knn.circuit_breaker.triggered` stays `false`.
- `knn.cache.item.expiry.enabled` (default `false`) and `knn.cache.item.expiry.minutes` (default `3h`) evict idle native indexes.
- Stats: `GET /_plugins/_knn/stats` (optionally `/_plugins/_knn/<nodeId>/stats/<stat>,<stat>`) returns `graph_memory_usage` (KB), `graph_memory_usage_percentage`, `hit_count`, `miss_count`, `eviction_count`, `cache_capacity_reached`, `circuit_breaker_triggered`, `total_load_time` (ns) and per-index `indices_in_cache`. `graph` is synonymous with native library index.
- Failure mode: graph memory above the limit causes cache thrashing, with operations repeatedly failing and retrying (docs warning).

## Verify
- [ ] After warmup, `hit_count` rises on repeated queries and `miss_count` and `eviction_count` stay flat.
- [ ] `cache_capacity_reached` is `false` in the stats.

## Checked
2026-11-08. Confirmed against the OpenSearch k-NN API page (stats fields, warmup, clear cache) and the k-NN plugin settings section of the vector search settings page: endpoints, idempotence, best practices, defaults and meanings of the circuit breaker and cache expiry settings, tier configuration.
Removed: the claim that queries fail until graphs are evicted when the breaker trips (docs say least recently used indexes are removed), the force-merge recommendation (docs advise not merging before warmup), and the Elasticsearch-side source (this skill is OpenSearch-only).
Method: documentation only; no commands were run.
