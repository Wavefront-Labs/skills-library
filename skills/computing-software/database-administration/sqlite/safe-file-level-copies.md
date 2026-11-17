---
id: computing-software.database-administration.sqlite.safe-file-level-copies
name: safe-file-level-copies
category: computing-software
field: database-administration
product: sqlite
tags: [database-administration, sqlite, backup-api, sqlite-file-copy, wal-file, shm-file, backup-corruption]
level: practitioner
status: verified
description: "Copy SQLite database files without producing a corrupt backup: why cp of a live db and missing -wal files fail, and the safe alternatives (.backup, VACUUM INTO, locks)."
sources:
  - https://www.sqlite.org/howtocorrupt.html
  - https://www.sqlite.org/wal.html
  - https://www.sqlite.org/backup.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Safe file-level copies

## Why `cp app.db backup/` goes wrong
- A writer can change pages while `cp` reads the file: the copy mixes old and new pages and is
  corrupt (`database disk image is malformed`).
- In **WAL mode** committed transactions may live only in `app.db-wal` until a checkpoint. Copying
  just `app.db` loses them; copying `app.db` and `app.db-wal` at slightly different moments is
  inconsistent.
- Deleting or not restoring a `-wal` file that belongs to a database ("hot" WAL) loses data;
  pairing a `-wal` with the wrong database file corrupts it.
- The `-shm` file holds the wal-index, a shared-memory index that lets readers find pages in the WAL (wal.html); it was not needed in the test: a copy of `app.db` plus `app.db-wal` alone opened and returned all 1,000 rows.
- A rollback journal (`app.db-journal`) left from a crash is "hot" and needed for recovery.

## Safe options
1. **Online backup API** (consistent, copies through SQLite's locking):
   ```bash
   sqlite3 app.db ".backup 'backup/app-$(date +%F).db'"
   ```
2. **VACUUM INTO** (consistent, compacted copy, 3.27+):
   ```bash
   sqlite3 app.db "VACUUM INTO 'backup/app-$(date +%F).db'"
   ```
3. **sqlite3_rsync** (added in 3.47.0, "experimental" in its release log) for efficient incremental copies of a live database, locally or over ssh (`sqlite3_rsync ORIGIN REPLICA`).
4. Litestream / LiteFS for continuous WAL replication.
5. Plain file copy **only** while no process has the database open (application stopped), or
   while holding a lock: `BEGIN IMMEDIATE;` blocks writers (readers continue; a second writer got
   `database is locked`), then copy **both** `app.db` and `app.db-wal`, then `COMMIT`.
   `PRAGMA wal_checkpoint(TRUNCATE);` empties the WAL, but it cannot run inside that transaction
   (`database table is locked`), so run it before the copy and accept that writers may append again before you copy.
   A test on 3.50.4 (WAL file of 4.1 MB, autocheckpoint off): copying only `app.db` gave a database with no tables,
   copying `app.db` plus `app.db-wal` gave all 1,000 rows, and after a TRUNCATE checkpoint (`0|0|0`, WAL size 0) `app.db` alone had them.

## Filesystem snapshots
LVM/ZFS/cloud snapshots that capture `app.db` and `app.db-wal` atomically at the same instant should
recover like a power-loss crash; snapshots of the two files at different times are not safe. (This is general
filesystem reasoning, not stated on the SQLite pages used here; test a restore, and note SQLite's own list of
safe backup methods is the backup API, `VACUUM INTO` and `sqlite3_rsync`.)

## After copying
```bash
sqlite3 backup/app-2026-10-18.db "PRAGMA integrity_check;"     # 'ok'
```
Store backups with checksums; test-restore regularly.

## Gotchas
- Containers and sync tools (Dropbox, OneDrive, rsync of a live directory) copy files without
  locks: classic source of corrupt SQLite databases.
- Renaming or moving a database file while open leaves the WAL associated with the old path.

## Verify
`PRAGMA integrity_check` on every backup returns `ok`, and a restored copy opens with the
latest committed rows present.
