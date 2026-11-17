---
id: computing-software.database-administration.sql.except-intersect-set-diff
name: except-intersect-set-diff
category: computing-software
field: database-administration
product: sql
tags: [sql, except-intersect-set-diff]
level: practitioner
status: docs-checked
description: "Compare datasets with EXCEPT and INTERSECT, including ALL variants."
sources: ["https://www.postgresql.org/docs/current/queries-union.html", "https://www.postgresql.org/docs/current/sql-select.html", "https://www.sqlite.org/lang_select.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# EXCEPT and INTERSECT for set comparison

- `a EXCEPT b` returns rows of a that are not in b, duplicates eliminated; `INTERSECT` returns rows in both, duplicates eliminated. Both queries need the same number of columns with compatible types.
- PostgreSQL: `EXCEPT ALL` / `INTERSECT ALL` keep duplicates. A row with m copies on the left and n on the right appears `max(m-n,0)` times for `EXCEPT ALL` and `min(m,n)` times for `INTERSECT ALL`. `DISTINCT` can be written to state the default explicitly.
- SQLite: the compound operators are `UNION`, `UNION ALL`, `INTERSECT` and `EXCEPT` only; `INTERSECT` and `EXCEPT` remove duplicates, and there is no `ALL` form of them.
- Reconcile two tables: run `a EXCEPT b` and `b EXCEPT a`; both empty means the two have the same distinct rows (use the `ALL` forms in PostgreSQL if duplicate counts matter).
- Precedence (PostgreSQL): `INTERSECT` binds more tightly than `UNION` and `EXCEPT`, which associate left to right at the same level; use parentheses. `ORDER BY` and `LIMIT` written after the last query apply to the whole result, not the last query.
- Self-check: run the check in both directions.

## Checked

Date: 2026-11-07. Read the whole PostgreSQL Combining Queries page (queries-union) and the UNION, INTERSECT and EXCEPT clause sections of the PostgreSQL SELECT page (located by search, those sections read); read SQLite SELECT section 3 (Compound Select Statements). Confirmed: ALL multiplicities (min(m,n), max(m-n,0)), INTERSECT precedence, left-to-right association, SQLite operator list and duplicate removal. Removed: "Oracle spells it MINUS" (not from Oracle docs). Changed "not SQLite" to the SQLite operator list from its page, which is the supporting evidence for the missing ALL forms.
Method: documentation only; no commands were run.
