---
id: computing-software.database-administration.sqlite.threading-modes-and-connection-per-thread
name: threading-modes-and-connection-per-thread
category: computing-software
field: database-administration
product: sqlite
tags: [database-administration, sqlite, sqlite-threading-mode, serialized, multi-thread, sqlite-concurrency, connection-pool]
level: practitioner
status: verified
description: "Choose SQLite threading mode (single-thread, multi-thread, serialized), use one connection per thread or a pool, and avoid sharing connections and statements unsafely."
sources:
  - https://sqlite.org/threadsafe.html
  - https://sqlite.org/c3ref/open.html
  - https://sqlite.org/faq.html#q6
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Threading modes and connection-per-thread patterns

## Modes
| Mode | Compile/start/open setting | Rule |
|---|---|---|
| Single-thread | `SQLITE_THREADSAFE=0` | No mutexes; one thread only |
| Multi-thread | `SQLITE_THREADSAFE=2` or `SQLITE_OPEN_NOMUTEX` | Many threads, but a connection (and its statements) used by one thread at a time |
| Serialized | `SQLITE_THREADSAFE=1` (default) or `SQLITE_OPEN_FULLMUTEX` | A connection may be shared; calls are serialised with a mutex |

Check: `SELECT * FROM pragma_compile_options WHERE compile_options LIKE 'THREADSAFE%';` (returned `THREADSAFE=1` in the Python 3.14 module, matching threadsafe.html's "default mode is serialized") and `sqlite3_threadsafe()`, which reports only the compile-time setting, not what a connection was opened with.

## Recommended pattern
- One connection per thread (or a pool where a connection is checked out by one thread at a time). Multi-thread mode is then safe and avoids mutex overhead.
- Sharing one serialized connection across threads works but serialises everything, and transactions become shared: thread A's `BEGIN` affects thread B's statements on the same connection.
- WAL mode so readers in other connections proceed while one writer writes.
- Single writer: funnel writes through one connection/thread (queue) to avoid `SQLITE_BUSY` storms; many reader connections.

## Language specifics
- Python `sqlite3`: by default refuses use of a connection from another thread (`check_same_thread=True`); tested: `ProgrammingError: SQLite objects created in a thread can only be used in that same thread`. Setting False is allowed only if you add your own locking. `sqlite3.threadsafety` was 3 (serialized) in the module tested.
- Go `database/sql` with `mattn/go-sqlite3` or `modernc.org/sqlite`: pool size matters; for writes set `db.SetMaxOpenConns(1)` on a write handle, separate read handle.
- iOS/macOS: GRDB offers `DatabaseQueue` and `DatabasePool` (README: pick the queue if unsure; the pool is the WAL reader/writer option). Android frameworks were not checked.

## Busy handling
Always set `PRAGMA busy_timeout = 5000;` per connection; use `BEGIN IMMEDIATE` for write transactions to take the write lock up front, avoiding deadlock-like upgrade failures (`SQLITE_BUSY` on lock upgrade from read).

## Forking
Never use a connection in a child process after `fork()`; open new connections in the child (howtocorrupt.html, "Carrying an open database connection across a fork()").

## Verify
Load test with N reader threads and one writer: no `database is locked` errors, writer latency stable.
