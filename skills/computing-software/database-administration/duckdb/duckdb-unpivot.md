---
id: computing-software.database-administration.duckdb.duckdb-unpivot
name: duckdb-unpivot
category: computing-software
field: database-administration
product: duckdb
tags: [duckdb, unpivot, pivot-longer, reshape, columns-expression, wide-to-long]
level: practitioner
status: docs-checked
description: "Stack DuckDB columns into name/value rows with UNPIVOT ON ... INTO NAME ... VALUE, dynamic COLUMNS lists, multi-value sets and the SQL-standard FOR ... IN form."
sources:
  - https://raw.githubusercontent.com/duckdb/duckdb-web/main/docs/1.4/sql/statements/unpivot.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: convert wide columns into long rows. `PIVOT_LONGER` is a synonym of `UNPIVOT`; inverse is `PIVOT` (`duckdb-pivot`).

Simplified syntax: `UNPIVOT dataset ON column(s) INTO NAME name_col VALUE value_col(s) [ORDER BY ...] [LIMIT n];`

```sql
UNPIVOT monthly_sales ON jan, feb, mar, apr, may, jun INTO NAME month VALUE sales;

-- dynamic: survives new month columns
UNPIVOT monthly_sales ON COLUMNS(* EXCLUDE (empid, dept)) INTO NAME month VALUE sales;

-- multiple value columns: each ON set must match the VALUE column count; aliases optional
UNPIVOT monthly_sales
    ON (jan, feb, mar) AS q1, (apr, may, jun) AS q2
    INTO NAME quarter VALUE month_1_sales, month_2_sales, month_3_sales;

-- single-column expressions and casts are allowed
UNPIVOT (SELECT 42 AS col1, 'woot' AS col2) ON (col1 * 2)::VARCHAR, col2;   -- name/value rows
```

The unpivoted rows keep the other columns (here `empid`, `dept`). Used as a CTE or subquery, `UNPIVOT` replaces the SELECT (no `SELECT` inside the CTE); in a subquery it must be parenthesised.

SQL-standard syntax:

```sql
FROM monthly_sales UNPIVOT (sales FOR month IN (jan, feb, mar, apr, may, jun));
FROM monthly_sales UNPIVOT (sales FOR month IN (columns(* EXCLUDE (empid, dept))));
FROM monthly_sales UNPIVOT (
    (month_1_sales, month_2_sales, month_3_sales)
    FOR quarter IN ((jan, feb, mar) AS q1, (apr, may, jun) AS q2)
);
```
Only one name column can follow `FOR`. The standard form accepts `UNPIVOT INCLUDE NULLS (...)` as shown in the syntax summary.

Note: the page's example table declares `Jan` etc. while its statements write `jan`; the page's output shows the capitalised names `Jan`, `Feb` and so on in the `month` column. The six-month example on 3 input rows returns 18 rows.

## Checked

2026-11-07. Read the DuckDB 1.4 docs page sql/statements/unpivot.md in full. Confirmed: `PIVOT_LONGER` synonym, PIVOT as inverse, simplified syntax summary, manual, COLUMNS and multiple-value-column examples with their results (18 and 6 rows), optional aliases and the matching column count rule, CTE without SELECT, parenthesised subquery, single-column expressions and casts with the name/value output, the standard syntax summary with `INCLUDE NULLS`, one name column only, standard dynamic and multi-value forms. Changed: removed the unconfirmed claim that identifiers are case-insensitive and the generalised row-count Verify formula; kept the observable fact from the page.

Method: documentation only; no commands were run.
