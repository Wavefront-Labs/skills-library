---
id: computing-software.database-administration.postgresql.hot-standby-query-conflicts
name: hot-standby-query-conflicts
category: computing-software
field: database-administration
product: postgresql
tags: [database-administration, postgresql, postgres, streaming-replication, hot-standby, hot-standby-feedback, max-standby-streaming-delay, recovery-conflict, canceling-statement, read-replica, pg-stat-database-conflicts]
level: advanced
status: docs-checked
description: "Stop 'canceling statement due to conflict with recovery' on PostgreSQL read replicas by choosing between hot_standby_feedback, standby delay settings and replica roles."
sources:
  - https://www.postgresql.org/docs/current/hot-standby.html#HOT-STANDBY-CONFLICT
  - https://www.postgresql.org/docs/current/runtime-config-replication.html#GUC-HOT-STANDBY-FEEDBACK
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Hot standby query conflicts

**Goal:** long reports on replicas finish, without bloating the primary or
letting replicas fall hours behind.

## The error
`ERROR: canceling statement due to conflict with recovery` /
`DETAIL: User query might have needed to see row versions that must be removed.`
The standby must replay a WAL record (usually VACUUM cleanup of dead rows) that
removes rows a running query can still see. It waits up to
`max_standby_streaming_delay` (default 30s), then cancels the query.

## See which kind
```sql
SELECT datname, confl_snapshot, confl_lock, confl_bufferpin, confl_deadlock, confl_tablespace
FROM pg_stat_database_conflicts;      -- run on the standby (the docs say it shows cancels and their reasons)
```
- snapshot: vacuum cleanup (most common)
- lock: `ACCESS EXCLUSIVE` from primary (DDL, TRUNCATE, vacuum truncating the table end)
- bufferpin: vacuum cleanup of a page that a standby query is accessing, whether or not the removed data is visible to it
- also `confl_tablespace`, `confl_deadlock` and `confl_active_logicalslot` columns exist

## Options (pick per replica purpose)
| Setting (standby) | Effect | Cost |
|---|---|---|
| `hot_standby_feedback = on` | Standby tells primary its oldest snapshot; primary vacuum keeps those rows | Bloat on primary while long queries run; slot-like behaviour without the slot |
| `max_standby_streaming_delay = 15min` (or -1) | Replay waits for queries | Replica lag up to that value (bad for HA failover target) |
| Primary `vacuum_truncate = off` (or the table storage parameter) | Truncation needs an ACCESS EXCLUSIVE lock on the table, which is what conflicts on a standby | Table file does not shrink |
Common pattern: an HA standby with short delay and feedback off; a separate
reporting replica with feedback on (or a long delay) and query timeouts.

## Gotchas
- `hot_standby_feedback` eliminates cleanup-record (snapshot) conflicts only; it does not prevent lock conflicts from ACCESS EXCLUSIVE locks (DDL, TRUNCATE), tablespace or database drops.
- Feedback plus a forgotten idle-in-transaction session on the replica holds back
  vacuum on the primary indefinitely: set `idle_in_transaction_session_timeout`
  and `statement_timeout` for replica users.
- Delay settings only apply to WAL from streaming/archive respectively
  (`max_standby_archive_delay` for archive replay).

## Verify
- `confl_snapshot` stops growing after the change.
- On the primary, `SELECT backend_xmin FROM pg_stat_replication;` shows the
  standby's xmin when feedback is on; watch `age(backend_xmin)` and dead tuples.

## Checked
2026-10-25. Against PostgreSQL 18 documentation (REL_18_STABLE doc/src/sgml, branch head 2026-10-24; PostgreSQL 19 is still at release-candidate stage): hot standby chapter (conflict cases: ACCESS EXCLUSIVE locks, tablespace and database drops, vacuum cleanup records versus snapshots and versus page access; `max_standby_archive_delay` versus `max_standby_streaming_delay`; remedial options; `pg_stat_database_conflicts` shows cancels and reasons), `max_standby_streaming_delay` (default 30 seconds, -1 waits forever), `hot_standby_feedback` (default off, can cause bloat on the primary, passed upstream in cascades), `vacuum_truncate` (ACCESS EXCLUSIVE lock; storage-parameter override), the `pg_stat_database_conflicts` columns and `pg_stat_replication.backend_xmin`. Removed the PG12 version gate and corrected the claim about which conflicts feedback prevents.
Method: documentation only; no commands were run.
