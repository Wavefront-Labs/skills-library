---
id: computing-software.database-administration.sqlite.uri-filenames-read-only-and-immutable
name: uri-filenames-read-only-and-immutable
category: computing-software
field: database-administration
product: sqlite
tags: [database-administration, sqlite, sqlite-uri-filename, read-only, immutable, sqlite-open-modes, sqlite-cli]
level: practitioner
status: verified
description: "Open SQLite databases with URI filenames (mode=ro, immutable=1, cache=shared, vfs, in-memory names), the shell's -readonly and -safe flags, and when each is safe."
sources:
  - https://sqlite.org/uri.html
  - https://sqlite.org/c3ref/open.html
  - https://sqlite.org/cli.html#command_line_options
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# URI filenames: read-only, immutable and safe opens

## Enabling URIs
URI filenames need `SQLITE_OPEN_URI` (or global `SQLITE_USE_URI`); the shell and Python (`uri=True`) support them.

## Parameters
| Parameter | Effect |
|---|---|
| `mode=ro` | read-only; fails writes. `rw`, `rwc` (create), `memory` |
| `immutable=1` | promise that nobody changes the file: no locking, no change detection |
| `nolock=1` | skip file locking only |
| `cache=shared` / `private` | shared cache between connections in one process (discouraged; prefer WAL) |
| `vfs=unix-dotfile` etc. | choose a VFS |
| `psow=0` | powersafe overwrite off |

Checked on 3.50.4 (Python) and the 3.54.1 shell: `mode=ro` made `CREATE TABLE` fail with `attempt to write a readonly database`; `mode=rw` on a missing file failed with `unable to open database file` while `mode=rwc` created it.
```bash
sqlite3 'file:/data/app.db?mode=ro'
sqlite3 'file:/mnt/cdrom/catalog.db?immutable=1'
```
```python
sqlite3.connect("file:app.db?mode=ro", uri=True)
sqlite3.connect("file:memdb1?mode=memory&cache=shared", uri=True)   # named in-memory DB shared by connections in-process
```

## When immutable is dangerous
`immutable=1` on a file that another process writes gives wrong results or corruption-like errors because SQLite skips locks and WAL checks. In a test an immutable connection kept returning 2 rows after another connection had committed a third (a normal connection saw 3). Use only for read-only media or files guaranteed static (published datasets).

## Read-only and WAL
Since 3.22.0 a WAL database on read-only media can be read if the `-shm` and `-wal` files already exist and are readable, or the directory is writable so they can be created, or the connection uses `immutable=1` (wal.html section 5); otherwise checkpoint and switch to `journal_mode=DELETE` before shipping the file.

## Shell flags
- `-readonly`: open read-only.
- `-safe`: disables commands that touch other files or run programs. In 3.54.1 it refused `.shell`, `.output`, every `ATTACH` (`cannot run ATTACH in safe mode`) and `readfile()`, for running untrusted SQL scripts.
- `-deserialize` (open the file via sqlite3_deserialize) and `-nofollow` (refuse symbolic links to database files); both are in `sqlite3 -help`.

## Verify
Attempting `CREATE TABLE t(x)` on a `mode=ro` connection returns `attempt to write a readonly database`. Do not rely on `PRAGMA query_only;`: it returned 0 on a `mode=ro` connection.
