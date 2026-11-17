---
id: computing-software.database-administration.oracle-database.securefiles-lob-storage
name: securefiles-lob-storage
category: computing-software
field: database-administration
product: oracle-database
tags: [database-administration, oracle-database, oracle, securefiles, basicfiles, lob, clob, blob]
level: advanced
status: docs-checked
description: "Store Oracle LOBs as SecureFiles: storage clauses (in-row, cache, logging, retention), changing LOB storage, Data Pump LOB_STORAGE, and shrinking LOB segments."
sources:
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/adlob/LOB-storage-with-applications.html
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/admin/managing-space-for-schema-objects.html
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/sutil/datapump-import-utility.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SecureFiles LOB storage

SecureFiles are an alternative LOB storage format to BasicFiles. The `SECUREFILE` keyword is required in the
`STORE AS` clause to get them, and the Oracle examples assume the LOB tablespace is ASSM.

## Create
```sql
CREATE TABLE docs.document (
  doc_id NUMBER PRIMARY KEY,
  body   CLOB,
  file_  BLOB)
LOB (body) STORE AS SECUREFILE (TABLESPACE lob_data ENABLE STORAGE IN ROW CACHE READS)
LOB (file_) STORE AS SECUREFILE doc_file_seg (
  TABLESPACE lob_data
  DISABLE STORAGE IN ROW        -- large binaries
  NOCACHE LOGGING);
```
| Clause | Notes |
|---|---|
| `ENABLE STORAGE IN ROW` | the default; LOBs under about 4000 bytes (minus control information) are stored in the row, larger ones go out of line regardless of this clause |
| `CACHE` / `CACHE READS` / `NOCACHE` | buffer cache behaviour for LOB reads and writes |
| `LOGGING` / `NOLOGGING` / `FILESYSTEM_LIKE_LOGGING` | if omitted, a SecureFile inherits logging from its tablespace and a NOLOGGING tablespace gives `FILESYSTEM_LIKE_LOGGING`; that mode suits bulk loads you can restart |
| `RETENTION` | SecureFiles accept only `RETENTION` (not `PCTVERSION`); the default is `AUTO`; `MAX` needs a `MAXSIZE` in the storage clause and applies in flashback mode |
Out-of-line LOBs always use space in multiples of `CHUNK`, so a large `CHUNK` wastes space on small LOBs.
Use a dedicated tablespace for big LOB segments so their growth and backups are visible.

## Check existing LOBs
```sql
SELECT owner, table_name, column_name, segment_name, securefile
FROM dba_lobs WHERE owner = 'DOCS';
```

## Changing LOB storage
- `ALTER TABLE ... MOVE` can change `RETENTION`, `PCTVERSION`, `CACHE`/`NOCACHE`, logging, `STORAGE` and the
  tablespace of an existing LOB column.
- Data Pump import: `TRANSFORM=LOB_STORAGE:SECUREFILE` (or `BASICFILE`, `DEFAULT`, `NO_CHANGE`; `NO_CHANGE` is the
  default) recreates LOB segments with that storage for all tables in the job. It is not valid in transportable
  import jobs, and a `DB_SECUREFILE` setting in the init file can prevent SecureFiles storage.

## Shrinking
The Administrator's Guide shows `ALTER TABLE employees MODIFY LOB (perf_review) (SHRINK SPACE);` only as a BasicFiles
example; confirm SecureFiles support in the SQL Language Reference before relying on it. `SHRINK SPACE CASCADE` on the
table also shrinks dependent segments, and shrinking invalidates cursors unless `COMPACT` is used.

## Gotchas
- With the `RETENTION` property, old LOB versions are kept for the time set by `UNDO_RETENTION` for BasicFiles LOBs
  (Automatic Undo Management required); SecureFiles manage consistent-read data dynamically.
- Exadata pushdown applies to uncompressed, unencrypted LOBs and to LOBs with SecureFiles compression.

## Verify
`dba_lobs.securefile = 'YES'` for the target columns after a move or import.

## Checked
2026-11-09. Confirmed against the 19c SecureFiles and Large Objects Developer's Guide (LOB storage with applications),
the Administrator's Guide (reclaiming unused space) and the Utilities guide (Data Pump import `TRANSFORM`). Removed
as not stated on those pages: the `db_securefile = PREFERRED` default, the 11g/12c/21c version claims, compression
and deduplication clauses and their licensing, `ENCRYPT`, online `MOVE ONLINE` migration and redefinition, the
`LOBPREFETCH` and ORA-22924 notes, the `DBMS_SPACE` overload, and the segment-size query. The source
`using-oracle-LOB-storage.html` returned 404 and was dropped.
Method: documentation only; no commands were run.
