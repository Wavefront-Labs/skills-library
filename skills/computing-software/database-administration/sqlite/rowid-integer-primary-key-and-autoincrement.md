---
id: computing-software.database-administration.sqlite.rowid-integer-primary-key-and-autoincrement
name: rowid-integer-primary-key-and-autoincrement
category: computing-software
field: database-administration
product: sqlite
tags: [database-administration, sqlite, integer-primary-key, autoincrement, rowid, sqlite-schema, primary-keys]
level: practitioner
status: verified
description: "Understand SQLite rowid tables: INTEGER PRIMARY KEY aliasing rowid, what AUTOINCREMENT really guarantees and costs, and rowid reuse pitfalls."
sources:
  - https://sqlite.org/lang_createtable.html#rowid
  - https://sqlite.org/autoinc.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# rowid, INTEGER PRIMARY KEY and AUTOINCREMENT

## rowid
Every ordinary table has a 64-bit signed `rowid` (also `oid`, `_rowid_`) that is the B-tree key. Lookups by rowid are the fastest access path.

## INTEGER PRIMARY KEY = rowid alias
```sql
CREATE TABLE users (id INTEGER PRIMARY KEY, email TEXT NOT NULL UNIQUE);
```
Exactly `INTEGER PRIMARY KEY` (the type name must be `INTEGER`) makes `id` an alias for rowid: no separate index, and inserting `NULL` assigns `max(rowid)+1`. Gotchas:
- `INT PRIMARY KEY`, `BIGINT PRIMARY KEY` or `INTEGER PRIMARY KEY DESC` do **not** alias rowid (they create a separate unique index). Check with `pragma table_info` and plan output (`USING INTEGER PRIMARY KEY`).
- Composite primary keys never alias rowid.

## AUTOINCREMENT
```sql
CREATE TABLE events (id INTEGER PRIMARY KEY AUTOINCREMENT, payload TEXT);
```
- Without it: new id = largest current rowid + 1. If you delete the max row, its id **can be reused**.
- With it: ids are never reused, even after deletes, tracked in `sqlite_sequence`. If the max (9223372036854775807) is reached inserts fail with `SQLITE_FULL`; without it SQLite then tries unused random rowids.
- Cost: an extra table write per insert; the docs advise avoiding it unless reuse is a real problem (ids exposed in URLs, audit trails referencing deleted rows).
- Neither guarantees gap-free sequences (deleted rows and explicit ids leave gaps), but a rolled-back transaction does not consume an id: `sqlite_sequence` rolls back too (tested 3.50.4; sqlite.org autoinc page).

## Explicit ids
You can insert any id; next automatic id follows the max. Negative ids are allowed.

## VACUUM and rowids
`VACUUM` may renumber rowids of tables **without** an INTEGER PRIMARY KEY. Never store raw rowids externally unless they are aliased by an INTEGER PRIMARY KEY column.

## Verify
`EXPLAIN QUERY PLAN SELECT * FROM users WHERE id=5` shows `SEARCH users USING INTEGER PRIMARY KEY (rowid=?)`.

## Checked
- SQLite 3.50.4: `INTEGER PRIMARY KEY` and `integer primary key` alias rowid (no index, NULL assigns 1), `INT`, `BIGINT`, `INTEGER PRIMARY KEY DESC` and composite keys create an index and leave the column NULL; without AUTOINCREMENT a deleted max id was reused and with it the next id was 4 (`sqlite_sequence` row); explicit negative ids work; after the max rowid AUTOINCREMENT fails with `database or disk is full` while a plain table picks an unused id; `VACUUM` renumbered rowids of a table without an integer key and left an `INTEGER PRIMARY KEY` unchanged; the `EXPLAIN QUERY PLAN` line matches. A rolled-back insert did not consume an id (the autoinc page says rolled-back ROWIDs are ignored).
