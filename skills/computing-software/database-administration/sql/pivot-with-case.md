---
id: computing-software.database-administration.sql.pivot-with-case
name: pivot-with-case
category: computing-software
field: database-administration
product: sql
tags: [sql, pivot-with-case]
level: practitioner
status: docs-checked
description: "Pivot rows into columns using conditional aggregation."
sources: ["https://www.postgresql.org/docs/current/sql-expressions.html", "https://www.postgresql.org/docs/current/tablefunc.html", "https://learn.microsoft.com/en-us/sql/t-sql/queries/from-using-pivot-and-unpivot"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Pivoting rows to columns with CASE

- `SELECT product, sum(CASE WHEN q = 1 THEN amt END) AS q1, sum(CASE WHEN q = 2 THEN amt END) AS q2 FROM s GROUP BY product;` A CASE with no ELSE yields NULL, which aggregates skip.
- Plain SQL: the output columns must be written out in advance, so dynamic pivots need generated SQL.
- PostgreSQL `FILTER` is shorter: `sum(amt) FILTER (WHERE q = 1) AS q1`; only rows where the filter is true are fed to the aggregate.
- PostgreSQL `crosstab(text)` (tablefunc extension) takes a query returning row_name, category and value columns, ordered (`ORDER BY 1,2`); the output columns must still be declared in the calling FROM clause, and short groups are padded with NULLs.
- SQL Server has a `PIVOT` operator: `PIVOT (AVG(x) FOR col IN ([0],[1],...))` with explicitly listed values; NULLs in the value column are not considered in the aggregation, and repeated PIVOT/UNPIVOT in one statement can hurt performance.
- Self-check: row totals across pivot columns equal the unpivoted sum.

## Checked

Date: 2026-11-08

Method: Read the PostgreSQL manual pages sql-expressions.html (FILTER) and tablefunc.html and the Microsoft Learn PIVOT page; the draft's "works on every engine" and Oracle PIVOT claims were dropped because no cited page covers them.
