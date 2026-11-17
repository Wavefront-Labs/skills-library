---
id: computing-software.database-administration.cassandra.bloom-filter-tuning
name: bloom-filter-tuning
category: computing-software
field: database-administration
product: cassandra
tags: [cassandra, bloom-filter-memory, bloom-filter-false-positive, disable-bloom, nosql, wide-column, cql]
level: practitioner
status: docs-checked
description: "Memory vs read cost"
sources: ["https://cassandra.apache.org/doc/latest/cassandra/managing/operating/bloom_filters.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Bloom filter tuning

Goal: balance memory against false positives.
- `bloom_filter_fp_chance` is a float between 0 and 1, per table; the default is 0.1 for LeveledCompactionStrategy tables and 0.01 otherwise.
- Bloom filters live off-heap, so ignore them when sizing the heap. 0.01 needs about three times the memory of 0.1.
- More RAM and slower disks favour a lower value; less RAM, dense nodes or very fast disks tolerate a higher one; read-rare or scan-only (analytics) workloads can use a much higher one.
- `ALTER TABLE keyspace.table WITH bloom_filter_fp_chance=0.01` only affects new SSTables; run `nodetool scrub` or `nodetool upgradesstables -a` to rebuild existing ones.
Verify: `DESCRIBE TABLE` shows the new value.

## Checked

2026-11-02. Checked against the Bloom Filters page (defaults, off-heap, three-times memory, tuning guidance, ALTER TABLE, scrub and upgradesstables -a). Removed: 'TWCS tables often use higher values', 'disable with 1.0', and the tablestats memory claim (not on the page).

Method: documentation only; no commands were run.
