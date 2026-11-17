---
id: computing-software.database-administration.sql.union-all-vs-union
name: union-all-vs-union
category: computing-software
field: database-administration
product: sql
tags: [sql, union-all-vs-union]
level: intro
status: docs-checked
description: "Choose UNION ALL by default and know when UNION dedupe is needed."
sources: ["https://www.postgresql.org/docs/current/queries-union.html", "https://www.sqlite.org/lang_select.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# UNION versus UNION ALL

- `UNION` eliminates duplicate rows from its result in the same way as `DISTINCT`; `UNION ALL` keeps every row. Default to UNION ALL unless you need the dedupe, since removing duplicates is extra work you only want when the result needs it.
- Both queries must be union compatible: the same number of columns, with compatible types in corresponding positions.
- `INTERSECT` and `EXCEPT` also remove duplicates unless `ALL` is given (PostgreSQL). SQLite's INTERSECT and EXCEPT always remove them and it has no INTERSECT ALL or EXCEPT ALL form in its compound operator list.
- Precedence in PostgreSQL: UNION and EXCEPT associate left to right, INTERSECT binds more tightly; use parentheses to be explicit. SQLite groups all compound operators left to right.
- A trailing ORDER BY or LIMIT applies to the whole result: `SELECT a FROM b UNION SELECT x FROM y LIMIT 10` limits the union. To limit one branch in PostgreSQL, parenthesise it. SQLite does not allow ORDER BY or LIMIT inside a branch of a compound SELECT; they go only at the end.
- Row order from UNION is not guaranteed (PostgreSQL).
- Gotcha (SQLite): for duplicate detection in compound SELECTs, NULL values are equal to other NULLs. No affinity conversion is applied to compared values.
- Self-check: `count(*)` of UNION ALL equals the sum of branch counts.

## Checked

2026-11-08. Confirmed against the PostgreSQL Combining Queries page and the SQLite SELECT page (compound SELECT section). Removed unsupported claims: that the cost is "sort or hash", that column names come from the first query, and that UNION treats NULLs as equal in general (the SQLite page states this for SQLite only). Replaced the lang.html and docs root sources.

Method: documentation only; no commands were run.
