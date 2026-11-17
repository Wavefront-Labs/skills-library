---
id: computing-software.database-administration.sqlite.sqlite3-analyzer-space-reports
name: sqlite3-analyzer-space-reports
category: computing-software
field: database-administration
product: sqlite
tags: [database-administration, sqlite, sqlite3-cli, sqlite3-analyzer, dbstat, disk-usage, freelist, file-size, vacuum, auto-vacuum]
level: practitioner
status: verified
description: "Find what takes space in a SQLite file with sqlite3_analyzer and the dbstat virtual table, then reclaim free pages with VACUUM or incremental auto_vacuum."
sources:
  - https://sqlite.org/sqlanalyze.html
  - https://sqlite.org/dbstat.html
  - https://sqlite.org/pragma.html#pragma_auto_vacuum
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Where did the space go?

**Goal:** explain a 2 GB SQLite file: which tables and indexes, how much is free,
and how to get it back.

## sqlite3_analyzer
Separate binary from the sqlite.org download page ("sqlite-tools").
```bash
sqlite3_analyzer app.db > report.txt
```
The report (3.54.1 `sqlite3_analyzer.exe` from the sqlite-tools zip) opens with a file summary: page size, pages in the file, **pages on the freelist** (free space inside the file), bytes of user payload. Then it gives page counts per table and per index, and for each the entries, bytes of payload and metadata, average and maximum payload per entry, overflow entries and pages, and unused bytes on primary, index and overflow pages (there is no "fragmentation" line). On a 5,000-row test with half the rows deleted it showed 2 freelist pages and 576 pages for the table plus its index.

## dbstat from SQL (when the binary isn't available)
```sql
SELECT name, SUM(pgsize)/1024/1024 AS mb, SUM(unused)/1024/1024 AS unused_mb
FROM dbstat GROUP BY name ORDER BY mb DESC LIMIT 15;
PRAGMA page_count; PRAGMA page_size; PRAGMA freelist_count;
```
Requires a build with `SQLITE_ENABLE_DBSTAT_VTAB` (the 3.54.1 shell and the Python 3.50.4 module both listed `ENABLE_DBSTAT_VTAB`; the query ran as written).

## Reclaiming space
Deleting rows does not shrink the file; pages go to the freelist and are reused.
- `VACUUM;` rebuilds the file compactly. Needs free disk ~2x the database, takes
  an exclusive lock, and changes rowids of tables without INTEGER PRIMARY KEY (checked: after deleting rowids 1 to 3 from a keyless table, `VACUUM` renumbered the survivors from 1).
- `PRAGMA auto_vacuum = INCREMENTAL;` (must be set before tables are created,
  or followed by a VACUUM to take effect: set after tables existed, `PRAGMA auto_vacuum` still returned 0 until `VACUUM` made it 2), then periodically
  `PRAGMA incremental_vacuum(1000);` to release up to 1000 free pages (in the sqlite3 shell this pragma printed one empty row per page freed; a 3.09 MB file with all rows deleted shrank to 12 KB and `freelist_count` went to 0).
- `auto_vacuum = FULL` truncates on every commit but fragments the file; rarely the best choice.

## Typical findings
- A large index nobody uses (drop it).
- Large TEXT/BLOB columns with overflow pages: consider storing blobs outside or in a separate table.
- High freelist after a purge: incremental vacuum or a scheduled VACUUM.

## Verify
After cleanup, `PRAGMA freelist_count` is near zero and the file size dropped
accordingly (`page_count * page_size`).
