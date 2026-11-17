---
id: computing-software.software-engineering.python.sqlite3-for-applications
name: sqlite3-for-applications
category: computing-software
field: software-engineering
product: python
tags: [python, sqlite3, python-stdlib, wal-mode, parameterized-queries, row-factory, transactions, py-databases]
level: practitioner
status: verified
description: "Use the sqlite3 module safely: parameters not f-strings, transaction control (autocommit attribute in 3.12), row factories, WAL and busy_timeout for concurrency."
sources: ["https://docs.python.org/3/library/sqlite3.html", "https://www.sqlite.org/wal.html", "https://www.sqlite.org/pragma.html"]
licence: Apache-2.0
version: 5
updated: 2026-11-17
---

# sqlite3 for applications

**Goal:** a reliable embedded database for tools, caches and small services, without
the classic sqlite3 module traps.

## Connect with sane settings
```python
import sqlite3
con = sqlite3.connect("app.db", timeout=10, autocommit=True)    # autocommit= is 3.12+
con.row_factory = sqlite3.Row                                   # rows behave like dicts
con.execute("PRAGMA journal_mode=WAL")       # readers don't block the writer
con.execute("PRAGMA foreign_keys=ON")        # off by default, per connection!
con.execute("PRAGMA busy_timeout=10000")
con.execute("PRAGMA synchronous=NORMAL")     # safe with WAL, much faster than FULL
con.autocommit = False                       # then switch to explicit transactions
```
Set `journal_mode` while `autocommit=True`: with `autocommit=False` a transaction is already open and SQLite raises `cannot change into wal mode from within a transaction` (reproduced on Python 3.14).

## Always parameterise
```python
con.execute("SELECT * FROM users WHERE email = ?", (email,))          # tuple, note the comma
con.execute("INSERT INTO users(name, email) VALUES (:name, :email)", {"name": n, "email": e})
con.executemany("INSERT INTO events VALUES (?, ?)", rows)              # bulk insert
```
Never format values into SQL (injection, quoting bugs). Table/column names cannot be
parameters; whitelist them.

## Transactions
- `autocommit=False` (3.12+): a transaction is always open; `con.commit()` / `con.rollback()`.
- `sqlite3.connect()` defaults on 3.14: `autocommit=-1` (legacy control) and `isolation_level=''`.
- Legacy default (`isolation_level=""`): module implicitly BEGINs before DML; DDL does not open a transaction on
  3.14 (`in_transaction` stayed False after `CREATE TABLE`, and the table survived a rollback of later DML), but older versions differed - a source of "my CREATE TABLE was not committed" bugs.
- `with con:` commits on success and rolls back on exception, but does **not** close the
  connection; close explicitly or use `contextlib.closing`.
```python
with con:
    con.execute("UPDATE accounts SET bal = bal - ? WHERE id = ?", (amt, a))
    con.execute("UPDATE accounts SET bal = bal + ? WHERE id = ?", (amt, b))
```

## Concurrency
- One writer at a time per database. `database is locked` = another connection held the
  write lock longer than `timeout`. Fix: WAL, short transactions, `busy_timeout`, and
  `BEGIN IMMEDIATE` for read-then-write transactions (avoids upgrade deadlocks). Reproduced: a deferred `BEGIN` that read, then tried to write after another connection had committed a write, failed at once with `database is locked` (no wait, because the snapshot is stale); `BEGIN IMMEDIATE` takes the write lock up front instead (while another writer held it, it waited for `timeout` and then raised the same error).
- Connections are not shareable across threads by default (`check_same_thread=True`);
  use one connection per thread or a lock. `sqlite3.threadsafety` reports build mode.
- Not for network filesystems (NFS/SMB): locking is unreliable, corruption risk.

## Useful bits
- Adapters: register `datetime` handling explicitly - the default adapters are deprecated in 3.12.
- `con.backup(dest_con)` for online backups; `VACUUM INTO 'copy.db'`.
- `json_extract`, `FTS5` and `STRICT` tables are available in modern SQLite builds
  (`sqlite3.sqlite_version`).

## Verify
- [ ] `PRAGMA journal_mode` returns `wal` and `PRAGMA foreign_keys` returns 1 on each connection.
- [ ] grep finds no f-strings/`%` formatting inside `execute(` calls.

## Checked
Run on Windows (Python 3.14.0, SQLite 3.50.4) and Linux (Python 3.14.8 musl in WSL2, SQLite 3.53.1) with identical results except lock wait timing: `journal_mode=WAL`; `foreign_keys` is 0 on every new connection and 1 after the pragma; `busy_timeout` pragma reflects `timeout=10`; `synchronous=NORMAL` is 1; WAL change inside `autocommit=False` raises `cannot change into wal mode from within a transaction` (and a rollback does not help because the next transaction opens at once); `Row` access by name and index; passing a bare string as parameters gives `Incorrect number of bindings`; table names as `?` are a syntax error; foreign key violation raises `IntegrityError`; `with con` commits or rolls back and leaves the connection open; `contextlib.closing` closes it; a second writer gets `database is locked` after `timeout`; a WAL reader sees the last committed value while a writer is open; cross-thread use raises `ProgrammingError`; `backup`, `VACUUM INTO`, `json_extract`, FTS5 and STRICT (`cannot store TEXT value in INTEGER column`) work; the default datetime adapter emits a `DeprecationWarning`. Not run: NFS/SMB locking claims, `executemany` performance, Python versions before 3.12 (no `autocommit=` parameter), `PRAGMA synchronous=NORMAL` durability under power loss.
