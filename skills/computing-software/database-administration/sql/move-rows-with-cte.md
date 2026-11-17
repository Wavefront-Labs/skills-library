---
id: computing-software.database-administration.sql.move-rows-with-cte
name: move-rows-with-cte
category: computing-software
field: database-administration
product: sql
tags: [sql, move-rows-with-cte]
level: advanced
status: docs-checked
description: "Move rows between tables atomically with DELETE ... RETURNING feeding INSERT."
sources: ["https://www.postgresql.org/docs/current/queries-with.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Archive and move rows with a writable CTE

- `WITH moved AS (DELETE FROM live WHERE ts < now() - interval '90 days' RETURNING *) INSERT INTO archive SELECT * FROM moved;` is one statement, so it is atomic (PostgreSQL). The PostgreSQL manual's own example moves rows from `products` to `products_log` this way.
- Data-modifying sub-statements in WITH run exactly once, to completion, whether or not the main query reads their output.
- All statements share one snapshot, so they cannot see one another's effects on the target tables; RETURNING is the only way to pass changes between them. The order in which sub-statements' updates happen is unpredictable.
- For very large moves, limit each run to a bounded batch of keys (for example `WHERE id IN (SELECT id FROM live WHERE ... LIMIT 10000)`) and repeat, to keep each transaction short. This is common practice, not something the manual prescribes.
- Self-check: rows deleted equals rows inserted, in one transaction.

## Checked

Date: 2026-11-08

Method: Read the PostgreSQL manual page queries-with.html (data-modifying statements in WITH) and compared each claim to its text; batching advice is marked as practice because the page does not cover it.
