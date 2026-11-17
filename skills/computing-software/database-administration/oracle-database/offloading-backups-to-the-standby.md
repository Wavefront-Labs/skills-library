---
id: computing-software.database-administration.oracle-database.offloading-backups-to-the-standby
name: offloading-backups-to-the-standby
category: computing-software
field: database-administration
product: oracle-database
tags: [database-administration, oracle-database, oracle, standby-backup-offload, data-guard, rman, recovery-catalog, db-unique-name, archivelog-deletion-policy]
level: advanced
status: docs-checked
description: "Run Oracle RMAN backups on a physical standby to offload the primary, with a recovery catalog so backups are usable on any database in the Data Guard configuration."
sources:
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/sbydb/using-rman-to-back-up-and-restore-files.html
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/bradv/configuring-rman-client-advanced.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Offloading backups to the standby

Datafile and archived log backups taken on a physical standby are interchangeable with the
primary's (same DBID, block-for-block copies). Taking them there removes backup IO from the primary.

## Requirements
- A **recovery catalog**, so every database in the configuration sees backups taken by the others
  (control files only know their own).
- Each database registered by `db_unique_name`; configure per-site settings with `FOR DB_UNIQUE_NAME`.

## Configure (connected to catalog and to the primary)
```
$ rman target sys@orcl catalog rco@rcat
RMAN> REGISTER DATABASE;                         -- once, from the primary
RMAN> CONFIGURE DB_UNIQUE_NAME orcl_dr CONNECT IDENTIFIER 'orcl_dr';
RMAN> CONFIGURE DEFAULT DEVICE TYPE TO SBT FOR DB_UNIQUE_NAME orcl_dr;
RMAN> CONFIGURE CHANNEL DEVICE TYPE SBT PARMS 'SBT_LIBRARY=<MML_LIB>' FOR DB_UNIQUE_NAME orcl_dr;
RMAN> CONFIGURE RETENTION POLICY TO RECOVERY WINDOW OF 14 DAYS;
RMAN> LIST DB_UNIQUE_NAME OF DATABASE;
```

## Back up on the standby
```
$ rman target sys@orcl_dr catalog rco@rcat
RMAN> BACKUP INCREMENTAL LEVEL 0 DATABASE PLUS ARCHIVELOG;     -- weekly
RMAN> BACKUP INCREMENTAL LEVEL 1 DATABASE PLUS ARCHIVELOG;     -- daily
RMAN> DELETE NOPROMPT OBSOLETE;
```
Control file and spfile: back them up **on the primary** too (`BACKUP CURRENT CONTROLFILE; BACKUP SPFILE;`) because a
standby control file backup restores as a standby control file. Archived logs: backing up on
the standby is fine; make sure the standby is not lagging or backups miss recent redo.

## Restore on the primary from standby backups
Connected to the primary and catalog, RMAN sees the standby's pieces (if the media is reachable from the primary host):
```
RMAN> RESTORE DATAFILE 7; RECOVER DATAFILE 7;
```
With disk backups, the files must be accessible at the same path (shared NFS / object storage) or re-cataloged.
Alternative without backups: `RESTORE DATAFILE 7 FROM SERVICE orcl_dr;` (12c+, over the network).

## Gotchas
- Without a catalog, the primary's `REPORT NEED BACKUP` thinks nothing is backed up.
- Apply lag at backup time = backup point is behind; check `v$dataguard_stats` before running.
- Snapshot standby state: back up only when converted back to physical standby.

## Verify
`LIST BACKUP SUMMARY` from the primary shows the standby's backups, and a restore test on the primary site from those backups succeeds.

## Checked

2026-10-28. Confirmed against the cited Oracle documentation: FOR DB_UNIQUE_NAME, CONFIGURE ... CONNECT IDENTIFIER, RESTORE ... FROM SERVICE from a physical standby, block change tracking exists as a feature (Backup and Recovery User Guide; Data Guard Concepts, using RMAN to back up and restore files).

Removed or corrected: standby BCT/Active Data Guard requirement and the ARCHIVELOG DELETION POLICY ... APPLIED ON ALL STANDBY lines (not found in the cited pages).

Method: documentation only; no commands were run.
