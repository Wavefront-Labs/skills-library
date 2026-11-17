---
id: computing-software.database-administration.duckdb.duckdb-merge-into
name: duckdb-merge-into
category: computing-software
field: database-administration
product: duckdb
tags: [duckdb, merge-into, upsert, delete, when-matched, returning]
level: practitioner
status: docs-checked
description: "Upsert, update or delete DuckDB rows from a source query with MERGE INTO when the target has no primary key, including WHEN NOT MATCHED BY SOURCE and merge_action."
sources:
  - https://raw.githubusercontent.com/duckdb/duckdb-web/main/docs/1.4/sql/statements/merge_into.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: apply a change set to a table using a custom match condition (no primary key needed, unlike `INSERT ... ON CONFLICT`).

Shape: `MERGE INTO target USING source ON (cond) | USING (col) WHEN ... THEN action ...`. If the key column has the same name in source and target, write `USING (id)` instead of `ON (...)`.

```sql
CREATE TABLE people (id INTEGER, name VARCHAR, salary FLOAT);
INSERT INTO people VALUES (1, 'John', 92_000.0), (2, 'Anna', 100_000.0);

-- whole-row upsert
MERGE INTO people
  USING (SELECT unnest([3, 1]) AS id, unnest(['Sarah','John']) AS name,
                unnest([95_000.0, 105_000.0]) AS salary) AS upserts
  ON (upserts.id = people.id)
  WHEN MATCHED THEN UPDATE
  WHEN NOT MATCHED THEN INSERT;

-- change set: only some columns
MERGE INTO people USING (SELECT 1 AS id, 98_000.0 AS salary) AS salary_updates
  USING (id)
  WHEN MATCHED THEN UPDATE SET salary = salary_updates.salary;

-- delete set, with extra condition
MERGE INTO people USING (SELECT unnest([3, 2]) AS id) AS deletes
  USING (id)
  WHEN MATCHED AND people.salary >= 100_000.0 THEN DELETE;
```

Multiple `WHEN MATCHED AND cond` branches are allowed (several UPDATE / DELETE conditions). The page's example uses `WHEN NOT MATCHED THEN INSERT BY NAME`. `RETURNING merge_action, *` shows what happened per row (`UPDATE`, `DELETE`, ...):

```sql
MERGE INTO people USING (...) AS upserts USING (id)
  WHEN MATCHED AND people.salary < 100_000.0 THEN UPDATE SET salary = upserts.salary
  WHEN MATCHED AND people.salary > 100_000.0 THEN DELETE
  WHEN NOT MATCHED THEN INSERT BY NAME
  RETURNING merge_action, *;
```

`WHEN NOT MATCHED BY SOURCE THEN DELETE` removes target rows absent from the source (a full sync). `WHEN NOT MATCHED BY TARGET` behaves the same as plain `WHEN NOT MATCHED`.

## Checked

2026-11-07. Read the DuckDB 1.4 docs page sql/statements/merge_into.md in full. Confirmed: MERGE INTO as an alternative to INSERT ... ON CONFLICT without a primary key, ON and USING (col) matching, WHEN MATCHED [AND cond] UPDATE/UPDATE SET/DELETE, WHEN NOT MATCHED INSERT [BY NAME], RETURNING merge_action, *, WHEN NOT MATCHED BY SOURCE/TARGET, and every example. Removed: the unsupported claim that INSERT BY NAME maps columns by name (the page only shows it) and the invented Verify step. Elided example sources (`USING (...)`) are illustrative.

Method: documentation only; no commands were run.
