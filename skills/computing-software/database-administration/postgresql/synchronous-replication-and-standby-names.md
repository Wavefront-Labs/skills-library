---
id: computing-software.database-administration.postgresql.synchronous-replication-and-standby-names
name: synchronous-replication-and-standby-names
category: computing-software
field: database-administration
product: postgresql
tags: [database-administration, postgresql, postgres, streaming-replication, hot-standby, synchronous-standby-names, synchronous-replication, synchronous-commit, quorum-commit, zero-data-loss, rpo]
level: advanced
status: verified
description: "Configure PostgreSQL synchronous replication with synchronous_standby_names (FIRST/ANY quorum) and synchronous_commit levels, and avoid the write-stall when a standby dies."
sources:
  - https://www.postgresql.org/docs/current/warm-standby.html#SYNCHRONOUS-REPLICATION
  - https://www.postgresql.org/docs/current/runtime-config-replication.html#GUC-SYNCHRONOUS-STANDBY-NAMES
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Synchronous replication

**Goal:** committed transactions survive loss of the primary (RPO 0), with a
topology that does not stop all writes when one standby is down.

## Configure on the primary
Each standby identifies itself with `application_name` in its `primary_conninfo`.
```conf
# postgresql.conf on primary (reload)
synchronous_standby_names = 'ANY 1 (s_az2, s_az3)'   # quorum: any 1 of 2 must confirm
#   'FIRST 1 (s_az2, s_az3)'  priority: s_az2 unless it is down, then s_az3
synchronous_commit = on
```
Standby: `primary_conninfo = 'host=primary user=replicator application_name=s_az2 ...'`

## synchronous_commit levels (per cluster, role, session or transaction)
| Value | Commit returns after |
|---|---|
| `remote_apply` | Standby has applied it (read-your-writes on the standby) |
| `on` | Standby flushed WAL to disk |
| `remote_write` | Standby received and wrote to OS (not fsynced) |
| `local` | Local flush only (async for this transaction) |
| `off` | Not even local flush (may lose last ~3×wal_writer_delay on crash) |
Lower it per transaction for bulk loads: `SET LOCAL synchronous_commit = local;`.

## The availability trap
With one listed sync standby and it fails, **all commits on the primary hang**
(clients wait forever; the commit is already local but not acknowledged). Options:
- list at least two candidates (`ANY 1 (a,b)`) so one can fail;
- let your HA manager drop sync mode when no standby is available (check its documentation for the
  exact setting), accepting RPO>0 then;
- never clear the setting by hand during an incident without knowing that
  waiting transactions then return success.
Cancelled waits (`pg_cancel_backend`) produce `WARNING:  canceling wait for synchronous replication due to user request`
with `DETAIL:  The transaction has already committed locally, but might not have been replicated to the standby.`
The same releases the waiters when `synchronous_standby_names` is cleared and reloaded.

## Gotchas
- Sync replication adds a network round trip per commit; keep sync standbys in
  low-latency zones, async ones cross-region.
- It does not make standbys read-consistent unless `remote_apply`.
- Cascading replication is asynchronous; these settings do not apply to cascaded standbys (docs).
- `application_name` mismatch = standby shows `async` and nothing is protected.

## Verify
```sql
SELECT application_name, state, sync_state, sync_priority,
       write_lag, flush_lag, replay_lag FROM pg_stat_replication;
```
`sync_state` is `sync` or `quorum` for the intended standbys. Test: stop one
standby and confirm commits still return.

## Checked
- PostgreSQL 18.6 (primary with a standby whose `primary_conninfo` has `application_name=standby1`): `synchronous_standby_names = 'FIRST 1 (standby1, standby2)'` gave `sync_state = sync`, `sync_priority = 1`; `'ANY 1 (standby1, ghost)'` gave `quorum`; `'FIRST 1 (nomatch)'` (name mismatch) gave `async` and a `CREATE TABLE` then hung in `wait_event = SyncRep`; `pg_cancel_backend` on it returned the WARNING and DETAIL quoted above and the table existed afterwards; on another pair, clearing `synchronous_standby_names` with `ALTER SYSTEM RESET` plus reload released a waiting `INSERT` with success. The verify query columns (`sync_priority`, `write_lag`, ...) ran.
- Docs (runtime-config-wal): `synchronous_commit` values; `off` can lose recent commits with a maximum delay of three times `wal_writer_delay`; with empty `synchronous_standby_names` only `on` and `off` are meaningful; warm-standby (cascading replication is asynchronous).
- Patroni setting names removed (not verified).
