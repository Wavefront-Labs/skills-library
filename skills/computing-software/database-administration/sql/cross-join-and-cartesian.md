---
id: computing-software.database-administration.sql.cross-join-and-cartesian
name: cross-join-and-cartesian
category: computing-software
field: database-administration
product: sql
tags: [sql, cross-join-and-cartesian]
level: intro
status: docs-checked
description: "Use CROSS JOIN deliberately and detect accidental Cartesian products."
sources: ["https://www.postgresql.org/docs/current/queries-table-expressions.html", "https://www.sqlite.org/lang_select.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CROSS JOIN and accidental Cartesian products

- `CROSS JOIN` returns every combination of rows: with N and M rows the result has N * M rows. Legitimate for combinations (sizes x colours) or calendar x entity grids.
- Accidental form: `FROM a, b` with the join predicate forgotten. In PostgreSQL `FROM T1 CROSS JOIN T2` is equivalent to `FROM T1, T2` and to `FROM T1 INNER JOIN T2 ON TRUE`; SQLite treats a comma join, `JOIN` or `INNER JOIN` with no `ON` or `USING` as the cartesian product too.
- PostgreSQL: a `NATURAL JOIN` between tables with no common column names behaves like `CROSS JOIN`.
- Symptom: row count equals the product of the table counts.
- Fix: use explicit `JOIN ... ON`; sanity check `count(*)` against the expected cardinality.
- Self-check: compare `count(*)` of the join with `count(*)` of the driving table.

## Checked

Date: 2026-11-07. Read the "Cross join" and "NATURAL" passages of the PostgreSQL Joined Tables page (queries-table-expressions; the rest of the page located by search, not read in full) and the join-operator passage of the SQLite SELECT page (lang_select; searched for CROSS JOIN and cartesian, not read in full). Confirmed: N * M rows, equivalence of CROSS JOIN, comma and `INNER JOIN ... ON TRUE`, NATURAL JOIN with no common columns acting as CROSS JOIN, SQLite cartesian product when no ON/USING. Removed: the claim that EXPLAIN shows a nested loop with no join condition (not on either page). Replaced the bare docs-root sources with the two specific pages.
Method: documentation only; no commands were run.
