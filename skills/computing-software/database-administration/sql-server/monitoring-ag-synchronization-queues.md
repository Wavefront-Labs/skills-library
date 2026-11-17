---
id: computing-software.database-administration.sql-server.monitoring-ag-synchronization-queues
name: monitoring-ag-synchronization-queues
category: computing-software
field: database-administration
product: sql-server
tags: [database-administration, sql-server, always-on, availability-group, dm-hadr-database-replica-states, redo-queue, log-send-queue]
level: advanced
status: docs-checked
description: "Monitor Always On AG health: synchronization state, log send and redo queues, and estimated data loss and failover time from the DMV."
sources:
  - https://learn.microsoft.com/en-us/sql/relational-databases/system-dynamic-management-views/sys-dm-hadr-database-replica-states-transact-sql
  - https://learn.microsoft.com/en-us/sql/database-engine/availability-groups/windows/monitor-performance-for-always-on-availability-groups
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Monitoring AG synchronization

## Per database replica (run on the primary to see all replicas)
```sql
SELECT ag.name AS ag, ar.replica_server_name AS replica, DB_NAME(drs.database_id) AS db,
       ar.availability_mode_desc, drs.synchronization_state_desc, drs.synchronization_health_desc,
       drs.is_suspended, drs.suspend_reason_desc,
       drs.log_send_queue_size AS send_queue_kb, drs.log_send_rate AS send_kb_s,
       drs.redo_queue_size AS redo_queue_kb, drs.redo_rate AS redo_kb_s,
       drs.last_commit_time, drs.secondary_lag_seconds
FROM sys.dm_hadr_database_replica_states drs
JOIN sys.availability_replicas ar ON ar.replica_id = drs.replica_id
JOIN sys.availability_groups ag ON ag.group_id = drs.group_id
ORDER BY ag, db, replica;
```

## What the numbers mean
- **log_send_queue_size** (KB not yet sent to the secondary): your potential **data loss** if
  the primary dies now (RPO). Grows with network limits or a paused/disconnected secondary.
- **redo_queue_size** (KB received but not yet redone): adds to **failover time** (RTO),
  because the secondary must redo it before coming online; also staleness of readable
  secondaries.
- Estimated failover time ~ `redo_queue_size / redo_rate` seconds.
- `secondary_lag_seconds`: how far behind the secondary is.
- `synchronization_state`: `SYNCHRONIZED` (sync commit, caught up), `SYNCHRONIZING`
  (async, or sync catching up), `NOT SYNCHRONIZING` (problem), `REVERTING`/`INITIALIZING`.


## Alerts
- Any database `synchronization_health_desc <> 'HEALTHY'` or `is_suspended = 1`.
- `log_send_queue_size` above your RPO budget (convert using log generation rate).
- `redo_queue_size` large enough that estimated failover time exceeds RTO.
- Replica role changes (alert on them through your monitoring of the availability group).

## Gotchas
- Index rebuilds generate huge log bursts; expect queues to grow during maintenance.

## Checked
2026-11-01: columns of sys.dm_hadr_database_replica_states (queue sizes and rates in KB, synchronization states, is_suspended, suspend_reason_desc, last_commit_time, secondary_lag_seconds) and the redo queue/redo_rate pairing checked against the two Learn pages in sources. Removed: HADR_SYNC_COMMIT section, redo-blocking wait names, error numbers and Extended Events name, version note (not confirmed in those pages).
Method: documentation only; no commands were run.

## Verify
Generate load in a test and watch `send_queue_kb`/`redo_queue_kb` rise and drain; suspend data
movement on a test database and confirm the alert fires.
