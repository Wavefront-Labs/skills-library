---
id: computing-software.database-administration.sqlite.without-rowid-tables
name: without-rowid-tables
category: computing-software
field: database-administration
product: sqlite
tags: [database-administration, sqlite, without-rowid, clustered-index, sqlite-schema, primary-keys]
level: practitioner
status: verified
description: "Decide when SQLite WITHOUT ROWID tables (clustered on the primary key) save space and time, how to create them, and the cases where they are slower."
sources:
  - https://sqlite.org/withoutrowid.html
  - https://sqlite.org/lang_createtable.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# WITHOUT ROWID tables

**Goal:** store rows in a B-tree keyed by the declared primary key (like a clustered index), avoiding a separate rowid B-tree plus a PK index.

## Create
```sql
CREATE TABLE kv (
  k TEXT PRIMARY KEY,
  v BLOB
) WITHOUT ROWID;

CREATE TABLE user_roles (
  user_id INTEGER NOT NULL,
  role_id INTEGER NOT NULL,
  PRIMARY KEY (user_id, role_id)
) WITHOUT ROWID;
```
Requires a PRIMARY KEY (`create table nopk(a,b) without rowid` failed with `PRIMARY KEY missing on table nopk`); its columns are implicitly `NOT NULL` (checked: inserting a NULL key into the WITHOUT ROWID table failed with `NOT NULL constraint failed: kv.k`, while the ordinary table accepted it, historical bug-compatibility). `AUTOINCREMENT` is rejected (`AUTOINCREMENT not allowed on WITHOUT ROWID tables`) and `select rowid from kv` fails with `no such column: rowid`.

## When it wins
- Non-integer or composite primary keys (strings, UUIDs, junction tables): one B-tree instead of table + index and one lookup instead of two. Measured on 3.50.4 with 50,000 random UUID text keys and a 20-byte value: 5.78 MB as a rowid table, 3.58 MB WITHOUT ROWID (about 38% smaller, not half); insert and point-lookup times were about equal.
- Small rows (the docs' rule of thumb: average row under about 1/20th of the page size, i.e. about 50 bytes at 1 KiB pages or 200 bytes at 4 KiB pages).

## When it loses
- Large rows: WITHOUT ROWID tables store content in interior B-tree nodes too, lowering fan-out (withoutrowid.html). Same test with a 1,000-byte value: 70.9 MB rowid vs 234.5 MB WITHOUT ROWID, inserts 3.4 s vs 0.29 s, lookups 1.5 s vs 0.36 s.
- Tables with an INTEGER PRIMARY KEY gain nothing (rowid tables already cluster on it).
- Secondary indexes store the full primary key instead of an 8-byte rowid: wide PKs make every index bigger.
- No `sqlite3_last_insert_rowid()`, no incremental BLOB I/O, no AUTOINCREMENT.

## Converting
Not possible with `ALTER TABLE`; use the 12-step rebuild: create new table WITHOUT ROWID, copy, drop, rename, recreate indexes and triggers.

## Verify
Compare file size and timing on a realistic dataset (`sqlite3_analyzer` or `dbstat`) before and after; `pragma index_list` still lists the PK as `sqlite_autoindex_kv_1` with origin `pk`, but `sqlite_schema` has no separate `sqlite_autoindex` row for it (an ordinary table with a text PK has one).
