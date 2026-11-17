---
id: computing-software.database-administration.sqlite.wal-mode-and-pragmas
name: wal-mode-and-pragmas
category: computing-software
field: database-administration
product: sqlite
tags: [database-administration, sqlite, sqlite3, embedded-database, pragma, journal-mode, wal, write-ahead-log, synchronous, busy-timeout, sqlite-busy, database-is-locked, foreign-keys, strict-tables, wal-checkpoint, wal-autocheckpoint, begin-immediate, cache-size, mmap-size, temp-store, optimize, integrity-check, network-filesystem, nfs, litestream, mobile-app-storage]
level: practitioner
status: verified
description: "Configure SQLite for apps: journal_mode=WAL, synchronous=NORMAL, busy_timeout, per-connection foreign_keys, STRICT tables, checkpoint control, and why not on network filesystems."
sources:
  - https://www.sqlite.org/wal.html
  - https://www.sqlite.org/pragma.html
  - https://www.sqlite.org/stricttables.html
  - https://www.sqlite.org/useovernet.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SQLite WAL mode and pragmas — the settings every app should set on open

**Goal:** an SQLite database that allows concurrent readers during writes, does not
throw "database is locked" under normal load, enforces its constraints, and keeps its
WAL file bounded.

## 1. Per-connection setup (run on every open)
```sql
PRAGMA journal_mode = WAL;        -- persistent: stored in the file, but harmless to repeat
PRAGMA synchronous = NORMAL;      -- per connection; safe with WAL
PRAGMA busy_timeout = 5000;       -- ms; per connection
PRAGMA foreign_keys = ON;         -- per connection; OFF by default!
PRAGMA cache_size = -65536;       -- negative = KiB, here 64 MiB
PRAGMA temp_store = MEMORY;
PRAGMA mmap_size = 268435456;     -- optional, 256 MiB
```
Only `journal_mode=WAL` persists. Everything else resets with each connection, so put
it in your pool's connection-init hook. Checked on 3.50.4 (Python): a fresh file reported `foreign_keys` 0, `journal_mode` delete, `synchronous` 2, `cache_size` -2000, `temp_store` 0, `mmap_size` 0, `wal_autocheckpoint` 1000 and `journal_size_limit` -1 (no limit); after setting the block above and reconnecting, only `journal_mode` stayed `wal` (the new connection showed `synchronous` 2, `foreign_keys` 0, `cache_size` -2000). `PRAGMA synchronous=NORMAL`, `foreign_keys=ON`, `cache_size`, `temp_store` return no row when set; `journal_mode`, `busy_timeout` and `mmap_size` echo the new value. Python's `sqlite3.connect()` already sets a 5000 ms busy timeout by default. Forgetting `foreign_keys = ON` is the most
common SQLite integrity bug: FKs are parsed, then ignored.

## 2. What WAL changes
- Readers don't block the writer and the writer doesn't block readers. There is still
  **one writer at a time**.
- Files: `db`, `db-wal`, `db-shm`. Copying only `db` while the app runs loses committed
  data; back up with `sqlite3 app.db ".backup backup.db"`, `VACUUM INTO 'backup.db'`, or
  Litestream for continuous replication.
- `synchronous=NORMAL` in WAL: durable against application crashes; a power loss can
  roll back the last few transactions but won't corrupt. Use `FULL` if each commit must
  survive power loss.
- WAL requires shared memory between processes on the same host: **do not use it (or
  SQLite generally for concurrent writers) on NFS/SMB/network filesystems**. Locking is
  unreliable there and corruption follows. One process on a local disk, or a
  client/server database.

## 3. Avoiding SQLITE_BUSY
`busy_timeout` makes a blocked connection retry for up to N ms instead of failing at
once. It is not enough on its own: a transaction that starts as a reader (`BEGIN`) and
later writes cannot be retried safely when another writer got in first, and fails
immediately with `SQLITE_BUSY` despite the timeout. Fix:
```sql
BEGIN IMMEDIATE;   -- take the write lock up front for any transaction that will write
...
COMMIT;
```
Most drivers let you set the default (e.g. Python `sqlite3.connect(..., isolation_level="IMMEDIATE")`:
tested, the first DML statement then left `in_transaction` True; check your driver). Reproduced: a `BEGIN` plus `SELECT` followed by a write after another connection committed failed at once with `SQLITE_BUSY_SNAPSHOT` despite a 5 s timeout. Keep write transactions short; route all writes through a single
connection or queue in high-write apps.

## 4. Checkpointing
WAL content is copied back into the main file by checkpoints; automatic at ~1000 pages
(`PRAGMA wal_autocheckpoint`, ≈4 MB with 4 KiB pages). A checkpoint can't pass a reader
still using an old snapshot, so a long-lived read transaction (an open cursor never
finalised) makes the WAL grow without bound. Manual control:
```sql
PRAGMA wal_checkpoint(TRUNCATE);  -- checkpoint fully and truncate the -wal file
PRAGMA journal_size_limit = 67108864;  -- cap leftover WAL size at 64 MiB
```
Run `TRUNCATE` checkpoints from a maintenance task when idle; monitor `-wal` file size.

## 5. STRICT tables and schema hygiene
SQLite's type affinity lets you store `'abc'` in an `INTEGER` column. Since 3.37:
```sql
CREATE TABLE item (
  id INTEGER PRIMARY KEY,           -- alias for rowid
  sku TEXT NOT NULL UNIQUE,
  qty INTEGER NOT NULL CHECK (qty >= 0),
  owner_id INTEGER REFERENCES owner(id) ON DELETE CASCADE
) STRICT;
```
STRICT allows only `INT, INTEGER, REAL, TEXT, BLOB, ANY`; no `DATETIME` type, so store
ISO-8601 text or Unix integers. Tested: `DATETIME`, `VARCHAR(10)`, `NUMERIC` and `BOOLEAN` columns failed with `unknown datatype`, and inserting `'abc'` into an INTEGER column failed with `cannot store TEXT value in INTEGER column it.qty`. Versions before 3.37.0 (2021-11-27) can't read or write STRICT tables (stricttables.html), which matters for bundled OS copies.

`ALTER TABLE` is limited (rename table, add/rename/drop column, with the restrictions in `twelve-step-table-rebuild`). Other changes use the
documented 12-step rebuild: new table, copy, drop, rename, inside a transaction with
`foreign_keys` off and `PRAGMA foreign_key_check` after. Use `PRAGMA user_version` to
track migration level.

## 6. Maintenance
- `PRAGMA optimize;` before closing long-lived connections (or periodically) updates
  planner statistics cheaply.
- `PRAGMA integrity_check;` (or the faster `quick_check`) in health checks.
- `VACUUM` rebuilds the file to reclaim space; it needs up to 2× disk space and an
  exclusive lock. `auto_vacuum=INCREMENTAL` must be set before tables are created.

## Verify
- [ ] `PRAGMA journal_mode;` returns `wal`; `PRAGMA foreign_keys;` returns `1` on a pooled connection.
- [ ] Write transactions use `BEGIN IMMEDIATE`; a two-writer load test shows no `SQLITE_BUSY`.
- [ ] The `-wal` file stays bounded over a day of traffic.
- [ ] Database lives on local storage, not NFS/SMB.
- [ ] Backups use `.backup`/`VACUUM INTO`/Litestream, and a restored copy passes `integrity_check`.
