---
id: computing-software.database-administration.oracle-database.rman-backup-and-recovery
name: rman-backup-and-recovery
category: computing-software
field: database-administration
product: oracle-database
tags: [database-administration, oracle-database, oracle, rman, recovery-manager, backup, restore, recover, archivelog, fast-recovery-area, fra, db-recovery-file-dest, controlfile-autobackup, incremental-backup, level-0, level-1, block-change-tracking, restore-validate, crosscheck, retention-policy, point-in-time-recovery, pitr, data-guard, spfile, dbid]
level: advanced
status: docs-checked
description: "Configure RMAN with ARCHIVELOG, FRA, control file autobackup and incremental level 0/1 backups; validate them; and restore/recover a database, datafile or point in time."
sources:
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/bradv/index.html
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/rcmrf/index.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# RMAN backup and recovery — configure once, validate always, rehearse restores

**Goal:** an Oracle database that can be restored to any point inside its recovery
window, with the commands to do it already rehearsed.

## 1. Prerequisites
```sql
-- SQL*Plus as SYSDBA
SELECT log_mode FROM v$database;              -- must be ARCHIVELOG
ALTER SYSTEM SET db_recovery_file_dest_size = 500G SCOPE=BOTH;  -- set size first
ALTER SYSTEM SET db_recovery_file_dest = '+FRA' SCOPE=BOTH;     -- or a filesystem path
-- to enable archivelog: SHUTDOWN IMMEDIATE; STARTUP MOUNT;
-- ALTER DATABASE ARCHIVELOG; ALTER DATABASE OPEN;
ALTER DATABASE ENABLE BLOCK CHANGE TRACKING;  -- fast level 1 incrementals; check edition licensing
ALTER DATABASE FORCE LOGGING;                 -- if NOLOGGING ops would make backups useless
```
Record the **DBID** (`SELECT dbid FROM v$database;`) somewhere outside the server: you
need it to restore a control file without a catalog. Size the FRA for at least one
level 0, the incrementals and archived logs for the window, plus headroom; a full FRA
stops archiving and then hangs the database.

## 2. Persistent RMAN configuration
```
rman target /
CONFIGURE RETENTION POLICY TO RECOVERY WINDOW OF 14 DAYS;
CONFIGURE CONTROLFILE AUTOBACKUP ON;          -- on by default when COMPATIBLE is 12.2+ (CDB or standalone); verify
CONFIGURE BACKUP OPTIMIZATION ON;
CONFIGURE DEVICE TYPE DISK PARALLELISM 4 BACKUP TYPE TO COMPRESSED BACKUPSET;
CONFIGURE ARCHIVELOG DELETION POLICY TO BACKED UP 2 TIMES TO DISK;
CONFIGURE ENCRYPTION FOR DATABASE ON;          -- needs wallet/TDE or SET ENCRYPTION ON IDENTIFIED BY
SHOW ALL;
```
Compression levels above BASIC and encryption may require the Advanced Compression /
Advanced Security options: check licensing before enabling. With Data Guard, use
`APPLIED ON ALL STANDBY` for the archivelog deletion policy.

## 3. Backup schedule
Weekly level 0, daily level 1, archived logs every 15–60 minutes:
```
RUN {
  BACKUP INCREMENTAL LEVEL 0 DATABASE TAG 'L0_WEEKLY' PLUS ARCHIVELOG;
}
BACKUP INCREMENTAL LEVEL 1 DATABASE TAG 'L1_DAILY' PLUS ARCHIVELOG;
BACKUP ARCHIVELOG ALL NOT BACKED UP 1 TIMES;
DELETE NOPROMPT OBSOLETE;
```
Choose between differential and `CUMULATIVE` level 1 backups (size versus number of restore steps). A recovery catalog in a separate database keeps
history beyond `control_file_record_keep_time` (default 7 days) and is recommended
once you have several databases. Copy backup pieces off the host (tape/SBT, object
storage via the cloud backup module, or a separate filesystem): FRA on the same storage
array is not a backup of that array.

## 4. Validate without restoring
```
CROSSCHECK BACKUP; CROSSCHECK ARCHIVELOG ALL;
LIST BACKUP SUMMARY;  REPORT NEED BACKUP;  REPORT UNRECOVERABLE;
RESTORE DATABASE VALIDATE;                     -- reads every needed piece
RESTORE ARCHIVELOG FROM TIME 'SYSDATE-1' VALIDATE;
BACKUP VALIDATE CHECK LOGICAL DATABASE;        -- finds corrupt blocks in live files
```
Corruption found lands in `V$DATABASE_BLOCK_CORRUPTION`; fix with
`RECOVER CORRUPTION LIST;`.

## 5. Recovery recipes
Lost datafile (database stays open):
```
ALTER DATABASE DATAFILE 7 OFFLINE;   -- in SQL, or let RMAN do it
RESTORE DATAFILE 7; RECOVER DATAFILE 7;
ALTER DATABASE DATAFILE 7 ONLINE;
```
Whole database / point in time:
```
STARTUP NOMOUNT;
SET DBID <DBID>;                                     -- only if no catalog/control file
RESTORE CONTROLFILE FROM AUTOBACKUP;
ALTER DATABASE MOUNT;
RUN {
  SET UNTIL TIME "TO_DATE('2026-10-01 09:55:00','YYYY-MM-DD HH24:MI:SS')";
  RESTORE DATABASE;
  RECOVER DATABASE;
}
ALTER DATABASE OPEN RESETLOGS;
```
After `RESETLOGS` take a new level 0. For a single dropped table, use
`RECOVER TABLE ... UNTIL TIME ... AUXILIARY DESTINATION '<PATH>'` or Flashback
(`FLASHBACK TABLE ... TO BEFORE DROP`) before resorting to full PITR.

Rehearse the full restore on a separate host quarterly using `DUPLICATE ... FOR
STANDBY`/`DUPLICATE DATABASE` or a plain restore, and time it against your RTO.

## Verify
- [ ] `ARCHIVELOG` mode, FRA usage well below its size limit (`V$RECOVERY_AREA_USAGE`).
- [ ] `SHOW ALL` shows retention, autobackup ON and deletion policy as intended.
- [ ] DBID recorded off-host; backups copied off the primary storage.
- [ ] `RESTORE DATABASE VALIDATE` succeeds and `REPORT NEED BACKUP` is empty.
- [ ] A timed restore to a separate host succeeded within RTO in the last quarter.

## Checked
2026-11-01. Confirmed on the Oracle 19c RMAN reference CONFIGURE page (control file autobackup default for COMPATIBLE 12.2+, backup optimization, retention policy examples) and the CONTROL_FILE_RECORD_KEEP_TIME reference page (default 7 days). Removed: Data Recovery Advisor deprecation remark, version gate on RECOVER TABLE, differential-default wording and the 80% FRA threshold. RMAN command syntax (BACKUP, RESTORE, RECOVER, REPORT pages) checked for the clauses used.
Method: documentation only; no commands were run.
