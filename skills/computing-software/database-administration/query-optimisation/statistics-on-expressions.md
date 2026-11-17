---
id: computing-software.database-administration.query-optimisation.statistics-on-expressions
name: statistics-on-expressions
category: computing-software
field: database-administration
product: query-optimisation
tags: [database-administration, query-optimisation, expression-statistics, function-based-statistics, query-statistics, cardinality-estimation, extended-statistics]
level: practitioner
status: docs-checked
description: "Give the optimiser statistics for predicates on expressions like lower(email): PostgreSQL expression statistics, SQL Server computed columns, Oracle extended statistics."
sources:
  - https://www.postgresql.org/docs/current/sql-createstatistics.html
  - https://www.postgresql.org/docs/current/planner-stats.html
  - https://learn.microsoft.com/en-us/sql/relational-databases/indexes/indexes-on-computed-columns
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Statistics on expressions and functions

## The problem
`WHERE lower(email) = 'a@x.io'` or `WHERE date_trunc('day', created_at) = '2026-10-18'`: column statistics describe `email` and `created_at`, not the expression result. Without statistics on the expression the planner has no information about its distribution and uses default estimates, producing wrong row estimates.

## PostgreSQL
- `CREATE STATISTICS` accepts an expression: univariate statistics on one expression, or a list of columns and/or expressions for multivariate statistics (separate univariate statistics are then built for each expression). The reference says expression statistics are similar to an index on the expression without the index maintenance overhead:
```sql
CREATE STATISTICS orders_day_stats ON (date_trunc('day', created_at)) FROM orders;
ANALYZE orders;
```
- Combine expressions and columns: `CREATE STATISTICS s (dependencies, mcv) ON (lower(city)), country FROM addresses;`.

## SQL Server
Create a computed column (it can be non-persisted) and statistics or an index on it; for a multi-variable expression the SQL Server statistics page suggests exactly this (computed column, then statistics or an index on it):
```sql
ALTER TABLE dbo.users ADD email_lower AS LOWER(email);
CREATE STATISTICS st_email_lower ON dbo.users(email_lower);
```

## Oracle
An extension is a column group or an expression; `DBMS_STATS.CREATE_EXTENDED_STATS` creates extensions, and the database gathers their statistics when a user-generated or automatic job gathers statistics for the table:
```sql
SELECT DBMS_STATS.CREATE_EXTENDED_STATS(user, 'USERS', '(LOWER(EMAIL))') FROM dual;
```

## Better: avoid needing them
Rewrite predicates to be sargable on the base column when possible: `created_at >= '2026-10-18' AND created_at < '2026-10-19'` instead of `date_trunc(...) =`.

## Verify
`EXPLAIN ANALYZE`: estimated rows for the filter move close to actual rows after creating the statistics and analyzing.

## Checked
2026-11-01. Confirmed against the PostgreSQL CREATE STATISTICS page (expression syntax, comparison to an index, default estimates without statistics), the SQL Server statistics page (computed column then statistics or index) and the Oracle extended statistics page (expression extensions, CREATE_EXTENDED_STATS). Removed: default selectivity figures, PostgreSQL version gate, pg_stats view queries, MySQL section, Oracle hidden-virtual-column claim, SQL Server expression-matching claim.
Method: documentation only; no commands were run.
