---
id: computing-software.database-administration.cassandra.off-heap-and-page-cache
name: off-heap-and-page-cache
category: computing-software
field: database-administration
product: cassandra
tags: [cassandra, offheap-memtables, chunk-cache, page-cache, nosql, wide-column, cql]
level: practitioner
status: docs-checked
description: "Memory beyond the heap"
sources: ["https://cassandra.apache.org/doc/latest/", "https://github.com/apache/cassandra/blob/trunk/conf/cassandra.yaml"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Off-heap structures and page cache

Goal: understand where memory goes.
- Bloom filters live off heap, so they do not count towards heap sizing; the chunk cache is also off heap (`file_cache_size`).
- Rely on the OS page cache for SSTable reads; heap should be at most 50% of RAM.
- If Cassandra dies with `OutOfMemoryError: Map failed`, check `/proc/<pid>/limits` and raise `vm.max_map_count`.
Verify: most RAM outside the heap is available to the OS page cache.

## Checked

2026-11-02. Confirmed against Apache Cassandra trunk docs (doc/modules/cassandra/pages) and conf/cassandra.yaml, nodetool sources: bloom filters off heap, file_cache_size off heap, heap at most 50% RAM, Map failed FAQ with /proc/<pid>/limits and vm.max_map_count.
Removed: compression-metadata/index-summary/off-heap-memtable claims, swap advice, free -m.
Method: documentation only; no commands were run.
