---
id: computing-software.database-administration.sql.not-exists-anti-join
name: not-exists-anti-join
category: computing-software
field: database-administration
product: sql
tags: [sql, not-exists-anti-join]
level: practitioner
status: docs-checked
description: "Find rows with no match using NOT EXISTS or LEFT JOIN with IS NULL."
sources: ["https://www.postgresql.org/docs/current/functions-subquery.html", "https://www.postgresql.org/docs/current/queries-table-expressions.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# NOT EXISTS and LEFT JOIN IS NULL anti-joins

- `WHERE NOT EXISTS (SELECT 1 FROM o WHERE o.cid = c.id)` negates EXISTS, which only asks whether the subquery returns any row; the manual says the subquery output list is normally unimportant (hence `SELECT 1`) and that the subquery usually stops as soon as one row is found. NULLs in `o.cid` cannot make it return nothing.
- Alternative: `FROM c LEFT JOIN o ON o.cid = c.id WHERE o.cid IS NULL` (test a NOT NULL column of o, ideally the key, so a genuine match is never mistaken for no match).
- Avoid `NOT IN (subquery)` when NULLs are possible: if no right-hand value equals the left and at least one right-hand row is NULL, the result is NULL, not true, so the row is dropped. A NULL on the left also yields NULL.
- Index the lookup column (`o.cid`); whether the planner uses an anti-join is something to confirm with EXPLAIN, not assume.
- Self-check: matched plus unmatched counts equal the parent count.

## Checked

Date: 2026-11-08

Method: Read the PostgreSQL manual pages functions-subquery.html (EXISTS, NOT IN null rules) and queries-table-expressions.html (outer joins); the draft's planner-anti-join claim is not on those pages and was reworded as an EXPLAIN check.
