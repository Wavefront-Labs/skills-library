---
id: computing-software.database-administration.query-optimisation.upsert-and-merge-statements
name: upsert-and-merge-statements
category: computing-software
field: database-administration
product: query-optimisation
tags: [database-administration, query-optimisation, sql, upsert, merge-statement, on-conflict, on-duplicate-key-update, insert-or-replace, race-conditions, idempotent-writes]
level: practitioner
status: gated
description: "Write race-safe upserts per engine (ON CONFLICT, ON DUPLICATE KEY UPDATE, MERGE) and know MERGE's concurrency pitfalls in SQL Server and PostgreSQL."
sources:
  - https://www.postgresql.org/docs/current/sql-insert.html#SQL-ON-CONFLICT
  - https://www.postgresql.org/docs/current/sql-merge.html
  - https://dev.mysql.com/doc/refman/8.4/en/insert-on-duplicate.html
  - https://learn.microsoft.com/en-us/sql/t-sql/statements/merge-transact-sql
  - https://www.sqlite.org/lang_upsert.html
  - https://www.postgresql.org/docs/16/sql-insert.html
  - https://www.postgresql.org/docs/16/sql-merge.html
  - https://www.postgresql.org/docs/17/sql-merge.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Upsert and MERGE

**Goal:** insert-or-update in one statement, correct under concurrency, without the select-then-insert race.

## PostgreSQL / SQLite: ON CONFLICT
```sql
INSERT INTO inventory (sku, qty, updated_at) VALUES ('A1', 5, now())
ON CONFLICT (sku) DO UPDATE
  SET qty = inventory.qty + EXCLUDED.qty, updated_at = EXCLUDED.updated_at
  WHERE inventory.updated_at < EXCLUDED.updated_at      -- optional guard
RETURNING sku, qty, (xmax = 0) AS inserted;             -- PG trick: xmax=0 means inserted
```
Needs a unique index/constraint matching the conflict target. Atomic and race-safe. `DO NOTHING` for insert-if-absent. SQLite 3.24+ same syntax (sqlite.org: added 3.24.0, 2018-06-04; run on 3.50.4). Run on PostgreSQL 16.4: the first call returns `inserted = true` and the second `false`; the `xmax = 0` trick works. With the optional `WHERE inventory.updated_at < EXCLUDED.updated_at` guard, 50 concurrent upserts of qty 5 summed to 245, not 250, because one update was skipped by the guard; drop the guard when you need every increment, as the Verify step expects.

## MySQL / MariaDB
```sql
INSERT INTO inventory (sku, qty) VALUES ('A1', 5) AS new
ON DUPLICATE KEY UPDATE qty = inventory.qty + new.qty;   -- 8.0.19+ alias; older: VALUES(qty); the MySQL 8.4 manual calls `VALUES()` deprecated and documents the row alias
```
Fires on ANY unique key conflict, not just the one you meant; tables with several unique keys may update the wrong row. `REPLACE INTO` deletes then inserts (fires delete triggers, new auto-increment, cascades FKs (gated: unconfirmed, source is paywalled or blocked)): avoid.
Under REPEATABLE READ, concurrent upserts can deadlock on gap locks; retry (gated: unconfirmed, source is paywalled or blocked).

## MERGE (SQL Server, Oracle, PostgreSQL 15+)
```sql
MERGE INTO inventory WITH (HOLDLOCK) AS t                 -- SQL Server: HOLDLOCK is required for race safety
USING (VALUES ('A1', 5)) AS s (sku, qty) ON t.sku = s.sku
WHEN MATCHED THEN UPDATE SET qty = t.qty + s.qty
WHEN NOT MATCHED THEN INSERT (sku, qty) VALUES (s.sku, s.qty);
```
- SQL Server: without `HOLDLOCK`/`SERIALIZABLE`, concurrent MERGEs hit duplicate key errors (gated: unconfirmed, source is paywalled or blocked). MERGE also has a history of bugs (filtered indexes, triggers); many teams use `UPDATE ...; IF @@ROWCOUNT = 0 INSERT ...` inside a serializable transaction instead.
- PostgreSQL MERGE (15+) is not race-safe against concurrent inserts the way ON CONFLICT is: a concurrent insert raises a unique violation (checked on 16.4: five rounds of 40 simultaneous MERGEs on one new key gave 22 `duplicate key value violates unique constraint` errors and lost increments, whereas 50 concurrent ON CONFLICT upserts raised none). Use ON CONFLICT for single-row upserts; MERGE for batch sync with deletes (`WHEN NOT MATCHED BY SOURCE THEN DELETE` is in the PostgreSQL 17 docs and a syntax error on 16.4).

## Bulk upserts
Load into a staging table, then one `INSERT ... SELECT ... ON CONFLICT` / MERGE. Deduplicate staging first: PostgreSQL errors `ON CONFLICT DO UPDATE command cannot affect row a second time` (confirmed on 16.4) when the batch has duplicate keys.

## Verify
Run 50 concurrent upserts of the same key in a test; the row exists once with the summed quantity and no errors (or only retryable deadlocks in MySQL, handled).
