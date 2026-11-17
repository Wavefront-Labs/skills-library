---
id: computing-software.search-and-information-retrieval.elasticsearch-opensearch.primary-shard-sizing
name: primary-shard-sizing
category: computing-software
field: search-and-information-retrieval
product: elasticsearch-opensearch
tags: [search-and-information-retrieval, elasticsearch-opensearch, elasticsearch, opensearch, primary-shard-sizing, es-shards-replicas]
level: advanced
status: docs-checked
description: "Pick primary shard count and size in Elasticsearch: 10-50GB and under 200M documents per shard, ILM rollover thresholds, shard and index count limits, fixing wrong sizes."
sources:
  - https://www.elastic.co/docs/deploy-manage/production-guidance/optimize-performance/size-shards
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Choose primary shard count and size (Elasticsearch)

**Goal:** avoid oversharding and giant shards. Scope: Elasticsearch documentation ("Size your Elasticsearch shards"); OpenSearch guidance was not checked here.

## Guidelines from the docs
- Aim for shard sizes between 10GB and 50GB and keep documents per shard below about 200 million. Larger or smaller can suit some use cases; there is no hard physical size limit, and a shard can in theory hold just over two billion documents (Lucene limit 2,147,483,519 including deleted documents).
- Too many shards degrade search performance and stability (oversharding); very large shards slow searches and lengthen recovery.
- Each shard runs a search on a single CPU thread; each index, shard, segment and mapped field has overhead, and a small set of large shards usually uses fewer resources than many small ones.
- Master-eligible nodes: reserve at least 1GB of heap per 3000 indices (an upper bound, not a performance guarantee).
- Cluster shard limits prevent more than 1000 non-frozen shards per node and 3000 frozen shards per dedicated frozen node. `cluster.max_shards_per_node` can be raised temporarily to get past the "maximum normal shards open" error, but the lasting fix is more nodes or fewer shards.
- There is no one-size-fits-all strategy: benchmark your own data on production hardware.

## Practice
- Time series: use data streams with ILM rollover. Set the rollover `max_primary_shard_size` to `50gb` and `min_primary_shard_size` to `10gb` to keep shards in range; avoid `max_age`-only rollover that creates empty indices.
- Delete indices rather than documents.
- Inspect: `GET _cat/shards?v=true&h=index,prirep,shard,store&s=prirep,store&bytes=gb`; heap with `GET _cat/nodes?v=true&h=heap.max`.
- Shards are immutable, so a wrong primary count means copying the index: Split Index to increase primaries (or Shrink to reduce them for read-only indices), or create a destination index with corrected settings and Reindex. The docs state Restore Snapshot and Clone Index do not fix shard sizing. Ensure enough disk first.
- Limit hotspots with `index.routing.allocation.total_shards_per_node`.
- To reduce shard count: longer-interval indices, delete empty indices, force merge indices no longer written to, shrink, or reindex small indices into larger ones.

## Verify
- [ ] `_cat/shards` sizes are in the planned range and no node holds an unusual number of shards.
- [ ] Documents per shard (docs.count plus docs.deleted) are well below the recommended 200 million.

## Notes
- Try every request on a test index first.

## Checked
2026-11-08. Confirmed against the Elasticsearch "Size your Elasticsearch shards" page: size and document guidelines, rollover thresholds, shard limits, heap guideline, repair options, example requests. Removed: `_cat/allocation` (not on the page) and OpenSearch applicability (not checked).
Method: documentation only; no commands were run.
