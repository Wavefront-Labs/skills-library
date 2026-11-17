---
id: computing-software.database-administration.cassandra.unified-compaction-strategy
name: unified-compaction-strategy
category: computing-software
field: database-administration
product: cassandra
tags: [cassandra, unified-compaction-strategy, ucs, scaling-parameters, nosql, wide-column, cql]
level: practitioner
status: docs-checked
description: "UCS in 5.0"
sources: ["https://cassandra.apache.org/doc/latest/cassandra/managing/operating/compaction/ucs.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Unified Compaction Strategy

Goal: understand UCS.
- UCS is documented as recommended for most workloads and can be configured to behave like STCS, LCS or TWCS; parameters can change in flight without a full recompaction.
- `scaling_parameters` selects behaviour: `'L10'` for leveled (migrating from LCS) and `'T4'` for tiered (migrating from STCS); other options include `target_sstable_size` and `base_shard_count`.
- Compaction is parallelised through sharding by token range, and UCS is stateless.
Verify: compare write amplification and read latency against the previous strategy.

## Checked

2026-11-02. Checked against the UCS page (recommendation, migration examples L10 and T4, target_sstable_size, base_shard_count, sharding, stateless). Removed: the '5.0' version label and the 'trial on test tables' framing is now only the Verify step.

Method: documentation only; no commands were run.
