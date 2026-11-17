---
id: computing-software.database-administration.sqlite.comparing-databases-with-sqldiff
name: comparing-databases-with-sqldiff
category: computing-software
field: database-administration
product: sqlite
tags: [database-administration, sqlite, sqldiff, schema-comparison, data-diff, sqlite-backup, rbu]
level: practitioner
status: verified
description: "Compare two SQLite databases with sqldiff to produce SQL that turns one into the other, diff schema only or a single table, and generate changesets or RBU updates."
sources:
  - https://sqlite.org/sqldiff.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Comparing databases with sqldiff

## Basic
```bash
sqldiff old.db new.db > patch.sql        # SQL statements that convert old.db into new.db
sqlite3 old.db < patch.sql               # apply
```
Output contains `INSERT`, `UPDATE`, `DELETE` per differing row, and schema changes. By default rows are paired by rowid (or by PRIMARY KEY for WITHOUT ROWID tables), not by the declared primary key: `--primarykey` switches pairing to the declared key (sqldiff.html). Run against sqlite-tools 3.54.1 it emitted e.g. `ALTER TABLE orders ADD COLUMN extra;`, `UPDATE orders SET v='B' WHERE id=2;`, `DELETE FROM orders WHERE id=3;`, `INSERT INTO orders(id,v,extra) VALUES(4,'d',NULL);`, and `UPDATE nopk SET a=3, b=3 WHERE rowid=2;` for a table without a key.

## Options
| Option | Use |
|---|---|
| `--schema` | compare schema only |
| `--table orders` | only one table |
| `--primarykey` | match rows by declared PK instead of rowid |
| `--summary` | count changes per table instead of SQL (e.g. `orders: 1 changes, 1 inserts, 1 deletes, 1 unchanged`, or `newt: missing from first database`) |
| `--changeset FILE` | write a binary changeset (session extension format) instead of SQL; tables with no explicit primary key are omitted (see Limitations) |
| `--rbu` | output for the RBU (resumable bulk update) extension (listed in `sqldiff --help`, not on the sqldiff.html option list) |
| `--transaction` | wrap output in BEGIN/COMMIT (checked) |
| `--vtab` | handle FTS3/FTS5 and R*Tree tables (the docs list fts3, fts5 and rtree; `--help` also says fts4) |
| `-L LIB`, `--lib LIB` | load an extension library first, e.g. for application-defined collations the schema needs |

## Uses
- Verify a migration on a copy: `sqldiff --schema expected.db migrated.db` should print nothing.
- Audit what a test or a batch job changed: snapshot before, run, `sqldiff --summary before.db after.db`.
- Ship incremental data updates to devices: generate a changeset or SQL patch from the last published version.

## Limitations
- Without `--vtab`, an FTS5 table is diffed through its shadow tables: a new `fts5` table produced `CREATE TABLE 'f_config'`, `'f_content'`, `'f_data'`, `'f_docsize'`, `'f_idx'` plus raw INSERTs. With `--vtab` it printed `CREATE VIRTUAL TABLE f using fts5(t);` and `INSERT INTO f(rowid,t) VALUES(1,'hello');`.
- `--changeset` with a schema difference (a column added in the destination) failed with `schema changes for table orders` and wrote an empty file; align the schemas first.
- A column dropped or retyped is not an ALTER: sqldiff printed `DROP TABLE t; -- due to schema mismatch`, `CREATE TABLE t(...)` and fresh INSERTs, so review before applying to data you care about.
- Tables without a PRIMARY KEY or rowid differences (after VACUUM on tables without INTEGER PRIMARY KEY) produce noisy diffs; use `--primarykey` and stable keys.
- Large databases: comparisons are full scans of both files; run off-hours on copies.

## Verify
After applying `patch.sql` to old.db, `sqldiff old.db new.db` prints nothing (checked for the `orders` table with `--table orders`; `sqldiff --schema new.db new.db` printed nothing and exited 0).
