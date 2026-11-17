---
id: computing-software.database-administration.valkey.atomic-slot-migration
name: atomic-slot-migration
category: computing-software
field: database-administration
product: valkey
tags: [atomic-slot-migration, migrateslots, cluster, resharding, hash-slots]
level: advanced
status: docs-checked
description: "Valkey 9.0 atomic slot migration: CLUSTER MIGRATESLOTS, GETSLOTMIGRATIONS, CANCELSLOTMIGRATIONS, how the fork-based transfer works and tuning configs."
sources:
  - https://valkey.io/topics/atomic-slot-migration/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Valkey 9.0 adds atomic slot migration as a faster, more reliable alternative to the legacy `CLUSTER SETSLOT` migration, which remains available. It moves part of the 16384 hash slots between nodes.

Commands:
- Start on the source node: `CLUSTER MIGRATESLOTS SLOTSRANGE <start-slot> <end-slot> NODE <target>`. It returns at once and the work is asynchronous.
- Poll with `CLUSTER GETSLOTMIGRATIONS` on source or target. It shows in-progress migrations plus recent completed ones, with a short failure reason to guide retries.
- `CLUSTER CANCELSLOTMIGRATIONS` cancels active migrations whose source is that node; send it cluster-wide to cancel everything.

Mechanism: the source connects to the target and authenticates like a replication link, announces the migration with the internal `CLUSTER SYNCSLOTS`, forks a child to snapshot the slots (replicated on to the target replicas), and the parent tracks mutations meanwhile. It then sends the accumulated mutations; once in-flight mutations fall below a threshold it briefly pauses writes, the target catches up, takes ownership and broadcasts it. The source deletes the slot keys, unpauses, and clients get `MOVED` to the target.

Until the end, importing slots are hidden from `KEYS`, `SCAN`, `DBSIZE` and `INFO` counts on target primary and replica. `FLUSHDB` or `FLUSHALL` on source or target fails the migration; retry afterward.

Tuning: `client-output-buffer-limit` (replica class, hard and soft, large enough for mutations during the snapshot), `slot-migration-max-failover-repl-bytes` (pause once in-flight bytes are under this, for write-heavy loads), `cluster-slot-migration-log-max-len` (how many finished migrations are retained).

## Checked
2026-11-03. Confirmed against the Valkey Atomic slot migration page (valkey.io/topics/atomic-slot-migration/): Valkey 9.0, 16384 slots, the three CLUSTER commands and their syntax, the fork-based mechanism step by step, hidden importing slots, FLUSHDB/FLUSHALL failing the migration, and the three tuning settings. Nothing removed.
Method: documentation only; no commands were run.
