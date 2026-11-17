---
id: computing-software.cybersecurity-defensive.security-architecture.point-in-time-recovery
name: point-in-time-recovery
category: computing-software
field: cybersecurity-defensive
product: security-architecture
tags: [point-in-time-recovery, pitr, wal-archiving, postgresql-backup, rds-pitr, sql-server-log-backup]
level: practitioner
status: docs-checked
description: "Configure and test database point-in-time recovery on PostgreSQL WAL archiving, Amazon RDS and SQL Server log restores: prerequisites, recovery targets, restore sequence and gaps."
sources: ["https://www.postgresql.org/docs/current/continuous-archiving.html", "https://pgbackrest.org/user-guide.html", "https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_PIT.html", "https://learn.microsoft.com/en-us/sql/relational-databases/backup-restore/restore-a-sql-server-database-to-a-point-in-time-full-recovery-model"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Database point-in-time recovery

A base or full backup restores one moment; PITR replays logs to stop at a chosen moment, such as just before a bad `DELETE`.

## PostgreSQL continuous archiving
- Enable: `wal_level` set to `replica` or higher, `archive_mode = on`, and either `archive_command` or `archive_library`, all in `postgresql.conf`. In `archive_command`, `%p` is the file path and `%f` the file name.
- You need a continuous sequence of archived WAL files from at least the start of your base backup. Test the archiving procedure before taking the first base backup.
- Choose the interval between base backups by how much archived WAL you will keep and how long replay may take.
- Restore: restore the base backup, remove stale files from `pg_wal/`, set recovery settings in `postgresql.conf`, create `recovery.signal` in the data directory, and start the server. `restore_command` is mandatory. Optionally restrict `pg_hba.conf` until you have checked the result. The server removes `recovery.signal` after recovery and then runs normally.
- Stop point (recovery target): by date/time, named restore point or transaction ID; the docs call only the first two practically usable. By default recovery runs to the end of the available WAL on the latest timeline; `recovery_target_timeline` selects another.
- Some archive failures (killed by a signal, exit status above 125, an ERROR or FATAL from the archive function) restart the archiver and are not reported in `pg_stat_archiver`.
- pgBackRest user guide examples: `archive_command = 'pgbackrest --stanza=demo archive-push %p'`, `stanza-create`, `--type=full backup`, `--delta restore`. The PostgreSQL log then shows `starting point-in-time recovery to <time>`. pgBackRest can also read a versioned repository as it was at an earlier time, to recover data deleted or corrupted by accident or malware.

## Amazon RDS
- Restore to a point in time creates a new DB instance and leaves the source untouched.
- RDS uploads transaction logs to S3 every five minutes. The `LatestRestorableTime` field of `describe-db-instances` shows the latest restorable time. Any time within the backup retention period can be chosen.
- CLI: `aws rds restore-db-instance-to-point-in-time` with `--source-db-instance-identifier`, `--target-db-instance-identifier` and `--restore-time` (or `--use-latest-restorable-time`). Storage cannot be reduced on restore.
- SQL Server on RDS: databases in one instance restore to within 1 second of each other, so cross-database transactions may be inconsistent. Changing the recovery model can break the log chain, so RDS does not support it.

## SQL Server (full or bulk-logged recovery model)
- Restore the full backup `WITH NORECOVERY`, then the last differential `WITH NORECOVERY`, then each log backup in creation order with `WITH STOPAT = <time>, RECOVERY`. Use `STOPAT` on each restore so you do not go past the target.
- If a log backup lacks the requested time, a warning is raised and the database stays unrecovered.
- Under bulk-logged, a log backup containing bulk-logged changes cannot be restored to a point inside it.
- Specify the point in time early in the sequence; `STANDBY` helps find an unknown time.

## Self-check
- [ ] A scratch restore to a chosen timestamp succeeds and the data matches expectation.
- [ ] You can name the earliest and latest restorable time for each database.

## Checked

Confirmed on the PostgreSQL continuous archiving page, the pgBackRest user guide, the RDS point-in-time page and the SQL Server point-in-time restore page. Removed because the pages do not state them: the `pgbackrest --type=time --target-action=promote` restore line (not on the cached page), MySQL binlog steps, 5 to 15 minute SQL Server log-backup cadence, RDS retention 1 to 35 days, Azure SQL and Cloud SQL, `pg_stat_archiver.failed_count` monitoring, immutable cross-account archives and the dwell-time retention advice.

Method: docs-only read of cited pages, 2026-11-08
