---
id: computing-software.database-administration.cassandra.key-and-row-cache
name: key-and-row-cache
category: computing-software
field: database-administration
product: cassandra
tags: [cassandra, row-cache-size, key-cache-size, caching-options, row-cache, key-cache, counter-cache, nosql, wide-column, cql]
level: practitioner
status: docs-checked
description: "Table caching"
sources: ["https://cassandra.apache.org/doc/latest/", "https://github.com/apache/cassandra/blob/trunk/conf/cassandra.yaml"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Key cache and row cache

Goal: decide on caches.
- `key_cache_size` empty means auto-sized (min of 5% heap or 100MiB), 0 disables it; the row cache is off by default (`row_cache_size: 0MiB`) and is enabled per table via `caching = {'rows_per_partition': ...}` (default `NONE`).
- `nodetool info` shows hit rates.
Verify: the hit rate in `nodetool info` justifies the memory.

## Checked

2026-11-02. Confirmed against Apache Cassandra trunk docs (doc/modules/cassandra/pages) and conf/cassandra.yaml, nodetool sources: key_cache_size auto sizing, row_cache_size 0MiB, rows_per_partition NONE default and caching option (cassandra.yaml, ddl page).
Removed: row-cache invalidation and the 85% threshold.
Method: documentation only; no commands were run.
