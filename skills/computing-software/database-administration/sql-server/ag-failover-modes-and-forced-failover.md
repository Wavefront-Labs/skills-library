---
id: computing-software.database-administration.sql-server.ag-failover-modes-and-forced-failover
name: ag-failover-modes-and-forced-failover
category: computing-software
field: database-administration
product: sql-server
tags: [database-administration, sql-server, mssql, forced-failover, availability-groups, planned-manual-failover, force-failover-allow-data-loss, resume-data-movement, disaster-recovery, failure-condition-level]
level: advanced
status: docs-checked
description: "Run SQL Server AG failovers: automatic and planned manual failover checks, forced failover with possible data loss, estimating loss, and resuming suspended secondaries."
sources:
  - https://learn.microsoft.com/en-us/sql/database-engine/availability-groups/windows/failover-and-failover-modes-always-on-availability-groups
  - https://learn.microsoft.com/en-us/sql/database-engine/availability-groups/windows/perform-a-forced-manual-failover-of-an-availability-group-sql-server
  - https://learn.microsoft.com/en-us/sql/database-engine/availability-groups/windows/flexible-automatic-failover-policy-availability-group
  - https://learn.microsoft.com/en-us/sql/t-sql/statements/alter-availability-group-transact-sql
  - https://learn.microsoft.com/en-us/sql/sql-server/failover-clusters/windows/force-a-wsfc-cluster-to-start-without-a-quorum
  - https://learn.microsoft.com/en-us/sql/relational-databases/system-functions/sys-fn-hadr-is-primary-replica-transact-sql
  - https://docs.dbatools.io/Copy-DbaLogin.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AG failover modes and forced failover

## Modes
| Type | Requirement | Data loss |
|---|---|---|
| Automatic | sync commit, `FAILOVER_MODE = AUTOMATIC` on both, secondary SYNCHRONIZED, quorum | none |
| Planned manual | sync commit and SYNCHRONIZED | none |
| Forced | any state, run on the target secondary | possible |
What triggers automatic failover is set by `FAILURE_CONDITION_LEVEL` (1-5, default 3) and
`HEALTH_CHECK_TIMEOUT` (default 30000 ms, minimum 15000). With `DB_FAILOVER = ON`, any status other than ONLINE for an AG database on the primary also triggers automatic failover; the failure-condition levels alone never detect damaged or suspect databases.

## Planned manual failover
```sql
-- on the target secondary: confirm it is ready
SELECT ar.replica_server_name, drs.database_name, drs.is_failover_ready
FROM sys.dm_hadr_database_replica_cluster_states drs
JOIN sys.availability_replicas ar ON ar.replica_id = drs.replica_id;
-- every database is_failover_ready = 1, then:
ALTER AVAILABILITY GROUP [AG1] FAILOVER;
```
For an async DR replica: switch it to sync commit first, wait for SYNCHRONIZED, fail over, switch back.

## Forced failover (primary lost)
1. Decide: is the primary truly unrecoverable within the RTO? Forcing makes old-primary-only transactions unrecoverable through the AG.
2. Estimate data loss on the candidate:
   ```sql
   SELECT DB_NAME(database_id), end_of_log_lsn, last_commit_time, log_send_queue_size
   FROM sys.dm_hadr_database_replica_states WHERE is_local = 1;
   ```
   Run it on each surviving secondary and compare `end_of_log_lsn` (a higher value means less latency); pick the replica that is highest for your most important databases. You cannot assess loss while the cluster lacks quorum.
3. If the cluster lost quorum, force quorum on the DR node first: `Start-ClusterNode -Name dr01 -FixQuorum` (or `net start clussvc /forcequorum`).
4. On the chosen secondary:
   ```sql
   ALTER AVAILABILITY GROUP [AG1] FORCE_FAILOVER_ALLOW_DATA_LOSS;
   ```
5. Other secondaries are now SUSPENDED. Resume each database on each secondary:
   ```sql
   ALTER DATABASE appdb SET HADR RESUME;
   ```
6. When the old primary returns, it becomes a secondary with suspended data movement. If you need
   to salvage its lost transactions, create a database snapshot on it **before** resuming, compare, then resume.
7. Reset quorum votes and node weights, take a fresh full/log backup chain check, and update clients if they did not use the listener.

## After any failover
- Logins, Agent jobs, linked servers, credentials must already exist on the new primary (sync them with dbatools `Copy-DbaLogin`, `Copy-DbaAgentJob`).
- Jobs should check `sys.fn_hadr_is_primary_replica('appdb')` so they run only on the primary.

## Gotchas
- Automatic failover does not happen when the secondary is not SYNCHRONIZED (e.g. after a long redo backlog); check `is_failover_ready` regularly, not during the incident.
- WSFC failure threshold: by default n-1 failures (n = WSFC nodes) in a six-hour period, after which the cluster stops trying automatic failover and the AG resource stays failed until you bring it online or fail over manually.
- Before forcing, stop clients reaching the old primary (split-brain risk), and take a log backup after each extra forced failover in a series.

## Verify
Quarterly drill of planned failover; a written forced-failover runbook with the data-loss estimate query.

## Checked

2026-10-22. Documentation release checked: SQL Server 2025 (17.x) via learn.microsoft.com (ver17 pages; 2022 noted where relevant).
Confirmed: ALTER AVAILABILITY GROUP page (FAILURE_CONDITION_LEVEL default 3, HEALTH_CHECK_TIMEOUT default 30000 and minimum 15000, DB_FAILOVER meaning), flexible failover policy page (n-1 failures per six hours, suspect/damaged databases not detected), forced manual failover page (FORCE_FAILOVER_ALLOW_DATA_LOSS, all secondaries suspended and resumed manually, snapshot advice, end_of_log_lsn comparison, split-brain warning), force-quorum page (Start-ClusterNode -FixQuorum, net start clussvc /forcequorum), sys.dm_hadr_database_replica_cluster_states columns (database_name and is_failover_ready; no synchronization_state_desc), sys.fn_hadr_is_primary_replica, dbatools Copy-DbaLogin and Copy-DbaAgentJob. Wrong in the draft: the planned-failover query used columns that do not exist in that DMV, the failure threshold was stated as 3 in 6 hours, and the contained-AG/DAG forced-failover sentence had no source and was removed.
Method: documentation only; no commands were run.
