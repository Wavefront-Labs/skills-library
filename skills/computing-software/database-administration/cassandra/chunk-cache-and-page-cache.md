---
id: computing-software.database-administration.cassandra.chunk-cache-and-page-cache
name: chunk-cache-and-page-cache
category: computing-software
field: database-administration
product: cassandra
tags: [cassandra, chunk-cache-size, buffer-pool, cache-hit-rate, nosql, wide-column, cql]
level: practitioner
status: docs-checked
description: "Read caching layers"
sources: ["https://cassandra.apache.org/doc/latest/", "https://github.com/apache/cassandra/blob/trunk/conf/cassandra.yaml"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Chunk cache and OS cache interplay

Goal: reason about caching layers.
- `file_cache_size` bounds the off-heap sstable chunk cache and buffer pool (default: smaller of 1/4 heap or 512MB).
- Cassandra also relies on the OS page cache for recently read file portions; heap should be at most 50% of RAM.
- Measure with `nodetool info` and OS tools.
Verify: iostat reads fall as cache warms.

## Checked

2026-11-02. Confirmed against Apache Cassandra trunk docs (doc/modules/cassandra/pages) and conf/cassandra.yaml, nodetool sources: file_cache_size description and default (cassandra.yaml), page cache and heap guidance (hardware page).
Removed: nothing.
Method: documentation only; no commands were run.
