---
id: computing-software.database-administration.sqlite.checkpoint-starvation-and-large-wal
name: checkpoint-starvation-and-large-wal
category: computing-software
field: database-administration
product: sqlite
tags: [database-administration, sqlite, checkpoint-starvation, wal-checkpoint, wal-autocheckpoint, sqlite-wal, journal-size-limit]
level: practitioner
status: verified
description: "Diagnose SQLite WAL files that grow without bound because readers block checkpoints, and fix them with checkpoint modes, journal_size_limit and reader hygiene."
sources:
  - https://sqlite.org/wal.html#avoiding_excessively_large_wal_files
  - https://sqlite.org/pragma.html#pragma_wal_checkpoint
  - https://sqlite.org/c3ref/wal_checkpoint_v2.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Checkpoint starvation and large WAL files

## Symptom
`app.db-wal` grows without bound (sqlite.org/wal.html: with always at least one active reader, no checkpoint completes); disk fills.

## Cause
A checkpoint can run to completion and reset the WAL only if no other connection is using it: an open read transaction prevents the reset. With continuous overlapping readers (or one long-running read, or a connection holding an open statement), the WAL is never reset.

## Diagnose
```sql
PRAGMA wal_checkpoint(PASSIVE);   -- returns busy, log_frames, checkpointed_frames
```
`checkpointed < log` repeatedly means readers block progress. Reproduced on 3.50.4: with a reader holding an unfinished SELECT, `wal_checkpoint(PASSIVE)` returned `(0, 250, 0)` (nothing checkpointed) and `RESTART` returned busy=1 after the busy timeout; once the reader finished, `RESTART` returned `(0, 250, 250)`. Look for:
- Statements not reset/finalised (an iterator left open in app code holds a read transaction).
- Long analytics queries on the same file.
- A backup reading through the whole database.

## Fixes
1. Finalise/reset statements promptly; close cursors; keep read transactions short.
2. Run a stronger checkpoint at quiet moments:
```sql
PRAGMA wal_checkpoint(RESTART);   -- tries harder than PASSIVE, waits (busy timeout) for readers, then lets the WAL restart from the beginning
PRAGMA wal_checkpoint(TRUNCATE);  -- as RESTART and truncates the file to zero bytes (observed: size 0)
```
The docs warn readers might block while these run, and a busy result means it could not finish.
3. Cap the file size after resets: `PRAGMA journal_size_limit = 67108864;` (64 MB) the docs say a checkpoint does not normally truncate the WAL unless this is set; it otherwise just overwrites from the start.
4. Tune `PRAGMA wal_autocheckpoint = 1000;` (pages, default 1000 ≈ 4 MB at the default 4096-byte page size); automatic checkpoints are PASSIVE and happen on a COMMIT that grows the WAL past the threshold.
5. Move heavy reads to a snapshot copy (backup API or `VACUUM INTO`) so they do not pin the WAL.

## Verify
WAL size stays bounded over a day of production load; periodic `wal_checkpoint(PASSIVE)` shows `checkpointed == log` regularly.
