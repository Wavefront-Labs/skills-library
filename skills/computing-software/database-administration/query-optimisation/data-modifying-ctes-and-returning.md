---
id: computing-software.database-administration.query-optimisation.data-modifying-ctes-and-returning
name: data-modifying-ctes-and-returning
category: computing-software
field: database-administration
product: query-optimisation
tags: [database-administration, query-optimisation, writable-cte, returning-clause, output-clause, sql-fluency, atomic-updates]
level: practitioner
status: draft
description: "Use RETURNING (OUTPUT in SQL Server) and data-modifying CTEs to move, archive or upsert rows atomically in one statement, with snapshot visibility rules."
sources:
  - https://www.postgresql.org/docs/current/queries-with.html#QUERIES-WITH-MODIFYING
  - https://www.postgresql.org/docs/current/dml-returning.html
  - https://learn.microsoft.com/en-us/sql/t-sql/queries/output-clause-transact-sql
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Data-modifying CTEs and RETURNING

## RETURNING
Get generated or changed values without a second query:
```sql
INSERT INTO orders (customer_id, total) VALUES (42, 99.50) RETURNING id, created_at;
UPDATE jobs SET status = 'running', started_at = now()
WHERE id = (SELECT id FROM jobs WHERE status = 'queued' ORDER BY id FOR UPDATE SKIP LOCKED LIMIT 1)
RETURNING id, payload;
DELETE FROM sessions WHERE expires_at < now() RETURNING user_id;
```
Support: PostgreSQL, SQLite 3.35+, MariaDB (INSERT/DELETE ... RETURNING), Oracle (`RETURNING INTO` in PL/SQL; 23ai extended). SQL Server uses `OUTPUT inserted.*, deleted.*`. MySQL has no RETURNING (use `LAST_INSERT_ID()`).

## Move rows atomically (archive)
```sql
WITH moved AS (
  DELETE FROM events WHERE created_at < now() - interval '90 days'
  RETURNING *
)
INSERT INTO events_archive SELECT * FROM moved;
```
One statement, one transaction: no window where rows are in both or neither table. Batch it (`WHERE id IN (SELECT id ... LIMIT 10000)`) for large volumes.

## Insert parent and children together
```sql
WITH o AS (INSERT INTO orders (customer_id) VALUES (42) RETURNING id)
INSERT INTO order_items (order_id, sku, qty)
SELECT o.id, i.sku, i.qty FROM o, (VALUES ('A1', 2), ('B7', 1)) AS i(sku, qty);
```

## Visibility rules (PostgreSQL)
- All sub-statements see the **same snapshot** taken at statement start; they cannot see each other's changes to tables, only the RETURNING output.
- Updating the same row twice in one statement is unpredictable; avoid it.
- Data-modifying CTEs execute exactly once, even if not referenced by the main query.

## SQL Server equivalent
```sql
DELETE FROM dbo.events
OUTPUT deleted.* INTO dbo.events_archive
WHERE created_at < DATEADD(day, -90, SYSUTCDATETIME());
```

## Verify
Counts before and after: `archive_added = rows_deleted`; run inside a test transaction and roll back to check.
