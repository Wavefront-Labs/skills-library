---
id: computing-software.database-administration.sqlite.online-backup-api-from-application-code
name: online-backup-api-from-application-code
category: computing-software
field: database-administration
product: sqlite
tags: [database-administration, sqlite, backup-api, sqlite-online-backup, sqlite3-backup-step, python-sqlite3-backup, hot-backup, dot-backup, vacuum-into]
level: practitioner
status: verified
description: "Take consistent hot backups of a live SQLite database from application code with the Online Backup API (incremental steps), instead of copying the file."
sources:
  - https://sqlite.org/backup.html
  - https://sqlite.org/c3ref/backup_finish.html
  - https://docs.python.org/3/library/sqlite3.html#sqlite3.Connection.backup
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Online backup API

**Goal:** a consistent copy of a database that other connections are writing to,
without stopping the app and without copying a half-written file.

## Why not `cp`
Copying `app.db` while it is written can produce a torn copy; in WAL mode, the
latest commits live in `app.db-wal` and a copy of the main file alone misses them.

## C API shape
```c
sqlite3_backup *b = sqlite3_backup_init(dest_db, "main", src_db, "main");
while ((rc = sqlite3_backup_step(b, 256)) == SQLITE_OK || rc == SQLITE_BUSY || rc == SQLITE_LOCKED)
    sqlite3_sleep(50);                 // copy 256 pages, then let writers proceed
sqlite3_backup_finish(b);
```
Each step copies N pages under a read lock. If another connection **writes**
the source between steps, the backup restarts from the beginning (unless the
writer uses the same connection). Small steps keep writers moving but risk
restarts on busy databases; `-1` copies everything in one step (holds the read
lock for the duration; with WAL mode readers do not block writers, so this is usually fine).

## Python
```python
import sqlite3
src = sqlite3.connect("app.db")
dst = sqlite3.connect("backup-2026-10-16.db")
with dst:
    src.backup(dst, pages=0, progress=lambda status, remaining, total: None)   # pages=0 means all at once
dst.close(); src.close()
```
Python's `pages` of 0 or less copies the database in a single step (docs); with `pages=10` on a 47-page file the progress callback fired 5 times and ended with status 101 (`SQLITE_DONE`).
Also available: Go (`mattn/go-sqlite3` `(*SQLiteConn).Backup`), .NET (`Microsoft.Data.Sqlite` `SqliteConnection.BackupDatabase`), sqlite3 shell `.backup backup.db`. The C loop above was run through ctypes against Python's `sqlite3.dll` (3.50.4): it finished with `SQLITE_DONE` and the copy had all 20,000 rows.

## Alternative: VACUUM INTO
`VACUUM INTO '/backups/app-2026-10-16.db';` (3.27+) writes a compacted,
transactionally consistent copy in one statement. Simpler, but always rewrites
the whole file and cannot be done incrementally. Unlike `backup()`, it fails if the target exists
(`output file already exists`, checked).

## Gotchas
- The destination is overwritten (a `backup()` onto an existing file with another table left only the source's table, checked); write to a temp name and rename when done.
- In a test, `Connection.backup()` on a connection that still had an uncommitted write blocked; commit or use a separate connection.
- For continuous off-site replication use Litestream instead of periodic backups.

## Verify
`PRAGMA integrity_check;` on the backup file returns `ok`, and row counts on key
tables match the source at backup time.
