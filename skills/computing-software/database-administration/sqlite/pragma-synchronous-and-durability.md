---
id: computing-software.database-administration.sqlite.pragma-synchronous-and-durability
name: pragma-synchronous-and-durability
category: computing-software
field: database-administration
product: sqlite
tags: [database-administration, sqlite, wal-mode, pragma-synchronous, durability, fsync, power-loss]
level: practitioner
status: verified
description: "Choose PRAGMA synchronous (OFF, NORMAL, FULL, EXTRA) together with the journal mode, knowing exactly what each risks on application crash versus power loss."
sources:
  - https://www.sqlite.org/pragma.html#pragma_synchronous
  - https://www.sqlite.org/wal.html#performance_considerations
  - https://www.sqlite.org/atomiccommit.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# PRAGMA synchronous and durability

`synchronous` controls how often SQLite calls fsync. It is per connection and not persistent:
set it at every connection open.
```sql
PRAGMA synchronous;              -- 0 OFF, 1 NORMAL, 2 FULL (default; a fresh 3.50.4 file returned 2), 3 EXTRA
PRAGMA synchronous = NORMAL;
```

## What you risk
| Journal mode | synchronous | App crash | OS crash / power loss |
|---|---|---|---|
| WAL | FULL | safe | safe, durable |
| WAL | **NORMAL** | safe | **consistent**, but the most recent commits may roll back (not durable) |
| WAL | OFF | safe | may corrupt |
| DELETE (rollback) | FULL | safe | no corruption, but not necessarily durable: a commit just before power loss may roll back depending on the filesystem (EXTRA closes that gap) |
| DELETE | NORMAL | safe | small chance of corruption on old filesystems |
| any | OFF | safe (SQLite still hands data to the OS) | can corrupt |
| DELETE | EXTRA | as FULL, plus the directory is synced after the journal is unlinked | strongest durability in rollback mode; in WAL mode EXTRA is no different from FULL |

The usual recommendation for applications: **`journal_mode=WAL` + `synchronous=NORMAL`**:
fast (fsync only at checkpoint), never corrupt, loses at most the last few transactions on power
loss. Use FULL where every acknowledged commit must survive power loss (payments, ledgers).

## Bulk loads
For one-off imports that you can redo from source, `synchronous=OFF` and
`journal_mode=MEMORY` or `OFF` speed things up a lot; switch back afterwards and run
`PRAGMA integrity_check`.

## Things that defeat durability regardless
- Disks or virtual disks that lie about flush (consumer SSDs without power-loss protection,
  some hypervisor cache settings).
- Network filesystems (NFS/SMB) with broken locking or caching.
- macOS: `F_FULLFSYNC` (flush the drive cache) is used only when `PRAGMA fullfsync = ON` (all syncs) or `checkpoint_fullfsync = ON` (checkpoints, default off); the pragma page says only macOS supports it.

## Setting it reliably
Wrap connection creation: e.g. Python
```python
con = sqlite3.connect(path, isolation_level=None)
con.execute("PRAGMA journal_mode=WAL")      # persistent in the file
con.execute("PRAGMA synchronous=NORMAL")    # per connection
con.execute("PRAGMA foreign_keys=ON")
con.execute("PRAGMA busy_timeout=5000")
```

## Verify
`PRAGMA synchronous;` on a pooled connection returns the intended value; a pull-the-plug test on
the target hardware (VM hard reset during writes) leaves `PRAGMA integrity_check` returning `ok`.
