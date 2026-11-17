---
id: computing-software.database-administration.cassandra.read-repair-and-speculative-retry
name: read-repair-and-speculative-retry
category: computing-software
field: database-administration
product: cassandra
tags: [cassandra, blocking-read-repair, speculative-retry, read-repair-chance, nosql, wide-column, cql]
level: practitioner
status: docs-checked
description: "Per-read consistency fixes"
sources: ["https://cassandra.apache.org/doc/latest/cassandra/managing/operating/read_repair.html", "https://cassandra.apache.org/doc/latest/cassandra/developing/cql/ddl.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Read repair and speculative retry

Goal: reason about read-time correction.
- Read repair is foreground and blocking: if replicas at the read consistency level disagree, the response waits until they are repaired; this gives monotonic quorum reads.
- The `read_repair` table option (4.0+) is `BLOCKING` (default) or `NONE`; `NONE` reconciles but does not repair, giving partition-level write atomicity instead of monotonic quorum reads.
- The table option `speculative_retry` (default 99PERCENTILE; `'99p'` and `'10ms'` forms) sends the read to an extra replica when the first ones are slow.
- Background read repair via `read_repair_chance` and `dclocal_read_repair_chance` was removed.
Verify: tail latency improves after changing `speculative_retry` on a test table.

## Checked

2026-11-02. Checked against the Read repair page (blocking behaviour, read_repair option, removal of read_repair_chance) and the CQL DDL/ALTER TABLE pages (speculative_retry default and examples). Removed: 'above CL ONE' and the 'ALWAYS'/'NONE' value list (not confirmed).

Method: documentation only; no commands were run.
