---
id: computing-software.database-administration.cassandra.stcs-vs-lcs
name: stcs-vs-lcs
category: computing-software
field: database-administration
product: cassandra
tags: [cassandra, size-tiered-compaction, leveled-compaction, write-amplification, compaction, stcs, lcs, nosql, wide-column, cql]
level: practitioner
status: docs-checked
description: "Choosing a compaction strategy"
sources: ["https://cassandra.apache.org/doc/latest/cassandra/managing/operating/compaction/stcs.html", "https://cassandra.apache.org/doc/latest/cassandra/managing/operating/compaction/lcs.html", "https://cassandra.apache.org/doc/latest/cassandra/managing/operating/compaction/ucs.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SizeTiered vs Leveled compaction

Goal: match strategy to workload.
- STCS is the default strategy, recommended for write-intensive workloads; it compacts when 4 (the default `min_threshold`) similar-sized SSTables accumulate.
- LCS groups SSTables into levels, each 10x the previous by default, with `sstable_size_in_mb` default 160.
- Example: `ALTER TABLE t WITH compaction = {'class':'LeveledCompactionStrategy','sstable_size_in_mb':160}`.
- UCS is documented as recommended for most workloads and can be configured to behave like either.
Verify: pending compactions drain between peaks.

## Checked

2026-11-02. Checked against the STCS, LCS and UCS pages (default strategy, 4 SSTables, 10x levels, sstable_size_in_mb 160, UCS recommendation). Removed: '50% free disk', read/write amplification claims and `nodetool compactionstats` pending-task wording (not stated on those pages).

Method: documentation only; no commands were run.
