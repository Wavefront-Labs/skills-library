---
id: computing-software.database-administration.oracle-database.oracle-managed-files
name: oracle-managed-files
category: computing-software
field: database-administration
product: oracle-database
tags: [database-administration, oracle-database, oracle, oracle-managed-files, omf, db-create-file-dest, db-create-online-log-dest, db-recovery-file-dest, datafiles]
level: practitioner
status: docs-checked
description: "Use Oracle Managed Files (DB_CREATE_FILE_DEST, DB_CREATE_ONLINE_LOG_DEST_n) so Oracle names, creates and removes datafiles, redo logs and control files."
sources:
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/admin/using-oracle-managed-files.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Oracle Managed Files (OMF)

With OMF you give Oracle a file system directory or ASM disk group; it generates file names, creates files with
default sizes, and removes old OMF files automatically when they are no longer needed. OMF can manage data files, temp
files, control files, redo log files and archived logs.

## Parameters
```sql
ALTER SYSTEM SET db_create_file_dest = '<DATA_DIR>' SCOPE = BOTH;
ALTER SYSTEM SET db_create_online_log_dest_1 = '<LOG_DIR_1>' SCOPE = BOTH;
ALTER SYSTEM SET db_create_online_log_dest_2 = '<LOG_DIR_2>' SCOPE = BOTH;
ALTER SYSTEM SET db_recovery_file_dest_size = 20G SCOPE = BOTH;   -- set the size before the destination
ALTER SYSTEM SET db_recovery_file_dest = '<FRA_DIR>' SCOPE = BOTH;
```
- `DB_CREATE_FILE_DEST`: default directory or ASM disk group for data files and temp files when a create statement gives
  no file specification. It is also the default for redo log and control files if no `DB_CREATE_ONLINE_LOG_DEST_n` is set.
- `DB_CREATE_ONLINE_LOG_DEST_n`: location for redo log files and control files; each `n` (up to five) is one
  multiplexed copy. For redo and control files only, it overrides `DB_CREATE_FILE_DEST` and `DB_RECOVERY_FILE_DEST`.
  If you set it without `DB_CREATE_FILE_DEST`, only redo and control files can be OMF.
- `DB_RECOVERY_FILE_DEST` and `DB_RECOVERY_FILE_DEST_SIZE` identify the default Fast Recovery Area.
- On file systems, data file names follow `destination_prefix/o1_mf_%t_%u_.dbf`; the naming scheme for ASM is in
  the ASM Administrator's Guide.

## Defaults
- A permanent-tablespace OMF data file is 100 MB and autoextensible with unlimited maximum size. If you give `SIZE`
  without `AUTOEXTEND`, the file is not autoextensible.
- An OMF temp file is 100 MB, autoextensible, unlimited maximum.
- An OMF redo log file is 100 MB.
- When autoextending, the file grows by its current size or 100 MB, whichever is smaller, unless you set `NEXT`.

```sql
CREATE TABLESPACE tbs_1;                                                  -- OMF data file in the default location
CREATE TABLESPACE tbs_3 DATAFILE AUTOEXTEND ON MAXSIZE 800M;              -- 100 MB initial, capped at 800 MB
ALTER TABLESPACE tbs_1 ADD DATAFILE AUTOEXTEND ON MAXSIZE 800M;
```

## Control files at database creation
If `CONTROL_FILES` is not set and an OMF parameter is, Oracle creates OMF control files: in the
`DB_CREATE_ONLINE_LOG_DEST_n` locations if set (the first is primary); otherwise one in each of `DB_CREATE_FILE_DEST`
and `DB_RECOVERY_FILE_DEST` (the former primary), or one in whichever single parameter is set. If none are set, the
default is operating system dependent and those copies are not OMF.

## Gotchas
- Unlimited autoextend on the 100 MB default can fill a file system: set `MAXSIZE`.
- Multiplex redo and control files by setting more than one `DB_CREATE_ONLINE_LOG_DEST_n`.

## Verify
`SHOW PARAMETER db_create` shows the destinations, and creating then dropping a test tablespace shows OMF creating
and removing the file.

## Checked
Date: 2026-11-09. Confirmed against the Oracle 19c Database Administrator's Guide chapter "Using Oracle Managed Files"
(read by targeted search of the fetched page, not line by line): parameter roles, five-copy limit, precedence rules,
control file defaults, 100 MB defaults, autoextend growth, examples. Removed (not stated on that page): the `DROP
TABLESPACE ... INCLUDING CONTENTS` and `AND DATAFILES` remarks, `ALTER DATABASE MOVE DATAFILE`, standby
(`standby_file_management`, `db_file_name_convert`) and RMAN `SET NEWNAME` advice, PDB-level destination remark.
Method: documentation only; no commands were run.
