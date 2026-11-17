---
id: computing-software.database-administration.database-backup-recovery.point-in-time-recovery-and-restore-testing
name: point-in-time-recovery-and-restore-testing
category: computing-software
field: database-administration
product: database-backup-recovery
tags: [database-administration, database-backup-recovery, backup, restore, disaster-recovery, point-in-time-recovery, pitr, full-backup, incremental-backup, differential-backup, wal-archiving, binlog, transaction-log-backup, pgbackrest, barman, wal-g, xtrabackup, mysqldump, mysqlbinlog, rman, rpo, rto, retention, 3-2-1-backup, immutable-backup, object-lock, backup-encryption, restore-drill, backup-verification]
level: practitioner
status: draft
description: "Build a backup scheme with full, incremental and WAL/binlog archiving for point-in-time recovery, set retention and 3-2-1 copies, encrypt, and prove it with timed restore drills."
sources:
  - https://www.postgresql.org/docs/current/continuous-archiving.html
  - https://pgbackrest.org/user-guide.html
  - https://docs.percona.com/percona-xtrabackup/8.4/
  - https://dev.mysql.com/doc/refman/8.4/en/point-in-time-recovery.html
  - https://learn.microsoft.com/en-us/sql/relational-databases/backup-restore/back-up-and-restore-of-sql-server-databases
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Point-in-time recovery and restore testing — a backup is a restore you have timed

**Goal:** be able to restore any database to any second inside the retention window,
within a known time, from copies an attacker or a bad script cannot delete.

## 1. Set the targets first
- **RPO** (data you may lose) decides log shipping frequency: continuous WAL/binlog
  archiving gives seconds to minutes; nightly dumps give up to 24 h.
- **RTO** (time to be back) decides the method: restoring a 2 TB physical backup plus
  a day of logs can take hours. If that is too slow, add a standby (see
  computing-software.database-administration.replication-high-availability.failover-and-replica-design)
  or delayed replica; backups are for what replication can't fix (deleted data,
  corruption, ransomware).

## 2. The building blocks
| Layer | PostgreSQL | MySQL | SQL Server |
|---|---|---|---|
| Full physical | pgBackRest/Barman/WAL-G `full`, `pg_basebackup` | Percona XtraBackup, MySQL Enterprise Backup | `BACKUP DATABASE` |
| Incremental/diff | pgBackRest `diff`/`incr`; `pg_basebackup --incremental` (17+) | XtraBackup `--incremental-basedir` | `WITH DIFFERENTIAL` |
| Log for PITR | WAL archiving (`archive_mode=on`, `archive_command`/`archive_library`) | binary logs (`log_bin`, `binlog_format=ROW`, GTIDs) | `BACKUP LOG` every 5–15 min (FULL recovery model) |
Logical dumps (`pg_dump`, `mysqldump`, MySQL Shell `util.dumpInstance`)
are useful for single-table recovery and version migrations but are not PITR.

Typical schedule: weekly full, daily incremental/differential, continuous log archive.
Example pgBackRest:
```ini
[global]
repo1-path=/var/lib/pgbackrest
repo1-retention-full=2
repo2-type=s3
repo2-s3-bucket=<BUCKET>
repo2-cipher-type=aes-256-cbc
repo2-cipher-pass=<PASSPHRASE_FROM_SECRET_STORE>
[main]
pg1-path=/var/lib/postgresql/17/main
```
`archive_command = 'pgbackrest --stanza=main archive-push %p'`; then
`pgbackrest --stanza=main --type=full backup` and `pgbackrest check`.

## 3. Doing the point-in-time restore
Postgres (pgBackRest):
```
pgbackrest --stanza=main --delta --type=time \
  --target="2026-10-01 09:55:00+00" --target-action=promote restore
```
MySQL: restore the XtraBackup (`--prepare`, then `--copy-back`), read the binlog
position from `xtrabackup_binlog_info`, then replay to just before the bad event:
```
mysqlbinlog --start-position=<POS> --stop-datetime="2026-10-01 09:55:00" \
  binlog.000123 binlog.000124 | mysql -u root -p
```
(With GTIDs use `--exclude-gtids`/`--include-gtids`; skip a single bad transaction
by stopping before it and resuming after it.)
SQL Server: `RESTORE DATABASE ... WITH NORECOVERY`, differential `WITH NORECOVERY`, logs
`WITH STOPAT = '2026-10-01T09:55:00', RECOVERY`.

Restore to a **separate** instance, extract what you need, and only overwrite
production when the whole database is lost. Find the exact bad moment first (app logs,
`pg_waldump`, `mysqlbinlog --verbose`).

## 4. Retention, copies and protection
- **3-2-1:** three copies, two media/storage systems, one off-site. Add **1 immutable**
  (S3 Object Lock in compliance mode, or equivalent WORM) and a different account or
  credentials from production, so ransomware with database credentials can't delete it.
- Retention: e.g. 14–35 days of PITR, monthly fulls for 12 months if compliance needs
  them. Retention must keep the full *and* all logs since it, or the chain is useless.
- Encrypt at rest and in transit; keep keys/passphrases in a secrets manager *and*
  an offline escrow. A backup whose key died with the server is lost.
- Alert on: archive failures (Postgres `pg_stat_archiver.failed_count`, growing
  `pg_wal`), missed backup jobs, and backup size swinging by more than ~20%.

## 5. Restore drills (the actual verification)
- Automate a scheduled restore (weekly is good) of the latest backup plus logs to a
  scratch host; run `pg_amcheck`/`CHECK TABLE`/`DBCC CHECKDB`, row counts on key
  tables, and an application smoke query.
- Quarterly, run a full timed drill with a human following the runbook: pick a random
  target timestamp, restore, measure wall-clock against RTO, record gaps.
- Built-in checks help but are not drills: `pgbackrest verify`, RMAN
  `RESTORE ... VALIDATE`, `RESTORE VERIFYONLY` (SQL Server; validates readability, not
  data correctness).

## Verify
- [ ] RPO and RTO are written per database and the backup method meets both.
- [ ] Log archiving is continuous and alerting on failure.
- [ ] One copy is off-site, immutable and under separate credentials; keys are escrowed.
- [ ] Latest automated restore succeeded and passed integrity checks.
- [ ] Last timed PITR drill hit the target timestamp within RTO, and the runbook was updated.
