---
id: computing-software.database-administration.cassandra.tombstone-heavy-queues
name: tombstone-heavy-queues
category: computing-software
field: database-administration
product: cassandra
tags: [cassandra, tombstones, tombstone-warn-threshold, queue-pattern, queue-antipattern, tombstone-antipattern, allow-filtering, nosql, wide-column, cql]
level: practitioner
status: docs-checked
description: "Why queues in Cassandra fail"
sources: ["https://cassandra.apache.org/doc/latest/cassandra/managing/operating/compaction/tombstones.html", "https://cassandra.apache.org/doc/latest/cassandra/managing/operating/metrics.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Queue and delete-heavy anti-pattern

Goal: recognise and replace delete-heavy designs.
- Tombstones are kept for `gc_grace_seconds` (default 864000, ten days) and are removed only by a later compaction; a node down longer than that can resurrect deleted data unless repaired.
- Reads that scan more than `tombstone_warn_threshold` tombstones count as warnings and more than `tombstone_failure_threshold` as failures; the table metrics `TombstoneWarnings` and `TombstoneFailures` count them. Look up the default values in `cassandra.yaml` for your version.
- Prefer time buckets with TTL so whole SSTables expire (see TWCS).
Verify: no tombstone warnings under load.

## Checked

2026-11-02. Checked against the Tombstones page (gc_grace_seconds 864000, compaction needed, resurrection) and the Metrics page (TombstoneWarnings, TombstoneFailures and the threshold names). Removed: the 1000 and 100000 defaults and the `sstablemetadata` inspection advice (not confirmed on the fetched pages).

Method: documentation only; no commands were run.
