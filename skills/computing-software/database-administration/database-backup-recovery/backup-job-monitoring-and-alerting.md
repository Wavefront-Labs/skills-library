---
id: computing-software.database-administration.database-backup-recovery.backup-job-monitoring-and-alerting
name: backup-job-monitoring-and-alerting
category: computing-software
field: database-administration
product: database-backup-recovery
tags: [database-administration, backup-strategy, point-in-time-recovery, backup-monitoring, backup-freshness, wal-archive-lag, dead-mans-switch, prometheus-alerts, msdb-backupset, pgbackrest-info]
level: practitioner
status: draft
description: "Alert on backup freshness, size anomalies and archive lag (not just job failure exit codes) for PostgreSQL, MySQL, SQL Server and Oracle, with a dead-man's-switch pattern."
sources:
  - https://pgbackrest.org/command.html#command-info
  - https://learn.microsoft.com/en-us/sql/relational-databases/system-tables/backupset-transact-sql
  - https://prometheus.io/docs/practices/alerting/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Backup monitoring and alerting

**Goal:** you learn that backups stopped within hours, not on the day you need a restore.

## Alert on outcomes, not on job runs
A job that never starts produces no failure email. Monitor the **age of the
newest good backup** and the **WAL/binlog/log-backup lag**:
| Signal | Threshold example |
|---|---|
| Newest full/incremental backup age | > 26 h for daily |
| Newest log/WAL archived age | > 15 min (PITR RPO) |
| Backup size vs previous | < 50% or > 200% (empty DB? runaway growth?) |
| Backup duration | > 2x median (will overlap next window) |
| Last restore test age | > 30 days |

## Where to read it
- **pgBackRest**: `pgbackrest --stanza=main --output=json info` → last backup
  `timestamp.stop`, `archive.max`; `SELECT last_archived_time, failed_count FROM pg_stat_archiver;`
- **MySQL/XtraBackup**: backup tool writes `xtrabackup_info` with end time; binlog
  streamer process alive and last file age.
- **SQL Server**:
  ```sql
  SELECT d.name, MAX(CASE WHEN b.type='D' THEN b.backup_finish_date END) AS last_full,
         MAX(CASE WHEN b.type='L' THEN b.backup_finish_date END) AS last_log
  FROM sys.databases d LEFT JOIN msdb.dbo.backupset b ON b.database_name = d.name
  WHERE d.name <> 'tempdb' GROUP BY d.name;
  ```
- **Oracle RMAN**: `SELECT end_time, status, input_type FROM v$rman_backup_job_details ORDER BY end_time DESC;`
- Cloud snapshots: provider APIs (latest recovery point per resource).

## Dead-man's switch
Have each successful backup push a heartbeat (Prometheus Pushgateway metric
`backup_last_success_timestamp_seconds`, or a healthchecks.io-style ping).
Alert when `time() - backup_last_success_timestamp_seconds > 93600`. Silence of
the job itself then pages.

## Gotchas
- New databases added later are often missing from backup jobs: alert on any
  database with **no** backup record (the LEFT JOIN above shows NULLs).
- Success exit code with zero-byte output happens (permissions, full disk on
  compression step): check size.
- Alerts must reach a human rota, not a shared mailbox.

## Verify
Disable a backup job in staging and confirm the freshness alert fires within the threshold.
