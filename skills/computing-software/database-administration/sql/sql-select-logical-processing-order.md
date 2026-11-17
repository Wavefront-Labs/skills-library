---
id: computing-software.database-administration.sql.sql-select-logical-processing-order
name: sql-select-logical-processing-order
category: computing-software
field: database-administration
product: sql
tags: [sql, sql-select, logical-query-order, where-vs-having, column-aliases]
level: intro
status: docs-checked
description: "Reason about SELECT using its logical evaluation order, aliases, DISTINCT, ORDER BY and LIMIT."
sources: ["https://learn.microsoft.com/en-us/sql/t-sql/queries/select-transact-sql", "https://www.postgresql.org/docs/current/sql-select.html", "https://www.postgresql.org/docs/current/queries-order.html", "https://www.postgresql.org/docs/current/queries-limit.html", "https://www.postgresql.org/docs/current/tutorial-window.html", "https://www.sqlite.org/lang_select.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SELECT and logical processing order

SQL is written in one order and evaluated in another. The T-SQL manual lists the logical (binding) order as FROM, ON, JOIN, WHERE, GROUP BY, WITH CUBE or ROLLUP, HAVING, SELECT, DISTINCT, ORDER BY, TOP. The engine may physically execute differently, but names and values behave as if this order held.

- A SELECT-list alias is defined at the SELECT step, so earlier clauses cannot reference it, but later ones such as ORDER BY can (T-SQL manual). PostgreSQL agrees: an output column name can be used in ORDER BY and GROUP BY but not in WHERE or HAVING; there you write out the expression. Test other engines rather than assume.
- In PostgreSQL an ORDER BY item that is an output column name must stand alone: `ORDER BY sum` works, `ORDER BY sum + c` does not.
- Window functions are allowed only in the SELECT list and ORDER BY, not in WHERE, GROUP BY or HAVING, because they run logically after those clauses (PostgreSQL tutorial). To filter on one, compute it in a subquery or CTE and filter outside.
- `WHERE` filters rows before grouping; `HAVING` filters groups. HAVING turns a query into a grouped query even without GROUP BY.
- Without `ORDER BY` row order is unspecified (PostgreSQL, SQLite) and must not be relied on. With `LIMIT`, use an ORDER BY that gives a unique order, or different LIMIT/OFFSET values can return inconsistent subsets (PostgreSQL manual).
- `SELECT DISTINCT ON (...)` keeps the first row of each set of equal expressions and is PostgreSQL syntax; the "first" row is unpredictable without ORDER BY.
- Row limiting syntax: `FETCH { FIRST | NEXT } n ROWS ONLY` (PostgreSQL, and T-SQL after OFFSET, where it needs ORDER BY), `LIMIT n [OFFSET m]` (PostgreSQL, SQLite), `TOP (n)` (T-SQL; always pair it with ORDER BY). Skipped OFFSET rows are still computed, so a large OFFSET can be slow in PostgreSQL.
- List columns explicitly in application code rather than `SELECT *`.

Verify: run the query with the alias in WHERE on your engine and read the error or result to learn its dialect.

## Checked

2026-11-08. Confirmed against the T-SQL SELECT page (logical order, alias visibility, TOP), the PostgreSQL SELECT, ORDER BY, LIMIT/OFFSET and window tutorial pages, and the SQLite SELECT page (unordered results). Removed claims about MySQL and SQLite alias leniency, PostgreSQL 8.4 and Oracle 12c version gates, and `FETCH` support in other engines, which no fetched page states.
Method: documentation only; no commands were run.
