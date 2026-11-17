---
id: computing-software.database-administration.sqlite.concurrency-limits-and-busy-handling
name: concurrency-limits-and-busy-handling
category: computing-software
field: database-administration
product: sqlite
tags: [database-administration, sqlite, concurrency, sqlite_busy, busy_timeout, locking, wal-mode, writer-starvation, nfs, multi-process, single-writer]
level: advanced
status: verified
description: "Know exactly what SQLite's locking model allows concurrently, handle SQLITE_BUSY without silent data loss, and recognize when the workload has outgrown SQLite."
sources:
  - https://www.sqlite.org/lockingv3.html
  - https://www.sqlite.org/wal.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SQLite concurrency: what's actually allowed, and when to stop pretending it's a server database

**Goal:** stop guessing at "is this safe to do from two processes," handle
`SQLITE_BUSY` correctly instead of swallowing it, and recognize the write-volume
point where SQLite is the wrong tool.

## 1. The locking model, precisely
In **rollback journal mode** (the default; a new file reports `delete`): any number
of concurrent readers; a writer takes a RESERVED lock when its transaction starts
(readers may still read), then PENDING and EXCLUSIVE locks only to commit (or when its
page cache spills), which is when readers are blocked (lockingv3 page). Run on 3.50.4: a
second connection read the old row count while a write transaction was open. In **WAL
mode** (opt in with `PRAGMA journal_mode=WAL`, which persists in the file; recommended
for concurrent access on a local disk): readers don't block the writer and the writer
doesn't block readers, but there is still only **one writer at a time**, enforced by the
WAL write lock in the `-shm` wal-index file (there is no separate lock file; the files are
`-wal` and `-shm`). In both modes, on 3.50.4 a second `BEGIN IMMEDIATE` with a zero busy timeout
failed at once with `database is locked`. SQLite is not multi-writer under any mode: that
is a design constant, not a tunable.

## 2. SQLITE_BUSY: the error most apps handle wrong
By default, a blocked lock attempt returns `SQLITE_BUSY` immediately with no
retry. The common anti-pattern: catching it and discarding the write, or retrying
in a loop with no backoff that live-locks two processes against each other. Correct
handling:
```c
sqlite3_busy_timeout(db, 5000);  // retry internally for up to 5s before SQLITE_BUSY (ctypes check: a 300 ms timeout made a blocked BEGIN IMMEDIATE return SQLITE_BUSY after about 0.4 s, a 0 timeout after 0.0 s)
```
or implement `sqlite3_busy_handler` with exponential backoff for finer control.
Python's `sqlite3.connect(timeout=5.0)` sets a 5 s busy timeout by default (checked:
`PRAGMA busy_timeout` returns 5000); the C API default is none.
Even with a timeout set, a sustained high-concurrency write workload will still
eventually produce `SQLITE_BUSY` — the application must treat it as "retry the
whole transaction", not as a fatal error, and definitely not silently drop the
write. In WAL mode a transaction that read first (`BEGIN` then `SELECT`) and then tries to
write after another connection committed fails at once with `SQLITE_BUSY_SNAPSHOT`
(`database is locked`, 0.0 s even with a 5 s timeout, reproduced): the busy handler cannot
help, so start write transactions with `BEGIN IMMEDIATE` or retry the whole transaction.

## 3. Checkpoint starvation under WAL
A checkpoint (folding the WAL file back into the main database) can only reset the WAL
when no connection has a read transaction open on it (wal.html, "checkpoint starvation").
With always at least one overlapping reader the WAL keeps growing (disk usage, and read
performance deteriorates as the WAL grows). See `checkpoint-starvation-and-large-wal`. Tune
`wal_autocheckpoint` (pages before an automatic passive checkpoint) and consider
periodic explicit `PRAGMA wal_checkpoint(TRUNCATE)` during a known-quiet window if
automatic checkpointing can't keep up.

## 4. Network filesystems break the locking model
SQLite's file locking (and WAL's shared-memory file) assumes POSIX/Win32 locking
semantics that many network filesystems (NFS, some SMB configurations, most
consumer cloud-sync folders; the sqlite.org pages name NFS and network filesystems, the
cloud-sync folder case is general experience, not from those pages) do not implement
correctly or consistently across clients. WAL mode additionally needs all
processes on the same host (shared memory). Running a SQLite database from a network share
with multiple accessing hosts is a documented source of corruption (useovernet.html,
howtocorrupt.html), not just slowness. Keep the database file on local/direct-attached storage; if shared
access across machines is required, that's a sign to use a client/server database
instead.

## 5. When to stop using SQLite
SQLite's own documentation is explicit about this: it is not the right choice for
high write-concurrency multi-client workloads (many separate processes/hosts
writing frequently), very large concurrent client counts needing simultaneous
writes, or network-filesystem-hosted multi-host access. It's the right choice for
embedded/single-process apps, read-mostly workloads with occasional writes, and as
a local cache/queue — not as the backing store for a multi-service web application
under genuine write concurrency.

## Verify
- [ ] WAL mode is enabled (`PRAGMA journal_mode=WAL;`) for any multi-reader/writer access pattern.
- [ ] `busy_timeout` or a custom busy handler is set, and `SQLITE_BUSY` triggers a transaction retry, not a dropped write.
- [ ] WAL file size is monitored; checkpoints aren't silently starved under load.
- [ ] The database file lives on local/direct-attached storage, never a network share with multiple writers.
- [ ] Actual required write concurrency was sized against SQLite's single-writer limit before committing to it for a growing service.
