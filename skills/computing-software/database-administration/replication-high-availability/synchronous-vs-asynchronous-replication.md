---
id: computing-software.database-administration.replication-high-availability.synchronous-vs-asynchronous-replication
name: synchronous-vs-asynchronous-replication
category: computing-software
field: database-administration
product: replication-high-availability
tags: [database-administration, replication-high-availability, high-availability, sync-vs-async-replication, semi-synchronous, rpo, commit-latency, quorum-commit]
level: practitioner
status: draft
description: "Choose synchronous, semi-synchronous or asynchronous replication from RPO, latency and availability needs, mapped to PostgreSQL, MySQL, SQL Server and Oracle."
sources:
  - https://dataintensive.net/
  - https://www.postgresql.org/docs/current/warm-standby.html#SYNCHRONOUS-REPLICATION
  - https://dev.mysql.com/doc/refman/8.4/en/replication-semisync.html
  - https://learn.microsoft.com/en-us/sql/database-engine/availability-groups/windows/availability-modes-always-on-availability-groups
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Synchronous vs asynchronous vs semi-synchronous replication

## The trade-off (DDIA ch. 5)
| Mode | Commit returns when | RPO on primary loss | Cost |
|---|---|---|---|
| Asynchronous | primary has it durable locally | seconds of committed data may be lost | no added latency |
| Synchronous | a replica has also durably received (or applied) it | zero (for that replica) | +1 network round trip + replica fsync per commit; primary **blocks** if the sync replica is unavailable |
| Semi-synchronous | a replica has **received** it (not necessarily applied) | near zero | +1 round trip; usually falls back to async after a timeout |

Fully synchronous to **all** replicas makes availability worse than a single server. The usual
pattern: synchronous to **one of N** nearby replicas (quorum), async to distant DR.

## Engine mapping
- **PostgreSQL**: `synchronous_standby_names = 'ANY 1 (s1, s2)'` (quorum) or `FIRST 1 (...)`;
  `synchronous_commit` = `remote_write` / `on` (flush) / `remote_apply` (read-your-writes on the
  standby) can be set per transaction (e.g. `SET LOCAL synchronous_commit = local` for unimportant
  writes). With no sync standby connected, commits hang (by design).
- **MySQL**: semisynchronous plugin (`rpl_semi_sync_source_wait_for_replica_count`,
  `rpl_semi_sync_source_timeout` -> falls back to async silently: monitor
  `Rpl_semi_sync_source_status`). `AFTER_SYNC` (lossless) is the default wait point.
  Group Replication is consensus-based (majority certification).
- **SQL Server AGs**: `SYNCHRONOUS_COMMIT` replicas (up to 5 in 2019+) needed for automatic
  failover; `REQUIRED_SYNCHRONIZED_SECONDARIES_TO_COMMIT` to require N.
- **Oracle Data Guard**: Maximum Availability (SYNC/AFFIRM, falls back if standby unreachable),
  Maximum Protection (primary shuts down rather than lose a sync standby), Maximum Performance (ASYNC).

## Deciding
1. State RPO per system (money movement: 0; analytics: minutes).
2. Measure network RTT between sites: sync across > ~5-10 ms RTT adds that to every commit.
3. Ensure at least **two** candidate sync replicas, or quorum, so one replica outage does not
   block writes.
4. Decide fallback: block (protect RPO) or degrade to async (protect availability), and alert on
   degradation either way.

## Gotchas
- "Synchronous" in some products means received, not durable or applied; read the exact guarantee.
- Sync replication does not protect against logical errors (a bad DELETE replicates instantly):
  you still need backups/PITR or a delayed replica.
- Read-your-writes on replicas needs apply-level sync (`remote_apply`) or routing reads to the primary.

## Verify
Measure commit latency with and without sync (pgbench / sysbench); kill the sync replica in a test
and confirm the system behaves as decided (blocks or degrades) and alerts fire.
