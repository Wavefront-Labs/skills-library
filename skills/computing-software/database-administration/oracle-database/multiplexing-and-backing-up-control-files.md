---
id: computing-software.database-administration.oracle-database.multiplexing-and-backing-up-control-files
name: multiplexing-and-backing-up-control-files
category: computing-software
field: database-administration
product: oracle-database
tags: [database-administration, oracle-database, oracle, controlfile-multiplexing, control-files, backup-controlfile-to-trace, controlfile-autobackup]
level: practitioner
status: docs-checked
description: "Multiplex Oracle control files on separate disks, back them up (RMAN autobackup, binary copy, trace script), and recover from losing one copy."
sources:
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/admin/managing-control-files.html
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/bradv/configuring-rman-client-basic.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Multiplexing and backing up control files

The control file is a small binary file recording the physical structure of the database: database name, names and
locations of data files and redo logs, creation timestamp, current log sequence number and checkpoint information.
It must be writable whenever the database is open. Without it the database cannot be mounted and recovery is
difficult.

## Multiplexing rules
Every database should have at least two control files, each on a different physical disk. Oracle also suggests
putting a copy on each disk that holds redo log members when the redo log is multiplexed.
- The database writes to every file in `CONTROL_FILES` but reads only the first one listed.
- If any listed control file becomes unavailable while open, the instance becomes inoperable and should be
  terminated. If a damaged copy is replaced from an intact copy, no media recovery is required.
- `V$CONTROLFILE` lists the control file names.

## Add or relocate a copy
1. Shut down the database.
2. Copy an existing control file to the new location with operating system commands.
3. Add the new name to `CONTROL_FILES` (in an SPFILE: `ALTER SYSTEM SET control_files = ... SCOPE = SPFILE` before
   shutdown).
4. Restart.

## Back up
Back up after creating the database and every time the physical structure changes: adding, dropping or renaming
data files, adding or dropping a tablespace or changing its read/write state, adding or dropping redo log files or
groups.
```sql
ALTER DATABASE BACKUP CONTROLFILE TO '<BACKUP_DIR>/control.bkp';   -- binary duplicate
ALTER DATABASE BACKUP CONTROLFILE TO TRACE;                        -- SQL script in a trace file; see the alert log
```
The trace script can be edited to re-create the control file. With RMAN:
```
RMAN> CONFIGURE CONTROLFILE AUTOBACKUP ON;
```
Autobackup is on by default. It runs whenever a backup record is added, and in ARCHIVELOG mode also when the
database structure metadata in the control file changes. It lets RMAN recover even if the control file, recovery
catalog and server parameter file are all lost. With no other destination configured, autobackups go to the fast
recovery area; the default disk format is `%F`.

## Lose one copy
With the instance shut down, overwrite the bad file with a good copy (`cp` of a surviving file), then `STARTUP`. If
the media failed permanently, copy to a new accessible location, replace the bad path in `CONTROL_FILES`, and
`STARTUP`. To restart quickly you can instead remove the bad file from `CONTROL_FILES` and rebuild it later.

## Lose all copies
If no backup exists you must create new control files with `CREATE CONTROLFILE` (also needed to change the database
name). Use `RESETLOGS` if you also lost redo log groups or renamed the database, otherwise `NORESETLOGS`; after a
`RESETLOGS` creation recover with `USING BACKUP CONTROL FILE` and open with `ALTER DATABASE OPEN RESETLOGS`. If an
RMAN autobackup exists, RMAN can restore the control file from it (see the Backup and Recovery guide).

## Verify
`SELECT name FROM v$controlfile;` shows at least two copies on separate disks, and a recent backup of the control
file exists.

## Checked
Date: 2026-11-09. Confirmed against the Oracle 19c Administrator's Guide chapter "Managing Control Files" (read in
part: sections 10.1 to 10.3.2, 10.5, 10.6) and the Backup and Recovery guide page "Configuring the RMAN Client" (read by
targeted search): contents, multiplexing behaviour, backup triggers, both backup statements, recovery steps, autobackup
default, trigger and location. Removed (not on those pages): ASM `RESTORE CONTROLFILE TO` example, `REUSE` option on the
backup statements, ORA-00210/00202, `control_file_record_keep_time` guidance, `LIST BACKUP OF CONTROLFILE`.
Method: documentation only; no commands were run.
