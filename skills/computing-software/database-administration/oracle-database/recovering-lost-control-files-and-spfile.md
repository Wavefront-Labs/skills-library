---
id: computing-software.database-administration.oracle-database.recovering-lost-control-files-and-spfile
name: recovering-lost-control-files-and-spfile
category: computing-software
field: database-administration
product: oracle-database
tags: [database-administration, oracle-database, oracle, rman, restore-controlfile, restore-spfile, controlfile-autobackup, dbid, open-resetlogs, disaster-recovery]
level: advanced
status: docs-checked
description: "Recover an Oracle database after losing all control files and/or the spfile: find the DBID, restore from autobackup, recover, and OPEN RESETLOGS."
sources:
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/bradv/rman-recovery-advanced.html
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/bradv/rman-performing-flashback-dbpitr.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Recovering lost control files and spfile

## 1. Know the DBID
Autobackup restore without a catalog needs the DBID. Record it now (`SELECT dbid FROM v$database;`)
in the runbook. If lost: it is in RMAN log headers ("connected to target database: ORCL (DBID=...)"),
and in the autobackup file name with `%F` format: `c-1234567890-20261018-00` (DBID 1234567890).

## 2. Spfile lost too
```
$ rman target /
RMAN> STARTUP FORCE NOMOUNT;      -- starts with a dummy parameter file if none is found
RMAN> SET DBID 1234567890;
RMAN> RESTORE SPFILE FROM AUTOBACKUP;
-- non-default location:
RMAN> RESTORE SPFILE FROM '/backup/ORCL/c-1234567890-20261018-00';
-- or: SET CONTROLFILE AUTOBACKUP FORMAT FOR DEVICE TYPE DISK TO '/backup/ORCL/%F'; then RESTORE SPFILE FROM AUTOBACKUP;
RMAN> STARTUP FORCE NOMOUNT;      -- now with the real spfile
```
Restore to a pfile to edit it first: `RESTORE SPFILE TO PFILE '/tmp/initORCL.ora' FROM AUTOBACKUP;`.

## 3. Control files
```
RMAN> SET DBID 1234567890;        -- not needed with a recovery catalog
RMAN> RESTORE CONTROLFILE FROM AUTOBACKUP;
RMAN> ALTER DATABASE MOUNT;
RMAN> CATALOG START WITH '/backup/ORCL/' NOPROMPT;     -- backups newer than the restored control file
RMAN> RECOVER DATABASE;
RMAN> ALTER DATABASE OPEN RESETLOGS;
```
`RECOVER` applies archived and, if they are intact, online redo logs. If all current online redo
is intact you still must `OPEN RESETLOGS` after a backup control file. Recovery stops with
"RMAN-06054 media recovery requesting unknown log" when it runs out of logs: if online
logs exist, it applies them automatically; otherwise that is the end point.
With a catalog: `RESTORE CONTROLFILE;` (no DBID, no autobackup needed).

## 4. Afterwards
- Take a full backup immediately: the RESETLOGS creates a new incarnation (`LIST INCARNATION`).
- Tempfiles may need re-adding: `ALTER TABLESPACE temp ADD TEMPFILE SIZE 10G;` if `v$tempfile` is empty.
- Re-multiplex control files if paths changed.

## Only one of several copies lost
No RMAN needed: shut down, copy a surviving control file over the lost one (or remove it from
`control_files`), start up.

## No backup at all
Recreate with `CREATE CONTROLFILE` (see the SQL Language Reference for the rules), listing every
datafile, then recover and open the database.

## Verify
Database open, `v$database.resetlogs_time` updated, new full backup succeeded, `RESTORE DATABASE VALIDATE` passes.

## Checked

2026-10-28. Confirmed against the cited Oracle documentation: SET DBID, RESTORE SPFILE FROM AUTOBACKUP and TO PFILE, STARTUP FORCE NOMOUNT, autobackup %F format, RMAN-06054 (media recovery requesting unknown log), CREATE CONTROLFILE rules (Backup and Recovery User Guide).

Removed or corrected: BACKUP CONTROLFILE TO TRACE / NORESETLOGS recreate details, and the word archived in RMAN-06054 (the documented text is unknown log).

Method: documentation only; no commands were run.
