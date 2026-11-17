---
id: computing-software.database-administration.postgresql.wait-event-sampling-from-pg-stat-activity
name: wait-event-sampling-from-pg-stat-activity
category: computing-software
field: database-administration
product: postgresql
tags: [database-administration, postgresql, postgres, pg-monitoring, pg-wait-events, pg-stat-activity, wait-event-type, lwlock, io-wait, lock-wait, pg-wait-sampling, active-session-history]
level: practitioner
status: verified
description: "Find what PostgreSQL backends are waiting on by sampling wait_event_type/wait_event in pg_stat_activity, and map common wait events to their fixes."
sources:
  - https://www.postgresql.org/docs/current/monitoring-stats.html#WAIT-EVENT-TABLE
  - https://www.postgresql.org/docs/current/monitoring-stats.html#MONITORING-PG-STAT-ACTIVITY-VIEW
  - https://github.com/postgrespro/pg_wait_sampling
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Wait-event sampling from pg_stat_activity

**Goal:** answer "the database is slow, what is it doing?" with evidence: which waits dominate active sessions right now.

## 1. One snapshot
```sql
SELECT wait_event_type, wait_event, state, count(*)
FROM pg_stat_activity
WHERE backend_type = 'client backend' AND state <> 'idle'
GROUP BY 1, 2, 3 ORDER BY 4 DESC;
```
`wait_event IS NULL` with `state = 'active'` means **on CPU** (not waiting). One snapshot lies; sample.

## 2. Poor man's ASH (sample every second for a minute)
```bash
for i in $(seq 60); do
  psql -XAtc "SELECT now(), coalesce(wait_event_type,'CPU'), coalesce(wait_event,'CPU'), left(query,60)
              FROM pg_stat_activity WHERE backend_type = 'client backend' AND state='active' AND pid <> pg_backend_pid()" >> waits.log
  sleep 1
done
cut -d'|' -f2,3 waits.log | sort | uniq -c | sort -rn | head
```
For continuous history install `pg_wait_sampling` (`shared_preload_libraries = 'pg_wait_sampling'`) and query `pg_wait_sampling_profile`.

## 3. Reading the common ones
| wait_event_type / wait_event | Means | Usual fix |
|---|---|---|
| Lock / relation, tuple, transactionid | Row or table lock contention | Find blocker: `pg_blocking_pids(pid)`; shorten transactions |
| LWLock / WALWrite, WALInsert | WAL flush bottleneck | Faster WAL disk, `wal_buffers`, batch commits |
| LWLock / BufferMapping, BufferContent | Hot pages / shared_buffers churn | Bigger `shared_buffers`, fix hot-row updates |
| LWLock / LockManager | Too many locks per query (many partitions/indexes) | Fewer partitions touched, prune at plan time |
| IO / DataFileRead | Reading from disk (cache misses) | Indexes, more RAM, check `pg_stat_io` |
| IO / WalSync, DataFileSync | fsync latency | Storage latency; check `pg_test_fsync` |
| Client / ClientRead | Waiting on the app (idle in transaction if in a txn) | App-side: connection held while doing work |
| IPC / SyncRep | Waiting for synchronous standby | Standby lag or network; see `pg_stat_replication` |
| Timeout / PgSleep, VacuumDelay | Deliberate sleep / cost-based vacuum delay | Usually benign |

## 4. Blocking tree
```sql
SELECT pid, pg_blocking_pids(pid) AS blocked_by, wait_event, now()-xact_start AS xact_age, left(query,80)
FROM pg_stat_activity WHERE cardinality(pg_blocking_pids(pid)) > 0;
```

## Gotchas
- Wait events are only a snapshot of what is happening at the instant you look; short waits are invisible without high-frequency sampling.
- `pg_blocking_pids()` takes lock-manager locks; do not call it in a tight loop on a busy server.
- Wait event names change between major versions; check the table for your version.

## Verify
After a fix, the sampled histogram shifts (e.g. Lock/transactionid share drops) and p95 latency improves.

## Checked
- PostgreSQL 18.6: `pg_wait_events` lists the names used in the table (`WALWrite`, `WALInsert`, `BufferMapping`, `LockManager`, `DataFileRead`, `WalSync`, `DataFileSync`, `ClientRead`, `SyncRep`, `PgSleep`, `VacuumDelay`, `relation`, `tuple`, `transactionid`) and shows `BufferContent` (not `buffer_content`: fixed). With one session holding `LOCK TABLE`, one waiting on it and one CPU-bound `generate_series`, the snapshot query showed `Lock|relation|active` and a blank wait_event for the CPU one; the sampling loop produced `Lock|relation`, `Timeout|PgSleep` and `CPU|CPU` counts, and also counted a walsender (`Activity|WalSenderMain`) until `backend_type = 'client backend'` was added to the filter; the blocking-tree query returned `{blocking pid}` for the waiter with `wait_event = relation`.
- Docs: monitoring-stats (`wait_event` NULL when not waiting), functions-info (`pg_blocking_pids` takes exclusive access to the lock manager's shared state briefly; frequent calls can affect performance), pg_wait_sampling README (`shared_preload_libraries`, `pg_wait_sampling_profile` view; documented only, extension not installed). `pg_test_fsync` ships in the 18.6 binaries.
