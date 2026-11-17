---
id: computing-software.systems-network-administration.backup-and-recovery.oracle-rman-backup-and-restore
name: oracle-rman-backup-and-restore
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [rman, oracle, database-backup, archivelog, point-in-time-recovery, block-change-tracking]
level: advanced
status: gated
description: "Back up and restore Oracle databases with RMAN: archivelog mode, CONFIGURE defaults, level 0/1 incrementals, block change tracking, validation, and full or point-in-time restore."
sources:
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/bradv/index.html
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/rcmrf/index.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Oracle RMAN backup and restore

**Goal:** consistent, verifiable Oracle backups and a rehearsed restore, including point-in-time.

## Prerequisites
```sql
SELECT log_mode FROM v$database;        -- must be ARCHIVELOG for online backups
-- if NOARCHIVELOG: SHUTDOWN IMMEDIATE; STARTUP MOUNT; ALTER DATABASE ARCHIVELOG; ALTER DATABASE OPEN;
ALTER DATABASE ENABLE BLOCK CHANGE TRACKING USING FILE '+DATA/bct.f';   -- fast level 1
```
Set a Fast Recovery Area: `db_recovery_file_dest` and `db_recovery_file_dest_size`.

## Persistent config (rman target /)
```
CONFIGURE RETENTION POLICY TO RECOVERY WINDOW OF 14 DAYS;   -- example value; syntax unconfirmed (gated: unconfirmed, source is paywalled or blocked)
CONFIGURE CONTROLFILE AUTOBACKUP ON;
CONFIGURE DEVICE TYPE DISK PARALLELISM 4 BACKUP TYPE TO COMPRESSED BACKUPSET;
CONFIGURE ARCHIVELOG DELETION POLICY TO BACKED UP 2 TIMES TO DISK;   -- unconfirmed (gated: unconfirmed, source is paywalled or blocked)
SHOW ALL;
```

## Backups
```
BACKUP INCREMENTAL LEVEL 0 DATABASE PLUS ARCHIVELOG;      -- weekly
BACKUP INCREMENTAL LEVEL 1 DATABASE PLUS ARCHIVELOG;      -- daily (differential)
BACKUP ARCHIVELOG ALL NOT BACKED UP 1 TIMES;              -- every 15-60 min
CROSSCHECK BACKUP; DELETE NOPROMPT OBSOLETE;
REPORT NEED BACKUP; LIST BACKUP SUMMARY;
```
Media managers use `DEVICE TYPE SBT_TAPE` channels; check your vendor plug-in documentation for names and configuration (gated: unconfirmed, source is paywalled or blocked).

## Validate
```
BACKUP VALIDATE CHECK LOGICAL DATABASE ARCHIVELOG ALL;    -- syntax and effect unconfirmed (gated: unconfirmed, source is paywalled or blocked)
RESTORE DATABASE VALIDATE;                                -- proves backups are restorable
```

## Full restore (lost everything but backups)
```
SET DBID 1234567890;
STARTUP NOMOUNT;
RESTORE SPFILE FROM AUTOBACKUP;  STARTUP FORCE NOMOUNT;
RESTORE CONTROLFILE FROM AUTOBACKUP;
ALTER DATABASE MOUNT;
RESTORE DATABASE; RECOVER DATABASE;
ALTER DATABASE OPEN RESETLOGS;
```
Point-in-time: wrap in `RUN { SET UNTIL TIME "TO_DATE('2026-10-17 14:29','YYYY-MM-DD HH24:MI')"; RESTORE DATABASE; RECOVER DATABASE; }` then `OPEN RESETLOGS`.

## Gotchas
- Record the DBID somewhere outside the database; you need it to find autobackups.
- Without controlfile autobackup and a catalog, restores after total loss are painful.
- OS-level copies of open datafiles are not valid backups.

## Verify
Monthly `RESTORE DATABASE VALIDATE` plus a quarterly full restore to a test host with `OPEN RESETLOGS` and an application query.

## Checked
Date: 2026-11-02. The two Oracle Database 19c index pages cited as sources returned stub or near-empty content, and no readable RMAN command reference page was obtained, so the RMAN syntax in this skill (CONFIGURE, BACKUP INCREMENTAL, BACKUP VALIDATE, RESTORE ... VALIDATE, RESETLOGS and UNTIL TIME forms) is not confirmed against Oracle documentation. Marked gated: retention and deletion-policy syntax, validate commands, SBT_TAPE guidance. Verify every command in the current Oracle Database Backup and Recovery User's Guide and RMAN reference before use; restore procedures should be rehearsed by a qualified DBA.
Method: documentation only; no commands were run.
