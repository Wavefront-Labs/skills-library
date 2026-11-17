---
id: computing-software.search-and-information-retrieval.elasticsearch-opensearch.cluster-capacity-planning
name: cluster-capacity-planning
category: computing-software
field: search-and-information-retrieval
product: elasticsearch-opensearch
tags: [search-and-information-retrieval, elasticsearch-opensearch, elasticsearch, opensearch, cluster-capacity-planning, es-sizing]
level: advanced
status: docs-checked
description: "Estimate storage, shard count, heap and node count from daily volume, retention, replicas and growth."
sources:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/size-your-shards.html
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/advanced-configuration.html
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/cat-indices.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Capacity planning for a cluster

**Goal:** a defensible sizing.
- Raw daily data x (1 + replicas) x expansion factor from a real sample index (measure it, do not assume) x retention days + headroom for watermarks and merges.
- Measure index size with a sample: `GET _cat/indices/sample?v&h=index,docs.count,store.size`.
- Shards: Elastic suggests shards of 10GB to 50GB with fewer than 200 million documents each; with ILM, rollover `max_primary_shard_size` 50gb and `min_primary_shard_size` 10gb enforce this. Master-eligible nodes need at least 1GB of heap per 3000 indices (4GB of heap: under 12000 indices).
- Memory: heap for shards and aggregations (no more than 50% of node memory), remainder for the filesystem cache.
- Load test with representative queries and mapping before buying.
- Failure mode: sizing from raw JSON size ignores index overhead and replicas.

## Verify
- [ ] A soak test at 1.5x expected load stays within latency and rejection targets.

## Notes
- Try every request on a test index first; syntax and defaults differ between Elasticsearch and OpenSearch versions, so check the linked reference for yours.
- Cited pages are Elasticsearch; OpenSearch guidance was not checked here. The sizing formula and the 1.5x soak test are working practice, not documented figures.

## Checked
2026-11-08. Read the Elasticsearch "Size your shards" page (10GB-50GB, 200 million documents, ILM rollover thresholds, 1GB heap per 3000 indices), the JVM settings page (50% heap) and the cat indices API page (`docs.count`, `store.size` columns). Replaced the vague "check current wording" shard guidance with the documented figures.
Method: documentation only; no commands were run.
