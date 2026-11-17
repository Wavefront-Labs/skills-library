---
id: computing-software.database-administration.duckdb.duckdb-insert-on-conflict-upsert
name: duckdb-insert-on-conflict-upsert
category: computing-software
field: database-administration
product: duckdb
tags: [duckdb, insert, upsert, on-conflict, excluded, primary-key]
level: practitioner
status: docs-checked
description: "Handle key conflicts in DuckDB INSERT with ON CONFLICT DO NOTHING / DO UPDATE, INSERT OR IGNORE/REPLACE, conflict targets and the EXCLUDED pseudo-table."
sources:
  - https://raw.githubusercontent.com/duckdb/duckdb-web/main/docs/1.4/sql/statements/insert.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: insert rows without failing on PRIMARY KEY / UNIQUE violations.

Without handling, a duplicate raises `Constraint Error: Duplicate key "i: 1" violates primary key constraint.` and the first row stays.

```sql
CREATE TABLE tbl (i INTEGER PRIMARY KEY, j INTEGER);
INSERT INTO tbl VALUES (1, 42);
INSERT INTO tbl VALUES (1, 84) ON CONFLICT DO NOTHING;                  -- keeps (1,42)
INSERT INTO tbl VALUES (1, 84) ON CONFLICT DO UPDATE SET j = EXCLUDED.j; -- becomes (1,84)
```

- `INSERT OR IGNORE INTO` = `ON CONFLICT DO NOTHING`.
- `INSERT OR REPLACE INTO` = `DO UPDATE SET c1 = EXCLUDED.c1, c2 = EXCLUDED.c2, ...` for every column (updates all columns of the existing row).
- `EXCLUDED.col` is the to-be-inserted row; an unqualified column refers to the existing row. Usable in both `SET` and `WHERE`.
- Add `WHERE cond` after `SET ...` to restrict updates; conflicts failing the condition are ignored.

Conflict target: `ON CONFLICT (col)` names the columns of the index/constraint. If omitted, the PRIMARY KEY is targeted. It is required for `DO UPDATE` when the table has several unique/primary key constraints:

```sql
CREATE TABLE tbl (i INTEGER PRIMARY KEY, j INTEGER UNIQUE, k INTEGER);
INSERT INTO tbl VALUES (1, 20, 300);
INSERT INTO tbl VALUES (1, 40, 700) ON CONFLICT (i) DO UPDATE SET k = 2 * EXCLUDED.k;  -- k = 1400
INSERT INTO tbl VALUES (1, 40, 700) ON CONFLICT (i) DO UPDATE SET k = 2 * EXCLUDED.k WHERE k < 100;
```

Composite keys: declare one `PRIMARY KEY (id1, id2)` clause. Column order tricks work too: `INSERT INTO tbl (j, i) VALUES (168, 1) ON CONFLICT DO UPDATE SET j = EXCLUDED.j;` and `INSERT INTO tbl BY NAME (SELECT 1 AS i, 336 AS j) ON CONFLICT ...`.

The page also shows an example inserting two conflicting rows `(1, 52), (1, 62)` in one statement with `DO UPDATE SET j = EXCLUDED.j`; it does not state the resulting value.

## Checked

2026-11-07. Read the INSERT Statement page in full and confirmed the primary key Constraint Error text, DO NOTHING and DO UPDATE examples, INSERT OR IGNORE and INSERT OR REPLACE equivalences, the EXCLUDED qualifier in SET and WHERE, the optional WHERE on DO UPDATE, conflict target rules (PRIMARY KEY by default, required for DO UPDATE with several constraints), the k = 1400 and WHERE k < 100 examples, composite keys, and the reordered-column and BY NAME examples. Replaced the advice to test repeated keys in one batch with the page's factual statement (the result is not stated) and removed the Verify step.

Method: documentation only; no commands were run.
