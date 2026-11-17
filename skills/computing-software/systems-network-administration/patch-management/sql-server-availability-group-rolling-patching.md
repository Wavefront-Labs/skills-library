---
id: computing-software.systems-network-administration.patch-management.sql-server-availability-group-rolling-patching
name: sql-server-availability-group-rolling-patching
category: computing-software
field: systems-network-administration
product: patch-management
tags: [availability-group-patching, sql-server, always-on, rolling-upgrade, patch-deployment, patch-management]
level: practitioner
status: docs-checked
description: "Patch SQL Server Always On availability groups with minimal downtime: secondaries first, synchronous commit check, manual failover, then former primary, then verify."
sources:
  - https://learn.microsoft.com/en-us/sql/database-engine/availability-groups/windows/upgrading-always-on-availability-group-replica-instances
  - https://learn.microsoft.com/en-us/sql/database-engine/availability-groups/windows/perform-a-planned-manual-failover-of-an-availability-group-sql-server
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SQL Server Always On AG rolling patching

Primary downtime is one planned manual failover (two if you fail back) instead of the full update.

## Order
1. Remote / asynchronous secondaries first.
2. Synchronous secondaries.
3. Fail over to a patched synchronous secondary.
4. Patch the former primary.
5. Optionally fail back.

## Pre-checks
```sql
SELECT ag.name, ar.replica_server_name, ars.role_desc, ar.availability_mode_desc,
       drs.synchronization_state_desc, drs.log_send_queue_size, drs.redo_queue_size
FROM sys.availability_groups ag
JOIN sys.availability_replicas ar ON ag.group_id = ar.group_id
JOIN sys.dm_hadr_availability_replica_states ars ON ar.replica_id = ars.replica_id
LEFT JOIN sys.dm_hadr_database_replica_states drs ON ar.replica_id = drs.replica_id;
```
All databases SYNCHRONIZED on the failover target. Before starting: practise a manual failover on a synchronous-commit replica, take a full backup of every availability database, run `DBCC CHECKDB` on each, and set the automated backup preference to primary-only for a version upgrade (no replica is readable or available for backups then). Remove automatic failover from synchronous-commit replicas so the AG does not fail over mid-update.
```sql
ALTER AVAILABILITY GROUP [AG1] MODIFY REPLICA ON 'SQL02' WITH (FAILOVER_MODE = MANUAL);
```

## Patch a secondary
Install the update (unattended options are on Microsoft's command-prompt install page), reboot, confirm it rejoins and resynchronises. A secondary being updated is not available for failover or read-only use, and may need time to catch up afterwards (expect high network traffic).

## Failover
```sql
-- on the target secondary
ALTER AVAILABILITY GROUP [AG1] FAILOVER;
```
Or `Switch-SqlAvailabilityGroup -Path SQLSERVER:\Sql\SQL02\DEFAULT\AvailabilityGroups\AG1`.
Async replicas: switch to synchronous first, wait for SYNCHRONIZED, then fail over (avoid `FORCE_FAILOVER_ALLOW_DATA_LOSS`). Failing over to an asynchronous-commit replica risks data loss and suspends data movement until you resume it.

## Finish
Patch old primary, restore `FAILOVER_MODE = AUTOMATIC`, return async replicas to async, resume data movement where it was suspended.

## Gotchas
- After the first failover to a newer-version replica the databases run an upgrade process and no replica is readable meanwhile. An upgraded primary cannot ship logs to a replica on a lower version, so data movement stops until that replica is updated; you may need to resume synchronisation. Mixed versions are supported only during a rolling upgrade, so do not leave them longer than needed.
- Distributed AGs have their own order (upgrade secondaries, fail over the forwarder, then the global primary).
- For databases with change data capture or replication, check the update's release notes: `sp_vupgrade_replication` may be needed on the new primary (not on SQL Server 2019 CU1 or later).
- Cluster-Aware Updating is not supported for updating availability groups; use the order above.

## Verify
Same build on all replicas, all DBs SYNCHRONIZED/HEALTHY, failover modes restored.

## Checked
2026-10-28. Confirmed against Microsoft Learn: Upgrade availability group replicas (order, pre-checks, backup preference, synchronous-commit failover target, CAU unsupported, mixed versions, distributed AG, CDC and replication step), Perform a planned manual failover (ALTER AVAILABILITY GROUP FAILOVER, Switch-SqlAvailabilityGroup, SYNCHRONIZED requirement), ALTER AVAILABILITY GROUP (FAILOVER_MODE values) and the catalog view and DMV pages for every column in the pre-check query. Removed: downtime duration, installer command line, script-upgrade-mode claim, reversed claim about the old primary's readability, SERVERPROPERTY check.
Method: documentation only; no commands were run.
