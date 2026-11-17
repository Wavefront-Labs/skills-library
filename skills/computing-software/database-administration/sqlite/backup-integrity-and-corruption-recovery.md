---
id: computing-software.database-administration.sqlite.backup-integrity-and-corruption-recovery
name: backup-integrity-and-corruption-recovery
category: computing-software
field: database-administration
product: sqlite
tags: [database-administration, sqlite, backup-api, integrity-check, corruption, dump, recover, pragma, vacuum-into, dot-dump, data-recovery]
level: advanced
status: verified
description: "Back up a live SQLite database safely with the online backup API, run integrity checks correctly, and recover readable data from a corrupt file."
sources:
  - https://www.sqlite.org/backup.html
  - https://www.sqlite.org/pragma.html#pragma_integrity_check
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SQLite backup, integrity checks, and corruption recovery

**Goal:** back up a database that's actively being written to without copying a
torn file, catch corruption with the right pragma, and pull out what's still
readable when a file is damaged.

## 1. Never just `cp` a live database file
sqlite.org/howtocorrupt.html: a copy taken while a transaction is in progress "might contain some old and some new content, and thus be corrupt"; a raw copy is safe only with no transactions in progress and any `-journal` or `-wal` file copied with the database.
Use one of:
- **Online Backup API** (`sqlite3_backup_init`/`step`/`finish`) — per sqlite.org/backup.html it can run incrementally so the source is locked only briefly while pages are read, and the finished copy is a consistent snapshot.
- **`VACUUM INTO 'backup.db'`** — produces a compacted, defragmented, consistent
  copy of a live database in one statement; simpler than the backup API for a one-shot snapshot (sqlite.org lists it as a backup technique; check lang_vacuum for its locking).
- **`sqlite3_rsync`** — copies a live database to or from a remote system over SSH.
- **`.dump`** (SQL text dump) — portable and human-auditable, but slow to produce
  and slow to restore (replays every INSERT) on larger databases; useful for
  archival or cross-version migration, not routine backup cadence.

## 2. Integrity checking — know which one you're running
```sql
PRAGMA integrity_check;    -- thorough: checks every page, all indexes match tables
PRAGMA quick_check;        -- faster: skips some index-content verification
```
`quick_check` skips UNIQUE-constraint verification and the check that index content matches table content (O(N) vs O(N log N)), so use `integrity_check` before trusting a backup or after a suspected crash. Neither checks FOREIGN KEY errors (use `PRAGMA foreign_key_check`). `integrity_check` returns a single row `ok` when clean and stops after 100 errors by default. Run them on an idle copy for a stable result.

## 3. What actually causes corruption
- Power loss or process kill mid-write **without** proper journaling — this is
  rare with WAL/rollback-journal modes functioning correctly, but happens if
  `synchronous=OFF` is set (skips fsync entirely for speed) and the OS/disk loses
  unflushed writes on crash. `FULL` is the default; `NORMAL` in WAL mode cannot corrupt the database but a committed transaction can roll back after power loss (loses durability). Only use `OFF` for genuinely disposable/rebuildable data.
- Network filesystems with broken or missing locking, where several processes access one database (howtocorrupt: "especially true of network filesystems and NFS").
- Other processes or bugs writing to the file (howtocorrupt: any process can overwrite it; reused file descriptors, rogue threads), or failing hardware.

## 4. Recovering data from a corrupt file
1. `PRAGMA integrity_check` first to see the scope (which tables/pages are
   affected — sometimes only one table is unreadable, the rest is fine).
2. Try `.recover` (sqlite3 CLI): `sqlite3 corrupt.db .recover > data.sql`, then load into a new file. sqlite.org/recovery.html warns recovered databases are usually defective: content may be lost, deleted rows may reappear, values or types may change, constraints may be violated; recovered content that cannot be placed goes to `lost_and_found`.
3. If `.recover` can't run, `.dump` is a fallback that reads through normal SQL and may stop at damaged pages: check its output for errors and gaps.
4. As a last resort, `PRAGMA writable_schema=ON` lets ordinary UPDATE/INSERT/DELETE modify `sqlite_schema` (unless defensive mode is on), which can make it worse —
   genuinely a last resort, document exactly what was reconstructed versus
   recovered verbatim.
5. After any recovery, treat the result as unverified until cross-checked (row
   counts, spot-checked values) against the last known-good backup or external
   source of truth.

## Verify
- [ ] Backups use the Online Backup API, `VACUUM INTO`, `sqlite3_rsync` or `.dump` — never a raw file copy of a live database with writers active.
- [ ] `synchronous` is not set to `OFF` for any data that must survive a crash.
- [ ] `PRAGMA integrity_check` (not `quick_check`) runs as part of backup verification, on an idle copy.
- [ ] A `.recover` or `.dump`-based recovery drill has been tried at least once before it's needed for real.
- [ ] Any recovered database's row counts/spot-checks were compared against a known-good reference before trusting it.
