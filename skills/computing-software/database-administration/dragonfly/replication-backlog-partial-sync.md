---
id: computing-software.database-administration.dragonfly.replication-backlog-partial-sync
name: replication-backlog-partial-sync
category: computing-software
field: database-administration
product: dragonfly
tags: [replication-backlog, partial-sync, full-sync, shard-repl-backlog, dragonfly]
level: advanced
status: docs-checked
description: "Tune the per-shard replication backlog flags so Dragonfly replicas reconnect with a partial sync instead of a full sync."
sources:
  - https://raw.githubusercontent.com/dragonflydb/documentation/main/docs/managing-dragonfly/replication.md
  - https://raw.githubusercontent.com/dragonflydb/documentation/main/docs/managing-dragonfly/flags.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
When a replica reconnects, the primary tries a partial sync from its per-shard replication backlog and falls back to a full sync if the backlog no longer holds what the replica missed.

From Dragonfly v2.0.0 the backlog is limited by age and size:

- `--shard_repl_backlog_time_ms` (default `5000`; `0` disables the age limit): older entries are evicted as new writes arrive.
- `--shard_repl_backlog_max_bytes` (default `0`): caps each shard's backlog; `0` uses `maxmemory` / shard count / 200.
- `--shard_repl_backlog_len` is legacy. A nonzero value limits by entry count and disables the age and size limits unless one of the new flags is also set.

If replicas often do a full sync after short disconnections, increase these limits.

Related:

- `--replica_partial_sync` (default true) lets replicas use partial sync after an interruption.
- `--replication_acks_interval` (default 1000 ms) sets the ack interval.
- `--break_replication_on_master_restart` (default false) breaks replication when the master restarts, avoiding flushing the replica's data.

Watch the `lag` field of `INFO REPLICATION` on the primary to see how far replicas are behind.

## Checked

2026-11-04. Confirmed in the Replication page (backlog paragraph, lag section) and the flags page (`replica_partial_sync`, `replication_acks_interval`, `break_replication_on_master_restart` and defaults). Removed the claim that `ROLE` shows `full_sync` states, which the pages do not document.

Method: documentation only; no commands were run.
