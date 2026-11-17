---
id: computing-software.database-administration.cassandra.table-options-and-alter
name: table-options-and-alter
category: computing-software
field: database-administration
product: cassandra
tags: [cassandra, table-options, alter-table, default-ttl, nosql, wide-column, cql]
level: practitioner
status: docs-checked
description: "gc_grace, compaction, compression and schema changes"
sources: ["https://cassandra.apache.org/doc/latest/", "https://github.com/apache/cassandra/blob/trunk/conf/cassandra.yaml"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Table options and ALTER TABLE

Goal: set per-table behaviour and evolve schema.
- Options: `default_time_to_live`, `gc_grace_seconds`, `compaction`, `compression`, `bloom_filter_fp_chance`, `speculative_retry`, `caching`.
- After compression changes run `nodetool upgradesstables -a`.
Verify: `nodetool describecluster` shows a single schema version.

## Checked

2026-11-02. Confirmed against Apache Cassandra trunk docs (doc/modules/cassandra/pages) and conf/cassandra.yaml, nodetool sources: table options, `nodetool upgradesstables -a` after compression changes (compression page), describecluster command (nodetool source).
Removed: ADD-column safety, primary-key immutability and the single-client advice.
Method: documentation only; no commands were run.
