---
id: computing-software.database-administration.scylladb.kb-compaction-strategies-overview
name: kb-compaction-strategies-overview
category: computing-software
field: database-administration
product: scylladb
tags: [compaction, ics, lcs, twcs, stcs, major-compaction]
level: practitioner
status: docs-checked
description: "ScyllaDB compaction overview: minor vs major compaction, strategies ICS (default), LCS, TWCS, the deprecated STCS alias and its allow flag, and major compaction disk needs."
sources: ["https://github.com/scylladb/scylladb/blob/master/docs/kb/compaction.rst"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Compaction overview and strategy choice

ScyllaDB writes follow the LSM design: updates go to a memtable that is flushed to an immutable sorted SSTable. Two problems accumulate over time: overwritten or deleted data in older SSTables wastes space, and reads must consult many SSTables. Compaction merges SSTables into new ones holding only live data.

Types:
- **Minor**: triggered automatically per the compaction strategy; recommended.
- **Major**: triggered by `nodetool compact` over all SSTables. Can exhaust resources, raise cost and use disk; it needs 50% more disk space than your data unless you use ICS.

Strategies (set in `CREATE`/`ALTER TABLE` compaction options):
- **Incremental (ICS)**: the default. Runs of sorted, fixed-size SSTables (default 1 GB) organised in size tiers; lowers temporary space amplification.
- **Leveled (LCS)**: small fixed-size SSTables (default 160 MB) in levels; lowers read and space amplification.
- **Time-window (TWCS)**: for time series; uses size-tiered compaction inside the open window, and when a window closes, compacts it into one SSTable.
- **Size-tiered (STCS)**: deprecated. `SizeTieredCompactionStrategy` is an alias of ICS. Naming it in CREATE/ALTER TABLE or materialized views still works but returns a CQL warning; set `allow_deprecated_size_tiered_compaction_strategy: false` (default true) to make it an error.

STCS logic that remains inside TWCS and LCS level 0: SSTables are bucketed by size (`bucket_low`, `bucket_high`) and when a bucket reaches `min_threshold`, its members merge.

Changing strategy or its parameters with ALTER can create issues. Inspect with `nodetool compactionstats` and `compactionhistory`.

## Checked

2026-11-04: compaction types, the four strategies with their defaults, the STCS alias and allow flag, and the STCS bucket parameters confirmed against the ScyllaDB compaction knowledge-base page. Corrected the major-compaction disk claim (ICS is the exception) and removed the unsupported rewrite remark.

Method: documentation only; no commands were run.
