---
id: computing-software.database-administration.duckdb.duckdb-pivot
name: duckdb-pivot
category: computing-software
field: database-administration
product: duckdb
tags: [duckdb, pivot, pivot-wider, reshape, aggregate, on-using-group-by]
level: practitioner
status: docs-checked
description: "Turn rows into columns in DuckDB with the simplified PIVOT ON/USING/GROUP BY syntax or SQL-standard PIVOT ... FOR ... IN, plus naming, IN filters and limitations."
sources:
  - https://raw.githubusercontent.com/duckdb/duckdb-web/main/docs/1.4/sql/statements/pivot.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: pivot distinct values of a column into their own columns. `PIVOT_WIDER` is a synonym of `PIVOT`; the inverse is `UNPIVOT` (see `duckdb-unpivot`).

Simplified syntax (columns auto-detected): `PIVOT dataset ON columns USING values GROUP BY rows ORDER BY ... LIMIT n;`. `ON`, `USING` and `GROUP BY` are each optional but not all can be omitted. `USING` defaults to `count(*)`.

```sql
PIVOT cities ON year USING sum(population);                    -- keeps all other columns as row keys
PIVOT cities ON year USING first(population);                  -- reshape without aggregating (works for text)
PIVOT cities ON year USING sum(population) GROUP BY country;   -- only listed row columns
PIVOT cities ON year IN (2000, 2010) USING sum(population) GROUP BY country;  -- restrict columns
PIVOT cities ON country, name USING sum(population);           -- Cartesian product of values, names like NL_Amsterdam
PIVOT cities ON country || '_' || name USING sum(population);  -- expression: only combinations that exist
PIVOT cities ON year USING sum(population) AS total, max(population) AS max GROUP BY country;  -- columns 2000_total, 2000_max
```

GROUP BY takes column names only (no positions, no expressions). `FILTER` clauses in `USING` are silently ignored. PIVOT can appear as a CTE body (no SELECT needed) or in a parenthesised subquery, and two pivots sharing GROUP BY columns can be joined: `FROM (PIVOT ...) a JOIN (PIVOT ...) b USING (country)`.

SQL-standard form needs an explicit `IN` list per column, no commas between `FOR` items but commas between values and GROUP BY:

```sql
SELECT * FROM cities
PIVOT (sum(population) FOR year IN (2000, 2010, 2020) GROUP BY country);
-- multiple FOR columns: year IN (2000, 2010) country IN ('NL','US') -> 2000_NL_total ...
```

Limitation: USING accepts only an aggregate, not an expression. `USING sum(population) * 1000` fails with `Catalog Error: * is not an aggregate function`. Workaround: pivot first, then `SELECT country, name, 1000 * COLUMNS(* EXCLUDE (country, name)) FROM (PIVOT cities ON year USING sum(population));`.

## Checked

2026-11-07. Read the DuckDB 1.4 docs page sql/statements/pivot.md in full. Confirmed: PIVOT_WIDER synonym, simplified syntax and its optional clauses, `count(*)` default, every example including IN filter, multiple ON columns (Cartesian product, NULL for absent combinations), ON expression, USING aliases, GROUP BY column-name-only rule, silently ignored FILTER, CTE and subquery use, joining pivots, SQL-standard form with its comma rules, the aggregate-only limitation, the error text (the page prints `Catalog Error:` then `* is not an aggregate function` on two lines) and the COLUMNS workaround. Removed the invented Verify step.

Method: documentation only; no commands were run.
