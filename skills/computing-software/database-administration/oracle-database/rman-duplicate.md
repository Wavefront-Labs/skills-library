---
id: computing-software.database-administration.oracle-database.rman-duplicate
name: rman-duplicate
category: computing-software
field: database-administration
product: oracle-database
tags: [database-administration, oracle-database, oracle, rman, rman-duplicate, active-database-duplication, backup-based-duplication, auxiliary-instance, db-file-name-convert, nofilenamecheck, database-clone, standby-creation]
level: advanced
status: docs-checked
description: "Clone an Oracle database with RMAN DUPLICATE from active database or backups: auxiliary instance prerequisites, file name conversion, PDB duplication."
sources:
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/rcmrf/DUPLICATE.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# RMAN DUPLICATE

**Goal:** a copy of a database (test refresh, restore rehearsal, or standby) built by RMAN rather than by
hand-restoring and renaming.

## Prepare the auxiliary (destination host)
1. RMAN connects as `AUXILIARY` to the duplicate's instance, which must be started `NOMOUNT`. You must configure
   a static listener to perform duplication. Source and duplicate are normally the same platform.
2. Active duplication: the source and auxiliary must use the same `SYS` and `SYSBACKUP` password, so both need
   password files with at least those two passwords. For a non-standby duplicate, RMAN overwrites the auxiliary
   password file only if you give `PASSWORD FILE`; for a standby it copies it by default. Connect to the source as
   `TARGET` with a user name and password even under OS authentication, and use the same credentials for the
   auxiliary.
3. A minimal parameter file; to duplicate a whole CDB or PDBs, the auxiliary must be a CDB (include
   `enable_pluggable_database=TRUE`) and RMAN connects to the root of both.
```
STARTUP NOMOUNT PFILE='$ORACLE_HOME/dbs/initTESTDB.ora';
```
If the duplicate is on the source host, set `CONTROL_FILES` and all `*_DEST` parameters so the source's files are
not overwritten. Without manually allocated or configured auxiliary channels, RMAN uses the source's channel
configuration. Copy the keystore by hand when duplicating encrypted tablespaces.

## Active database duplication (no backups needed)
```
rman target sys@PROD auxiliary sys@TESTDB
RUN {
  ALLOCATE CHANNEL c1 DEVICE TYPE DISK;  ALLOCATE CHANNEL c2 DEVICE TYPE DISK;
  ALLOCATE AUXILIARY CHANNEL a1 DEVICE TYPE DISK;  ALLOCATE AUXILIARY CHANNEL a2 DEVICE TYPE DISK;
  DUPLICATE TARGET DATABASE TO TESTDB
    FROM ACTIVE DATABASE USING COMPRESSED BACKUPSET SECTION SIZE 32G
    SPFILE
      SET db_unique_name='TESTDB'
      SET control_files='+DATA','+FRA'
      SET db_create_file_dest='+DATA'
      SET db_recovery_file_dest='+FRA'
    NOFILENAMECHECK;
}
```
- `USING BACKUPSET` makes the auxiliary pull data from the source with backup sets; `COMPRESSED` compresses the
  transfer; `SECTION SIZE` also implies backup-set active duplication. With backup sets, have at least as many
  auxiliary channels as target channels.
- `SPFILE` copies the source's server parameter file; `SET name value` changes parameters afterwards (like
  `ALTER SYSTEM SET`), and `DB_FILE_NAME_CONVERT` on the command overrides competing `SPFILE SET` file names.
- `NOFILENAMECHECK` stops RMAN checking whether files with the same names are in use; you are responsible for
  making sure the duplicate does not overwrite useful data.
- The `UNTIL` clause is not supported for active duplication.

## Backup-based duplication
The duplicate is created from existing backups, with or without a target or catalog connection. All backups and
archived logs must be accessible to the server session on the destination host. Without a target connection,
`BACKUP LOCATION` names a disk location (not the fast recovery area):
```
DUPLICATE DATABASE TO 'TEST' BACKUP LOCATION '/net/prod/backups' NOFILENAMECHECK;
```
Backup-based duplication accepts `untilClause` (time, SCN or log sequence) or `TO RESTORE POINT`; the end point
cannot be before the most recent `RESETLOGS`, and you cannot recover to the current SCN.

## Variations
- `SKIP TABLESPACE name` excludes a tablespace; `TABLESPACE name` includes only the listed ones. `SYSTEM`,
  `SYSAUX` and undo tablespaces cannot be skipped. `SKIP READONLY` excludes read-only tablespaces. `SKIP
  TABLESPACE` cannot be used with `FOR STANDBY`.
- `DUPLICATE ... PLUGGABLE DATABASE` duplicates PDBs to a new CDB; duplicating a PDB into an existing CDB needs
  active duplication, `COMPATIBLE` 18.0.0 or higher on both CDBs, local undo, an spfile and
  `REMOTE_RECOVERY_FILE_DEST` on the destination, which must be open read-write.
- `DUPLICATE TARGET DATABASE FOR STANDBY FROM ACTIVE DATABASE DORECOVER` creates a standby and recovers it,
  leaving it mounted.
- Non-OMF file names: use `DB_FILE_NAME_CONVERT` / `LOG_FILE_NAME_CONVERT`, or the clause on `DUPLICATE`; with
  OMF/ASM, convert the disk group name.

## Verify
- [ ] The duplicate opens and has the intended name and files.
- [ ] No jobs, links or integrations still point at the source.

## Checked
2026-11-09. Read the 19c RMAN `DUPLICATE` command reference (prerequisites, usage notes, syntax element table and
examples); the Backup and Recovery guide source was not read and was dropped. Removed because the pages do not state them: version tags (11g+/12c+/18c+ except the
`COMPATIBLE` values), the "faster than image copy" claim, `RESET` parameters and `sga_target`, the `(UR=A)` and
ORA-/RMAN- error notes, the `UNTIL TIME` example, post-refresh hardening advice and the `v$database` query.
Method: documentation only; no commands were run.
