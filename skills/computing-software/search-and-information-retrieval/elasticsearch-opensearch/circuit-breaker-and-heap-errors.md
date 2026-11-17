---
id: computing-software.search-and-information-retrieval.elasticsearch-opensearch.circuit-breaker-and-heap-errors
name: circuit-breaker-and-heap-errors
category: computing-software
field: search-and-information-retrieval
product: elasticsearch-opensearch
tags: [search-and-information-retrieval, elasticsearch-opensearch, elasticsearch, opensearch, circuit-breaker-and-heap-errors, es-troubleshooting]
level: advanced
status: docs-checked
description: "Diagnose CircuitBreakingException and high heap using breaker stats, fielddata and aggregation usage."
sources:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/circuit-breaker.html
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/high-jvm-memory-pressure.html
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/advanced-configuration.html
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/cat-fielddata.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Circuit breaker and heap pressure

**Goal:** find what consumes memory.
- `GET _nodes/stats/breaker` (the `breaker` metric) reports per-breaker limits and how many times each tripped. Elasticsearch has a parent breaker plus fielddata, request, in-flight requests, script compilation, regex, EQL and model-inference breakers.
- Elasticsearch defaults: parent limit 95% of heap (70% if `indices.breaker.total.use_real_memory` is false), fielddata 40%, request 60%, in-flight requests 100% (bounded by the parent). Most breaker settings are dynamic.
- Breakers do not track all memory use, so they give only incomplete protection; nodes can still hit `OutOfMemoryError`.
- `GET _cat/fielddata?v=true&s=size:desc` shows fielddata per field and node; `GET _cat/nodes?v=true&h=name,heap.*,fielddata.*` shows heap and fielddata evictions; `POST my-index/_cache/clear?fielddata=true` clears the cache.
- Typical causes named by Elastic: many shards (each uses memory), a large `size`, aggregations with many buckets, mapping explosion, fielddata. `search.max_buckets` can cap bucket counts.
- Heap: `Xms`/`Xmx` no more than 50% of the memory available to the node, and under the compressed-oops threshold (26GB is safe on most systems, up to 30GB on some; the node log prints `compressed ordinary object pointers [true]`). Elasticsearch sizes the heap automatically by default.
- Failure mode: raising breaker limits instead of fixing the query leads to out-of-memory.

## Verify
- [ ] Breaker `tripped` counters stop increasing after the change.

## Notes
- Try every request on a test index first; syntax and defaults differ between Elasticsearch and OpenSearch versions, so check the linked reference for yours.
- Cited pages are Elasticsearch; OpenSearch breaker settings and defaults can differ.

## Checked
2026-11-08. Read the Elasticsearch Circuit breaker settings, High JVM memory pressure, JVM settings, cat fielddata and nodes stats pages. Confirmed the breaker defaults, the 50% heap and compressed-oops guidance, and the cat/cache-clear requests. Removed "terms aggregation on high-cardinality fields" and "fielddata on text" (not stated on the pages) and replaced them with the documented causes.
Method: documentation only; no commands were run.
