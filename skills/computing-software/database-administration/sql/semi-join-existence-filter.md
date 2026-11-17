---
id: computing-software.database-administration.sql.semi-join-existence-filter
name: semi-join-existence-filter
category: computing-software
field: database-administration
product: sql
tags: [sql, semi-join-existence-filter]
level: practitioner
status: docs-checked
description: "Filter parents by child existence without fanning out rows."
sources: ["https://www.postgresql.org/docs/current/functions-subquery.html", "https://www.postgresql.org/docs/current/queries-table-expressions.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Semi-join existence filters without duplicates

- Joining parents to children returns one output row per matching pair, so a parent with several children repeats; `WHERE EXISTS (SELECT 1 FROM child WHERE child.pid = parent.id)` returns each parent at most once because EXISTS only tests whether the subquery returns any row. The manual says the output list is normally unimportant and the subquery generally stops once a row is found.
- Avoid patching a join's duplicates with DISTINCT afterwards: it hides the intent and forces extra work (common practice, not from the manual).
- `IN (SELECT ...)` also filters without fan-out; it differs from EXISTS only in NULL handling, which matters for the negated forms (see not-exists-anti-join).
- PostgreSQL EXPLAIN may show a Semi Join node for EXISTS or IN; the cited pages do not describe this, so confirm it in your own plan.
- Self-check: the result row count must not exceed the parent table count.

## Checked

Date: 2026-11-08

Method: Read the PostgreSQL manual pages functions-subquery.html (EXISTS) and queries-table-expressions.html (joined tables); planner and DISTINCT-cost remarks are labelled as unverified practice because those pages do not cover them.
