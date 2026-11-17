---
id: computing-software.database-administration.oracle-database.moving-datafiles-online
name: moving-datafiles-online
category: computing-software
field: database-administration
product: oracle-database
tags: [database-administration, oracle-database, oracle-tablespaces, datafiles, move-datafile, storage-migration, asm-migration]
level: practitioner
status: docs-checked
description: "Relocate or rename Oracle datafiles while the database stays open with ALTER DATABASE MOVE DATAFILE, including filesystem-to-ASM moves and what it cannot do."
sources:
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/admin/managing-data-files-and-temp-files.html#GUID-FEB3D8E3-1BAC-4A1C-B2E3-9ACD29726BE2
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Moving datafiles online

Since 12c, `ALTER DATABASE MOVE DATAFILE` copies a datafile to a new location while users
keep reading and writing, then switches to the copy and (by default) deletes the original.

## Commands
```sql
-- by name or file number
SELECT file_id, file_name, tablespace_name, bytes/1024/1024 mb FROM dba_data_files ORDER BY file_id;

ALTER DATABASE MOVE DATAFILE '/u01/oradata/PROD/users01.dbf'
  TO '/u02/oradata/PROD/users01.dbf';

ALTER DATABASE MOVE DATAFILE 7 TO '+DATA';              -- filesystem -> ASM (OMF name generated)
ALTER DATABASE MOVE DATAFILE '/u01/oradata/PROD/x.dbf' TO '/u01/oradata/PROD/x_renamed.dbf';  -- rename
```

## Progress
```sql
SELECT sid, opname, sofar, totalwork, ROUND(sofar/totalwork*100, 1) pct, time_remaining
FROM v$session_longops WHERE opname LIKE 'Online data file move%' AND sofar < totalwork;
```

## Things to know
- Needs space for both copies during the move; I/O load roughly equals a full copy plus
  writes being mirrored to both files.
- Works for data files only: **temp files** (drop/add), **online redo logs** (add new groups,
  drop old), **control files** (spfile change + restart or RMAN) need other procedures.
- Older pre-12c method: take the tablespace offline (or the database mounted), `cp`/RMAN copy,
  `ALTER DATABASE RENAME FILE`, recover, online. Use only when online move is not available.

## Bulk moves
Generate statements:
```sql
SELECT 'ALTER DATABASE MOVE DATAFILE ' || file_id || ' TO ''+DATA'';' FROM dba_data_files
WHERE file_name LIKE '/u01/%';
```
Run a few in parallel sessions at most; monitor storage throughput.

## Verify
`dba_data_files.file_name` shows the new paths, `v$datafile` status `ONLINE`, the old files are
gone (unless KEEP), and an RMAN backup afterwards reads the new locations.

## Checked

2026-10-28. Confirmed against the cited Oracle documentation: ALTER DATABASE MOVE DATAFILE to rename or relocate online datafiles, progress via V$SESSION_LONGOPS opname Online data file move (Administrator Guide, renaming and relocating datafiles).

Removed or corrected: KEEP and REUSE examples, container advice, concurrent-operation restrictions and physical-standby behaviour (not found in the cited pages).

Method: documentation only; no commands were run.
