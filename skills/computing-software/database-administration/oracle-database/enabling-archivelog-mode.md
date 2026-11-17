---
id: computing-software.database-administration.oracle-database.enabling-archivelog-mode
name: enabling-archivelog-mode
category: computing-software
field: database-administration
product: oracle-database
tags: [database-administration, oracle-database, oracle-instance, archivelog-mode, log-archive-dest, fast-recovery-area, force-logging, ora-00257]
level: practitioner
status: docs-checked
description: "Put an Oracle database in ARCHIVELOG mode, configure archive destinations or the FRA, enable force logging, and recover from ORA-00257 archiver stuck."
sources:
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/admin/managing-archived-redo-log-files.html
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/refrn/LOG_ARCHIVE_DEST_n.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Enabling ARCHIVELOG mode

Without ARCHIVELOG mode you can only restore to the last cold backup: no online backups, no
point-in-time recovery, no Data Guard. Every production database should run in it.

## Check
```sql
SELECT log_mode, force_logging FROM v$database;
ARCHIVE LOG LIST            -- SQL*Plus
```

## Destination
Simplest: use the Fast Recovery Area (set both parameters):
```sql
ALTER SYSTEM SET db_recovery_file_dest_size = 500G SCOPE=BOTH;
ALTER SYSTEM SET db_recovery_file_dest = '+FRA' SCOPE=BOTH;
```
If you configure a FRA and specify no local archive destinations, the database selects the FRA and sets `LOG_ARCHIVE_DEST_1` to `USE_DB_RECOVERY_FILE_DEST`. Explicit form:
```sql
ALTER SYSTEM SET log_archive_dest_1 = 'LOCATION=USE_DB_RECOVERY_FILE_DEST' SCOPE=BOTH;
ALTER SYSTEM SET log_archive_format = '%t_%s_%r.arc' SCOPE=SPFILE;   -- %t thread, %s sequence, %r resetlogs ID (required); the parameter is ignored in some cases (e.g. server-managed names, see the guide)
```

## Switch the mode (requires a short outage)
```sql
SHUTDOWN IMMEDIATE;
STARTUP MOUNT;
ALTER DATABASE ARCHIVELOG;
ALTER DATABASE OPEN;
ALTER SYSTEM ARCHIVE LOG CURRENT;      -- confirm an archive is produced
```
The database must be mounted but not open to switch. For RAC, follow the Oracle RAC Administration and Deployment Guide.

Then **back up all database files and the control file**: the mode change updates the control file and any previous backup is no longer usable because it was taken in NOARCHIVELOG mode.

## Force logging
```sql
ALTER DATABASE FORCE LOGGING;
```
Logs all changes, so `NOLOGGING` requests do not leave unrecoverable blocks (for example `TRANSFORM=DISABLE_ARCHIVE_LOGGING` in Data Pump import has no effect in this mode). `V$DATABASE.FORCE_LOGGING` shows YES, NO or a STANDBY NOLOGGING mode.

## ORA-00257 / ORA-16038: archiver stuck
ORA-00257 "Archiver error. Connect AS SYSDBA only until resolved": ARCn failed to write a filled online redo log to a destination (FRA or destination out of space, or a MANDATORY destination failed); if not fixed the database stops processing transactions. ORA-16038 ("log ... cannot be archived") has the cause in secondary errors in the alert log and trace files.
1. Check the alert log, then `SELECT name, space_limit, space_used, space_reclaimable FROM v$recovery_file_dest;` and `SELECT dest_id, status, error FROM v$archive_dest WHERE status <> 'INACTIVE';`.
2. Free space safely with RMAN so only backed-up files are removed: `DELETE OBSOLETE;` or `DELETE ARCHIVELOG ALL COMPLETED BEFORE 'SYSDATE-1' BACKED UP 1 TIMES TO DEVICE TYPE DISK;`, or raise `db_recovery_file_dest_size` if disk exists.
3. Do not delete archived logs manually with `rm` unless they are backed up and RMAN has no record of them. For a failed MANDATORY destination fix the cause, then `ALTER SYSTEM SET log_archive_dest_state_2 = ENABLE;`. Then `ALTER SYSTEM ARCHIVE LOG CURRENT;`. Monitor FRA usage (alert around 80-85%).

## Verify
`ARCHIVE LOG LIST` shows `Database log mode: Archive Mode`, `Automatic archival: Enabled`, and
`v$archived_log` gets a new row at each log switch; archive logs are backed up and removed by an RMAN job.

## Checked
Date 2026-10-22. Oracle Database 19c Administrator's Guide (managing archived redo log files), Oracle error help
(ORA-00257, ORA-16038) and Database Reference (V$DATABASE). Confirmed: mount-not-open requirement and ALTER DATABASE
ARCHIVELOG steps, backup-after-switch statement, FRA automatic LOG_ARCHIVE_DEST_1 behaviour, LOG_ARCHIVE_FORMAT variables
and `%r` requirement, ARCHIVE LOG LIST output, ORA-00257/ORA-16038 text and recovery steps, V$DATABASE columns and
FORCE_LOGGING values. Removed (not in the pages read): the RAC srvctl commands, `v$recovery_area_usage`,
`BACKUP ARCHIVELOG ALL DELETE INPUT`, CROSSCHECK advice, "required for Data Guard" claim for force logging, "size first" ordering.
Method: documentation only; no commands were run.
