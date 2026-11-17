---
id: computing-software.database-administration.oracle-database.tablespace-management-bigfile-and-autoextend
name: tablespace-management-bigfile-and-autoextend
category: computing-software
field: database-administration
product: oracle-database
tags: [database-administration, oracle, oracle-database, oracle-tablespaces, datafiles, bigfile-tablespace, autoextend, ora-01653, omf, resize-datafile]
level: practitioner
status: docs-checked
description: "Create and grow Oracle tablespaces (smallfile vs bigfile, AUTOEXTEND with MAXSIZE, RESIZE), and know the DB_FILES limit and ORA-01653 meaning."
sources:
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/admin/managing-tablespaces.html
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/admin/managing-data-files-and-temp-files.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tablespaces: bigfile, autoextend, growth

**Goal:** tablespaces never run out unexpectedly, and growth is planned rather than fixed in an emergency.

## Smallfile vs bigfile
- A **bigfile** tablespace has a single data file of up to 4G blocks. It reduces the number of data files to manage
  and suits very large databases and logical volume managers.
- A traditional **smallfile** tablespace can hold several data files, which cannot be as large.
- Create one with `CREATE BIGFILE TABLESPACE ...`.

```sql
CREATE BIGFILE TABLESPACE app_data DATAFILE '<PATH>/app_data01.dbf' SIZE 10G AUTOEXTEND ON NEXT 1G MAXSIZE 2T;
CREATE TABLESPACE app_idx DATAFILE '<PATH>/app_idx01.dbf' SIZE 5G AUTOEXTEND ON NEXT 512M MAXSIZE 30G;
```
With Oracle Managed Files, omit the file name (see the OMF skill).

## Grow
- Autoextend: add `AUTOEXTEND ON [NEXT size] [MAXSIZE size]` when creating the file, or change it on an existing file
  with `ALTER DATABASE DATAFILE ... AUTOEXTEND ...`. For a bigfile tablespace use `ALTER TABLESPACE ... AUTOEXTEND`.
- Resize manually: `ALTER DATABASE DATAFILE '<PATH>' RESIZE 20G;`. For a bigfile tablespace use
  `ALTER TABLESPACE app_data RESIZE 3T;`.
- Smallfile: `ALTER TABLESPACE app_idx ADD DATAFILE '<PATH>' SIZE 10G;`. You cannot add a data file to a bigfile
  tablespace, and `DROP DATAFILE` does not work on one.
- `DB_FILES` sets the maximum number of data files for the instance. If it is too low you cannot add files without a
  restart (a changed value takes effect only after restart); too high wastes SGA memory. Bigfile tablespaces help
  keep the file count down.

## ORA-01653
`ORA-01653: unable to extend table <owner>.<table> by <n> in tablespace <name>` means the segment could not get space
in that tablespace. Add or resize a file, or raise `MAXSIZE`, then find which segment grew and why. Also confirm the
file system or disk group has room for autoextend to happen.

## Gotchas
- `MAXSIZE UNLIMITED` on a shared file system lets one tablespace consume the disk for everyone; set a `MAXSIZE`.

## Verify
Each data file has the intended autoextend settings and maximum size, and your monitoring alerts on a tablespace
approaching its maximum size.

## Checked
Date: 2026-11-09. Confirmed against the Oracle 19c Administrator's Guide chapters "Managing Tablespaces" and "Managing
Data Files and Temp Files" (read by targeted search of the fetched pages, not line by line): bigfile definition and
4G-block limit, CREATE BIGFILE, AUTOEXTEND and RESIZE rules, no ADD or DROP DATAFILE for bigfile, `DB_FILES`
behaviour, ORA-01653 text. Removed (not confirmed): 1022-file and 32 GB / 32 TB figures, 23ai default claim, RMAN
`SECTION SIZE` remark, `DBA_TABLESPACE_USAGE_METRICS` query and thresholds, `ORA-03297` note, `v$asm_diskgroup` check,
ORA-01652 and ORA-01688.
Method: documentation only; no commands were run.
