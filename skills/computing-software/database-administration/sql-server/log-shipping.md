---
id: computing-software.database-administration.sql-server.log-shipping
name: log-shipping
category: computing-software
field: database-administration
product: sql-server
tags: [database-administration, sql-server, mssql, log-shipping, warm-standby, disaster-recovery, restore-standby, norecovery, invoke-dbadblogshipping, log-shipping-monitor, always-on]
level: practitioner
status: docs-checked
description: "Set up and run SQL Server log shipping for warm standby DR: backup, copy and restore jobs, monitoring, failover, and role reversal."
sources:
  - https://learn.microsoft.com/en-us/sql/database-engine/log-shipping/about-log-shipping-sql-server
  - https://learn.microsoft.com/en-us/sql/database-engine/log-shipping/fail-over-to-a-log-shipping-secondary-sql-server
  - https://learn.microsoft.com/en-us/sql/database-engine/log-shipping/monitor-log-shipping-transact-sql
  - https://learn.microsoft.com/en-us/sql/relational-databases/system-tables/log-shipping-monitor-secondary-transact-sql
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Log shipping

**Goal:** a simple warm standby built from ordinary log backups, often used for DR or delayed copies alongside AGs.

## How it works
Agent jobs: **backup** on the primary (category "Log Shipping Backup"), **copy** and **restore** on each
secondary (categories "Log Shipping Copy" and "Log Shipping Restore"), plus an **alert** job (category "Log Shipping Alert")
on the monitor server. No automatic failover. The secondary is in the RECOVERING state or `STANDBY` (limited read-only access
in the interval between restore jobs). An optional monitor server records history; it must be added when you enable log shipping
and cannot be changed afterwards without removing log shipping.

## Set up
Prereqs: not SIMPLE recovery (FULL or BULK_LOGGED), a backup share the primary writes to and secondaries
read (service accounts need rights), the secondary initialised from a full backup.
SSMS: database Properties -> Transaction Log Shipping (Microsoft's Configure Log Shipping topic covers the wizard and the
`sp_add_log_shipping_*` stored procedures).
SQL Server 2025 adds TDS 8.0 / strict encryption options for log shipping; a remote SQL Server 2025 monitor with older
primary/secondary instances can break monitoring (drop and recreate the configuration).
Keep one log backup chain: another tool taking log backups of the same database means the restore job cannot apply a complete sequence.

## Delayed restore
A user-specified delay between the log backup and its restore on the secondary keeps a secondary behind, so an accidental
change noticed quickly can still be recovered from the secondary (an AG applies changes immediately).

## Monitor
```sql
EXEC msdb.dbo.sp_help_log_shipping_monitor_primary   @primary_server = N'<server>', @primary_database = N'appdb';    -- monitor or primary server
EXEC msdb.dbo.sp_help_log_shipping_monitor_secondary @secondary_server = N'<server>', @secondary_database = N'appdb'; -- monitor or secondary server
SELECT secondary_database, last_copied_file, last_restored_file, last_restored_latency, restore_threshold
FROM msdb.dbo.log_shipping_monitor_secondary;      -- latency is minutes from log backup to restore
```
The alert job raises errors when backup or restore misses its threshold; each alert has an alert number and must be configured
to notify an operator.

## Planned failover / role reversal
1. Copy any uncopied log backups to each secondary and apply all unapplied backups in sequence.
2. If the primary is accessible, back up the tail of its log `WITH NORECOVERY` (leaves it restoring, unavailable to users), e.g.
   `BACKUP LOG appdb TO DISK = '<share>\appdb_tail.trn' WITH NORECOVERY;` (single-user mode may be needed for exclusive access).
3. Apply the tail backup to the secondaries, then recover the secondary you chose (`RESTORE DATABASE appdb WITH RECOVERY`) and redirect clients.
4. Make the secondary's metadata (logins, jobs) consistent with the old primary; see Microsoft's topics on metadata after
   making a database available on another instance and on logins and jobs after role switching.
5. Reconfigure the recovered database as a primary for other secondaries; the old primary, left restoring by the tail backup,
   can be rolled forward from the new primary's log backups.

Unplanned: apply whatever log backups reached the secondary, then recover it. Data loss is everything not yet backed up and applied.

## Gotchas
- No automatic failover and no listener: plan client redirection.
- Read access to a `STANDBY` secondary is limited to the interval between restore jobs.
- Bulk-logged operations make log backups larger.
- Known issue (docs): for databases with memory-optimized tables, a tail-log backup with no recovery followed by a restore with recovery can hang the restore; restarting the instance first is the documented workaround.

## Verify
- [ ] `last_restored_latency` within RPO; alert jobs enabled and mailing.
- [ ] Logins and jobs exist on the secondary; failover runbook tested.

## Checked
Date 2026-10-23. Documentation release: SQL Server 2025 pages for About Log Shipping, Fail over to a log shipping secondary, Monitor Log Shipping and log_shipping_monitor_secondary.
Confirmed: job categories, monitor server rules, STANDBY behaviour, delayed restore, failover procedure with `WITH NORECOVERY` tail backup, monitoring procedures and `log_shipping_monitor_secondary` columns, 2025 TDS 8.0 note and monitor issue. Removed unconfirmed claims: Standard/Web edition support, LSBackup_ job names, error numbers 14420/14421, the dbatools command, a bare `sp_help_log_shipping_monitor` call, and role reversal without a new full backup.
Method: documentation only; no commands were run.
