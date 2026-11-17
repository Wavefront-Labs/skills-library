---
id: computing-software.database-administration.sqlite.sqlite3-rsync-live-copies
name: sqlite3-rsync-live-copies
category: computing-software
field: database-administration
product: sqlite
tags: [database-administration, sqlite, sqlite3-rsync, sqlite-replication, live-backup, sqlite-backup]
level: practitioner
status: verified
description: "Copy or update a live SQLite database to another location or host with sqlite3_rsync (3.47+), which transfers only changed pages and keeps the replica consistent."
sources:
  - https://sqlite.org/rsync.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# sqlite3_rsync for live database copies

**Goal:** keep a consistent copy of a database that is being written, locally or over SSH, transferring only changed pages. Plain `rsync` of a live database can produce a corrupt copy.

## Usage
```bash
sqlite3_rsync ORIGIN REPLICA [OPTIONS]
sqlite3_rsync /data/app.db /backup/app.db
sqlite3_rsync /data/app.db backup-host:/srv/replicas/app.db       # over ssh
sqlite3_rsync user@prod:/data/app.db ./app-local.db                # pull
```
Options (from `sqlite3_rsync --help`, 3.54.1): `--exe PATH` (name of sqlite3_rsync on the remote side), `--ssh PATH`, `-p|--port PORT` (ssh TCP port), `-v` (more v's, more output), `--protocol N`, `--wal-only` (do not sync unless both databases are in WAL mode), `--version`. Options may appear before, after or between the two paths. One side must be local; both cannot be remote.

## Requirements
- Ships with SQLite 3.47.0+ (added in that release as "experimental"; `sqlite3_rsync.exe` is in the sqlite-tools zip). Install the same tool on both ends (remote must have it in PATH or `--exe`).
- Before 3.50.0 both databases had to be in **WAL mode** with the same page size; sqlite.org says those limits were removed in 3.50.0 (2025-05-29). Checked on 3.54.1: a rollback-journal origin synced fine (the replica stayed in `delete` mode, and `--wal-only` refused with `Origin database is not in WAL mode`), while a WAL origin gave a WAL replica.
- Origin can be read and written during the sync; changes made to the origin during the run are not transferred. The replica is read-only for the duration (readers are fine, writers are not).
- SSH access to the remote side; no daemon needed.

## How it works
Both sides hash pages; only pages with different hashes are sent, inside a read transaction on the origin, so the replica becomes an exact snapshot of one point in time. Bandwidth is roughly proportional to changed pages, much less than a full copy.

## Patterns
- Hourly cron to a standby host for fast DR (pair with a retention scheme of dated copies on the backup side).
- Refresh a reporting/analytics copy without locking production.
- Seed a new replica before switching to Litestream/LiteFS.

## Gotchas
- It is a copy tool, not continuous replication: data written after the last run is not on the replica.
- An existing replica with another page size still failed in 3.54.1 (`ERROR: page size mismatch; origin is 4096 bytes and replica is 8192 bytes`, exit 1), although a replica that did not yet exist was created with the origin's page size. Delete or recreate the replica. For a continuously written origin use WAL mode (`PRAGMA journal_mode=WAL`) so writers are not blocked by the sync's read.

## Verify
`sqlite3 /backup/app.db "PRAGMA integrity_check"` returns `ok` (it did after a local sync), and a row count or checksum query matches the origin at the sync time.
