---
id: computing-software.database-administration.sql.natural-and-using-joins
name: natural-and-using-joins
category: computing-software
field: database-administration
product: sql
tags: [sql, natural-and-using-joins]
level: practitioner
status: docs-checked
description: "Know what JOIN USING and NATURAL JOIN do and why NATURAL is risky."
sources: ["https://www.postgresql.org/docs/current/queries-table-expressions.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# NATURAL JOIN and USING pitfalls

- `JOIN b USING (id)` is shorthand for `ON a.id = b.id` on the listed same-named columns, and the output suppresses the redundant column: one `id` column (in USING-list order), then the remaining columns of a, then the remaining columns of b. `JOIN ON` outputs all columns of both tables.
- `NATURAL JOIN` is shorthand for a USING list of every column name present in both tables; with no common names it behaves like CROSS JOIN.
- The manual calls USING reasonably safe from column changes, since only the listed columns are combined, and NATURAL considerably more risky: any schema change that creates a new matching name (for example an `updated_at` added to both tables) silently adds that column to the join.
- Prefer explicit `ON` or USING in production code; avoid NATURAL.
- Self-check: list `information_schema.columns` for both tables and confirm which names collide.

## Checked

Date: 2026-11-08

Method: Read the PostgreSQL manual page queries-table-expressions.html (joined tables) and matched the USING, NATURAL and output-column claims to its text; a draft claim about qualified USING columns erroring in some engines was removed because the page does not support it.
