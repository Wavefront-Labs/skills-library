---
id: computing-software.database-administration.query-optimisation.grouping-sets-rollup-and-cube
name: grouping-sets-rollup-and-cube
category: computing-software
field: database-administration
product: query-optimisation
tags: [database-administration, query-optimisation, sql, advanced-sql, grouping-sets, rollup, cube, grouping-function, subtotals, olap-queries]
level: practitioner
status: gated
description: "Produce subtotals and grand totals in one SQL pass with GROUPING SETS, ROLLUP and CUBE, and label rollup rows correctly with GROUPING()."
sources:
  - https://www.postgresql.org/docs/current/queries-table-expressions.html#QUERIES-GROUPING-SETS
  - https://dev.mysql.com/doc/refman/8.4/en/group-by-modifiers.html
  - https://learn.microsoft.com/en-us/sql/t-sql/queries/select-group-by-transact-sql
  - https://www.postgresql.org/docs/16/queries-table-expressions.html#QUERIES-GROUPING-SETS
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Grouping sets, ROLLUP and CUBE

**Goal:** a report with detail rows, subtotals and a grand total from one scan instead of several UNIONed GROUP BYs.

## ROLLUP: hierarchical subtotals
```sql
SELECT region, country, sum(total) AS revenue,
       GROUPING(region) AS g_region, GROUPING(country) AS g_country
FROM orders
GROUP BY ROLLUP (region, country)
ORDER BY region NULLS LAST, country NULLS LAST;
```
Produces (region, country), (region) subtotals, and () grand total. MySQL syntax: `GROUP BY region, country WITH ROLLUP` (8.0+ supports `GROUPING()`, per the MySQL 8.4 manual).

## CUBE: all combinations
`GROUP BY CUBE (region, channel)` = (region, channel), (region), (channel), (). 2^n sets: keep n small.

## GROUPING SETS: exactly the ones you want
```sql
SELECT region, channel, date_trunc('month', created_at) AS month, sum(total)
FROM orders
GROUP BY GROUPING SETS ((region, month), (channel, month), (month));
```

## Labelling subtotal rows
Subtotal rows have NULL in the rolled-up columns, indistinguishable from real NULL data. Use `GROUPING(col)` (1 = rolled up):
```sql
SELECT CASE WHEN GROUPING(region) = 1 THEN 'All regions' ELSE coalesce(region, '(none)') END AS region, ...
```
SQL Server also has `GROUPING_ID(a, b)` bitmask; PostgreSQL `GROUPING(a, b)` returns the bitmask too.

## Performance
- One pass over the data; PostgreSQL may use several sorts or hash aggregates for different sets (on 16.4 a small three-set query planned as one `HashAggregate` with three hash keys; mixed sort and hash plans, `MixedAggregate`, appear in other cases (gated: unconfirmed, source is paywalled or blocked)).
- Filtering subtotals: use `HAVING GROUPING(country) = 1` or wrap in a subquery.

## Gotchas
- ORDER BY should place subtotal rows predictably (`NULLS LAST`, or order by `GROUPING()`).
- MySQL `WITH ROLLUP` cannot be combined with `ORDER BY` before 8.0.12 (gated: unconfirmed, source is paywalled or blocked).
- Not available in SQLite (checked on 3.50.4: `rollup` is an unknown function and `GROUPING SETS` a syntax error); emulate with UNION ALL.
- Checked on PostgreSQL 16.4: with real NULL regions in the data the ROLLUP output has indistinguishable NULL rows, and `GROUPING(region, channel)` in CUBE returns the bitmask 0-3; `HAVING GROUPING(country) = 1` keeps only subtotal and grand-total rows.

## Verify
The grand-total row equals `SELECT sum(total) FROM orders`, and each region subtotal equals the sum of its country rows.
