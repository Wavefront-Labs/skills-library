---
id: computing-software.database-administration.duckdb.duckdb-update-delete-from
name: duckdb-update-delete-from
category: computing-software
field: database-administration
product: duckdb
tags: [duckdb, update, delete, truncate, returning, checkpoint]
level: practitioner
status: docs-checked
description: "UPDATE ... FROM joins, self-updates with aliases, DELETE ... USING / RETURNING, TRUNCATE, and why DuckDB DELETE does not free disk space until CHECKPOINT."
sources:
  - https://raw.githubusercontent.com/duckdb/duckdb-web/main/docs/1.4/sql/statements/update.md
  - https://raw.githubusercontent.com/duckdb/duckdb-web/main/docs/1.4/sql/statements/delete.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: modify or remove rows in bulk and know the space-reclaim limits.

UPDATE changes only columns named in `SET`; others keep their values.

```sql
UPDATE tbl SET i = 0 WHERE i IS NULL;
UPDATE tbl SET i = 1, j = 2;
```

Update from another table (both forms complete in bulk for increased performance):

```sql
UPDATE original SET value = new.value FROM new WHERE original.key = new.key;
UPDATE original SET value = (SELECT new.value FROM new WHERE original.key = new.key);
```

Join-driven: `UPDATE city SET revenue = revenue + 100 FROM country WHERE city.country_code = country.code AND country.name = 'France';`

Updating from the same table needs distinct aliases on both sides (`UPDATE original AS true_original SET value = (SELECT new.value || ' a change!' FROM original AS new WHERE true_original.key = new.key);`).

DELETE: no `WHERE` deletes everything; rows where the condition is false or NULL are kept. `USING` deletes based on other tables or subqueries. `RETURNING` takes SELECT-clause syntax (no `DISTINCT`):

```sql
DELETE FROM tbl WHERE i = 2;
DELETE FROM employees RETURNING name, 2025 - age AS approx_birthyear;
TRUNCATE tbl;     -- alias for DELETE FROM tbl without WHERE
```

Space: DELETE in general only marks rows deleted; space is reclaimed on `CHECKPOINT` (see `duckdb-checkpoint-vacuum`). `VACUUM` currently does not reclaim space. For upserts use `duckdb-insert-on-conflict-upsert` or `duckdb-merge-into`.

## Checked

2026-11-07. Read the DuckDB 1.4 docs pages sql/statements/update.md and sql/statements/delete.md in full. Confirmed: SET semantics, both examples, UPDATE from another table by FROM or sub-select, same-table update with distinct aliases, the city/country join example, DELETE with and without WHERE and false/NULL retention, USING, RETURNING without DISTINCT and its example, TRUNCATE as alias, space reclaim only on CHECKPOINT, VACUUM not reclaiming, upsert pointer. Changed: softened "only marks" to "in general" per the page; removed the invented Verify step.

Method: documentation only; no commands were run.
