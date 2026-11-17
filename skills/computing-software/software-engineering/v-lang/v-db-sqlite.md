---
id: computing-software.software-engineering.v-lang.v-db-sqlite
name: v-db-sqlite
category: computing-software
field: software-engineering
product: v-lang
tags: [v-db-sqlite, orm-and-databases, sqlite, db.sqlite, sqlite.connect, exec, exec_param, rows, memory, transaction, embedded database, v-lang]
level: practitioner
status: draft
description: "Open sqlite databases with sqlite.connect, run exec and exec_param statements, read rows, transactions and in-memory databases."
sources:
  - https://docs.vlang.io/
  - https://modules.vlang.io/
  - https://github.com/vlang/v
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# db.sqlite: opening, exec and queries

Goal: use SQLite from V.

- `import db.sqlite`; `mut db := sqlite.connect('app.db')!`; in-memory `sqlite.connect(':memory:')!`; `defer { db.close() or {} }`.
- Raw SQL: `db.exec('CREATE TABLE t (id INTEGER PRIMARY KEY, name TEXT)')!`, rows `rows := db.exec('SELECT id, name FROM t')!` then `row.vals[0]`; params `db.exec_param('SELECT * FROM t WHERE name = ?', who)!`, `exec_param_many` for several.
- Helpers: `db.q_int('select count(*) from t')!`, `db.q_string(...)`, `db.last_insert_rowid()`, `db.get_affected_rows_count()`.
- Transactions: `db.exec('BEGIN')!` ... `db.exec('COMMIT')!` (or `db.begin()` helpers, confirm); `db.busy_timeout(5000)`.
- Needs `libsqlite3` dev package on Linux (`libsqlite3-dev`), bundled on Windows builds.

Gotchas:
- Always use `exec_param` for user values; never concatenate.
- Concurrent writers need WAL mode: `PRAGMA journal_mode=WAL`.

Verify: insert and read back a row within a test.
