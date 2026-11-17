---
id: computing-software.database-administration.database-backup-recovery.logical-vs-physical-backups
name: logical-vs-physical-backups
category: computing-software
field: database-administration
product: database-backup-recovery
tags: [database-administration, database-backup-recovery, logical-vs-physical-backup, logical-backup, physical-backup, backup-strategy, pg-dump]
level: practitioner
status: draft
description: "Choose between logical backups (pg_dump, mysqldump, Data Pump, mongodump) and physical backups (base backups, xtrabackup, RMAN, snapshots) by restore speed, granularity and PITR."
sources:
  - https://www.postgresql.org/docs/current/backup.html
  - https://dev.mysql.com/doc/refman/8.4/en/backup-types.html
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/bradv/getting-started-rman.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Logical vs physical backups

## Definitions
- **Logical**: data exported as SQL statements or a portable format (rows, DDL). `pg_dump`, `mysqldump`/`mysqlpump`/MySQL Shell dump utilities, Oracle Data Pump (`expdp`), `mongodump`, SQL Server BACPAC.
- **Physical**: copies of data files plus transaction logs. `pg_basebackup`/pgBackRest/Barman + WAL, Percona XtraBackup / MySQL Enterprise Backup, RMAN, SQL Server `BACKUP DATABASE`, storage snapshots.

## Comparison
| | Logical | Physical |
|---|---|---|
| Backup speed on large DBs | Slow (row by row) | Fast (file copy, incremental) |
| Restore speed | Slow: reload + rebuild indexes (hours per TB) | Fast: copy files back, replay logs |
| Point-in-time recovery | No (single moment) | Yes with archived logs |
| Granularity | Single table/schema easy | Whole cluster/instance (partial with effort) |
| Portability | Across versions, platforms, engines (with effort) | Same major version and platform |
| Detects corruption | Reading every row surfaces some corruption | Copies corrupt blocks faithfully (unless checksums verified) |
| Consistency | Snapshot per run (`--single-transaction`, MVCC) | Consistent via log replay |

## Typical strategy
- Physical backups + continuous log archiving as the **primary** recovery method (meets RPO minutes/seconds, RTO hours).
- Logical dumps as a **secondary**: object-level restores ("restore one table from last night"), migrations, major upgrades, long-term archives readable without the exact engine version, and as a corruption cross-check.

## Engine notes
- PostgreSQL: `pg_dump -Fd -j 8` parallel directory format; `pg_restore -j 8`; globals via `pg_dumpall --globals-only`.
- MySQL: `mysqldump --single-transaction --routines --triggers --events` (InnoDB only consistent); MySQL Shell `util.dumpInstance()` is parallel and much faster.
- Oracle: Data Pump for logical; RMAN for physical (only RMAN supports PITR/block recovery).
- SQL Server: native backups are physical; BACPAC/`bcp` for logical extracts.
- MongoDB: `mongodump --oplog` for a consistent point on replica sets; filesystem snapshots or Ops Manager/Atlas backups for physical.

## Verify
Restore both kinds regularly: time the full physical restore + PITR to a target time, and a single-table logical restore; record durations against the RTO.
