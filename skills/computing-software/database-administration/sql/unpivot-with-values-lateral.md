---
id: computing-software.database-administration.sql.unpivot-with-values-lateral
name: unpivot-with-values-lateral
category: computing-software
field: database-administration
product: sql
tags: [sql, unpivot-with-values-lateral]
level: practitioner
status: docs-checked
description: "Turn columns into rows with VALUES and LATERAL or UNION ALL."
sources: ["https://www.postgresql.org/docs/current/queries-table-expressions.html", "https://www.postgresql.org/docs/current/queries-values.html", "https://learn.microsoft.com/en-us/sql/t-sql/queries/from-using-pivot-and-unpivot"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Unpivoting columns to rows

- PostgreSQL: `SELECT t.id, v.k, v.val FROM t CROSS JOIN LATERAL (VALUES ('q1', t.q1), ('q2', t.q2)) AS v(k, val);`. A `LATERAL` item may reference columns of FROM items to its left and is evaluated once per row of those items; the VALUES list is a constant table, and an alias column list names its columns (otherwise they are `column1`, `column2`).
- Portable: `SELECT id, 'q1' AS k, q1 AS val FROM t UNION ALL SELECT id, 'q2', q2 FROM t;`. VALUES is documented as equivalent to a chain of SELECT ... UNION ALL.
- SQL Server has an `UNPIVOT` operator that rotates columns into row values. It is not an exact reverse of PIVOT, and NULL values in its input disappear from the output, which differs from the VALUES and UNION ALL forms where NULLs come through. Repeated PIVOT/UNPIVOT in one statement can hurt performance. Unpivoted column names become `nvarchar(128)` values.
- With the VALUES or UNION ALL forms, filter `WHERE val IS NOT NULL` if you want the UNPIVOT behaviour.
- Self-check: row count equals source rows x columns unpivoted (before any NULL filter).

## Checked

2026-11-08. Confirmed against the PostgreSQL pages on table expressions (LATERAL subqueries) and VALUES lists, and the T-SQL PIVOT and UNPIVOT page (NULL behaviour, nvarchar(128)). Removed the Oracle and DuckDB UNPIVOT mentions, which no fetched page covers.
Method: documentation only; no commands were run.
