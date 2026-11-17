---
id: computing-software.database-administration.sql.sql-join-types-and-semantics
name: sql-join-types-and-semantics
category: computing-software
field: database-administration
product: sql
tags: [sql, sql-joins, inner-join, left-join, cross-join, join-duplication]
level: practitioner
status: docs-checked
description: "Choose INNER, LEFT, FULL, CROSS and self joins and avoid row multiplication from one-to-many joins."
sources: ["https://www.postgresql.org/docs/current/queries-table-expressions.html", "https://www.sqlite.org/lang_select.html", "https://www.sqlite.org/lang_expr.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Joins

- `INNER JOIN` (the default) keeps pairs of rows for which the `ON` condition is true. `LEFT JOIN` also keeps each left row with no match, with NULLs in the right-hand columns; `RIGHT JOIN` is the mirror and `FULL JOIN` keeps unmatched rows from both sides. `CROSS JOIN` pairs every row of T1 with every row of T2 (N x M rows) and equals `FROM T1, T2`. PostgreSQL and current SQLite both document RIGHT and FULL joins; check an older engine version before relying on them. A self join aliases the same table twice (employee/manager).
- Put filters on the right table of a LEFT JOIN in the `ON` clause; in `WHERE` they discard the null-extended rows and turn it into an inner join. PostgreSQL's explanation: an `ON` restriction is processed before the join, a `WHERE` restriction after it, which does not matter for inner joins but matters a lot for outer joins. Example from the docs: `t1 LEFT JOIN t2 ON t1.num = t2.num AND t2.value = 'xxx'` keeps all t1 rows, while moving the test to `WHERE` keeps only matching ones.
- Joining two one-to-many branches from the same parent multiplies rows (fan-out) and inflates `SUM`/`COUNT`; aggregate each branch in a subquery first, or use `COUNT(DISTINCT ...)` knowingly.
- Prefer explicit `JOIN ... ON` over comma joins. In PostgreSQL `JOIN` binds more tightly than the comma, so `FROM T1, T2 INNER JOIN T3 ON ...` cannot reference T1 in the condition. `USING (col)` is shorthand for equality on shared column names, outputs one column per listed pair, and is reasonably safe from schema changes.
- `NATURAL JOIN` uses every column name present in both tables, so adding a new same-named column to either table silently changes the join; if there are no common columns it behaves like `CROSS JOIN`. PostgreSQL calls it considerably more risky than `USING`.
- NULL never equals NULL in `ON`: where NULL keys must match, use `IS NOT DISTINCT FROM`, the standard spelling (SQLite also accepts `IS`, an SQLite extension).
- Anti join: `NOT EXISTS` or `LEFT JOIN ... WHERE r.id IS NULL`; semi join: `EXISTS`.

Verify: compare `COUNT(*)` of the parent table before and after the join.

## Checked

2026-11-08. Read: PostgreSQL 7.2.1 Table Expressions, joined-tables section (CROSS, INNER, outer joins, `USING`, `NATURAL`, `ON` versus `WHERE` example); SQLite SELECT, FROM clause join rules (cartesian product, `ON`, `USING`, `NATURAL`, LEFT, RIGHT, FULL); SQLite expression page `IS DISTINCT FROM` paragraph. Removed unconfirmed claims: that MySQL lacks `FULL OUTER JOIN` and that older SQLite lacks it (no version stated on the pages read); the anti-join and fan-out advice is general practice rather than page content.
Method: documentation only; no commands were run.
