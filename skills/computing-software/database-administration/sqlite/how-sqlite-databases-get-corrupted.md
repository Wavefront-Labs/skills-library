---
id: computing-software.database-administration.sqlite.how-sqlite-databases-get-corrupted
name: how-sqlite-databases-get-corrupted
category: computing-software
field: database-administration
product: sqlite
tags: [database-administration, sqlite, howtocorrupt, sqlite-corruption, data-integrity, sqlite-concurrency, integrity-check]
level: practitioner
status: verified
description: "Prevent SQLite corruption by knowing the documented causes: unsafe file copying, broken locking on network filesystems, deleted hot journals, fsync lies and misuse after fork."
sources:
  - https://sqlite.org/howtocorrupt.html
  - https://sqlite.org/lockingv3.html
  - https://sqlite.org/pragma.html#pragma_integrity_check
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# How SQLite databases get corrupted (and how to avoid it)

SQLite is very resistant to crashes and power loss when the OS and hardware honour its assumptions. Corruption almost always comes from violating those.

## Main causes (from the official "How To Corrupt" page)
1. **Copying the file while it is being written**: `cp app.db backup.db` mid-transaction, or copying `app.db` without its `-wal`. Use the backup API, `VACUUM INTO`, or `sqlite3 app.db ".backup b.db"`.
2. **Deleting or separating the hot journal / WAL**: deleting `-journal`/`-wal` after a crash, or moving `app.db` without them, loses committed or rollback data.
3. **Broken file locking**: filesystems with broken or missing lock implementations (network filesystems, NFS in particular); two processes using different locking protocols (e.g. one on POSIX advisory locks, the other on a dot-file locking VFS); POSIX locks cancelled by a separate thread calling `close()` on the same file; multiple copies of SQLite linked into one application; unlinking or renaming the database file while in use; multiple hard links to the same file. WAL mode needs all processes on one host (shared memory), so it is not for network filesystems.
4. **Closing a file descriptor that SQLite has open**: POSIX advisory locks are per-process, so another library opening and closing the same file drops SQLite's locks.
5. **Using a connection after `fork()`**.
6. **Storage that lies about fsync** (cheap USB/SD, some virtualised disks, `synchronous=OFF`): power loss reorders writes.
7. **Memory corruption / stray pointers** in the application overwriting SQLite buffers or file descriptors (e.g. fd reuse writing log lines into the database file).
8. Running with `PRAGMA journal_mode=OFF` or `MEMORY` and crashing mid-transaction.

## Safe configuration baseline
```sql
PRAGMA journal_mode = WAL;     -- local disks only
PRAGMA synchronous = NORMAL;   -- with WAL; FULL if every commit must survive power loss
PRAGMA foreign_keys = ON;
```
Keep the database on a local filesystem; for multi-host access use a client/server database or a replication tool.

## Detect early
```sql
PRAGMA quick_check;            -- faster, skips index content checks
PRAGMA integrity_check;        -- thorough
```
`quick_check` skips the UNIQUE and index-content consistency checks (pragma page). Run on backups and periodically on production (on a copy if large).
In a test on 3.54.1, overwriting 60 bytes in one page gave `Tree 2 page 3 cell 125: Offset 65535 out of range` from both checks.

## When corruption is found
Stop writes, copy all files (db, -wal, -shm) for forensics, then try `.recover` into a new database and restore from the last good backup for comparison.
```bash
sqlite3 broken.db ".recover" > rec.sql && sqlite3 recovered.db < rec.sql
```
That recovered 4,779 of 5,000 rows from the damaged test file and the new database passed `integrity_check`; expect losses.

## Verify
Audit deployments: no database file on NFS/SMB, backups made with the backup API, and `integrity_check` returns `ok` on the latest backup.
