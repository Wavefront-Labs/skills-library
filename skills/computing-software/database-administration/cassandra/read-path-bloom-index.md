---
id: computing-software.database-administration.cassandra.read-path-bloom-index
name: read-path-bloom-index
category: computing-software
field: database-administration
product: cassandra
tags: [cassandra, read-path, bloom-filter, key-cache, nosql, wide-column, cql]
level: practitioner
status: docs-checked
description: "How a read merges memtable and SSTables"
sources: ["https://cassandra.apache.org/doc/latest/", "https://github.com/apache/cassandra/blob/trunk/conf/cassandra.yaml"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Read path, bloom filters, key cache

Goal: explain and tune read latency.
- Reads consult the memtable and SSTables; each SSTable has a bloom filter, stored off heap.
- `bloom_filter_fp_chance` per table (default 0.1 for LCS, 0.01 otherwise; lower costs memory).
- `nodetool tablehistograms <ks> <t>` shows SSTables per read; high values mean compaction lag or a bad model.
Verify: the SSTables column of `tablehistograms` stays low on latency-sensitive tables.

## Checked

2026-11-02. Confirmed against Apache Cassandra trunk docs (doc/modules/cassandra/pages) and conf/cassandra.yaml, nodetool sources: bloom_filter_fp_chance defaults and memory trade-off, bloom filters off heap (bloom filter page), tablehistograms SSTables column.
Removed: the read-path ordering, bloom-ratio via tablestats and the 4-SSTable target.
Method: documentation only; no commands were run.
