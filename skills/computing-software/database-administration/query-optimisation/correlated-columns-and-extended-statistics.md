---
id: computing-software.database-administration.query-optimisation.correlated-columns-and-extended-statistics
name: correlated-columns-and-extended-statistics
category: computing-software
field: database-administration
product: query-optimisation
tags: [database-administration, query-optimisation, cardinality-estimation, extended-statistics, correlated-columns, create-statistics, multi-column-statistics, column-group-statistics, functional-dependencies, underestimate]
level: advanced
status: docs-checked
description: "Fix row underestimates from correlated predicates (city AND zip) with multi-column statistics: PostgreSQL CREATE STATISTICS, SQL Server multi-column stats, Oracle column groups."
sources:
  - https://www.postgresql.org/docs/current/planner-stats.html#PLANNER-STATS-EXTENDED
  - https://learn.microsoft.com/en-us/sql/relational-databases/statistics/statistics
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/tgsql/managing-extended-statistics.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Correlated columns and extended statistics

**Goal:** the optimizer stops multiplying selectivities of dependent columns and
choosing nested loops for queries that return far more rows than it thinks.

## The problem
`WHERE city = 'Berlin' AND zip = '10115'`: optimizers assume independence, so
est. rows = rows × sel(city) × sel(zip). But zip implies city: the true
selectivity is sel(zip). The estimate is far too low → wrong join order/method.
Spot it in `EXPLAIN ANALYZE`: estimated rows much lower than actual on a node
filtering two related columns.

## PostgreSQL
```sql
CREATE STATISTICS addr_dep (dependencies, ndistinct, mcv) ON city, zip FROM addresses;
ANALYZE addresses;
```
The PostgreSQL planner-stats page shows how to inspect the stored results.
- `dependencies`: functional dependencies; applied only to simple equality conditions against constants and IN clauses with constants, not to range, LIKE or column-to-column conditions.
- `ndistinct`: n-distinct estimates for groups of columns (GROUP BY city, zip).
- `mcv`: most-common-value lists on column combinations.
PostgreSQL also accepts expressions in `CREATE STATISTICS`.

## SQL Server
Multi-column statistics store densities (correlation information) for each prefix of
the key columns, and a histogram only on the first column:
```sql
CREATE STATISTICS st_city_zip ON dbo.addresses (city, zip) WITH FULLSCAN;
```
Densities exist only for leading column prefixes of the statistics object, so order the key columns to match the predicates.

## Oracle
```sql
SELECT DBMS_STATS.CREATE_EXTENDED_STATS(user, 'ADDRESSES', '(CITY,ZIP)') FROM dual;
```
The database gathers statistics for the extension when a user-generated or automatic statistics gathering job next gathers statistics for the table.
`DBMS_STATS.SEED_COL_USAGE` + `REPORT_COL_USAGE` can find candidate groups from the workload.

## Gotchas
- Extended stats only help predicates matching their column set (and simple
  equality/IN for dependencies in PostgreSQL).
- PostgreSQL's page advises creating ndistinct objects only for column groups actually used for
  grouping; otherwise ANALYZE cycles are wasted. Add stats for problem queries, not every pair.

## Checked
2026-11-01. Confirmed against the PostgreSQL planner-stats and CREATE STATISTICS pages (dependencies,
ndistinct, mcv, applicability limits, independence assumption), the SQL Server statistics page
(densities per column prefix, histogram on first column, FULLSCAN) and the Oracle extended statistics
page (column groups, CREATE_EXTENDED_STATS, SEED_COL_USAGE, REPORT_COL_USAGE). Removed: pg_stats_ext
query, PG14 version gate, SQL Server estimator-version claim, composite-index auto-statistics claim,
MySQL section, 1000x figure.
Method: documentation only; no commands were run.

## Verify
Re-run `EXPLAIN ANALYZE`: estimated rows within a small factor of actual, and the
plan shape changed (e.g. hash join instead of nested loop).
