---
id: computing-software.database-administration.query-optimisation.join-cardinality-misestimates
name: join-cardinality-misestimates
category: computing-software
field: database-administration
product: query-optimisation
tags: [database-administration, query-optimisation, join-cardinality, cardinality-estimation, query-statistics, execution-plans, misestimate]
level: practitioner
status: draft
description: "Diagnose and fix join cardinality misestimates that cause wrong join orders and methods: correlated join keys, skew, multi-column joins, and the fixes per engine."
sources:
  - https://www.postgresql.org/docs/current/planner-stats-details.html#PLANNER-STATS-DETAILS-JOIN
  - https://learn.microsoft.com/en-us/sql/relational-databases/performance/cardinality-estimation-sql-server
  - https://www.vldb.org/pvldb/vol9/p204-leis.pdf
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Join cardinality misestimates

## Why joins are the weak spot
Optimisers estimate join output as roughly `rows(A) * rows(B) * selectivity(join)`, assuming independence and uniform distribution. Errors multiply through each join: research on real workloads ("How Good Are Query Optimizers, Really?", Leis et al.) shows estimates off by orders of magnitude after 3-4 joins. Wrong estimates pick nested loops for large inputs or hash joins with tiny memory.

## Find the bad node
Compare estimated vs actual rows per join node:
```text
Nested Loop  (cost=... rows=12 ...) (actual ... rows=480000 loops=1)
```
The first node (bottom-up) where the ratio jumps > 10x is the root cause; everything above inherits the error.

## Common causes and fixes
| Cause | Fix |
|---|---|
| Filters on correlated columns before the join (city + postcode) | Extended statistics (PG `CREATE STATISTICS (dependencies, mcv)`), multi-column stats (SQL Server `CREATE STATISTICS ... (a, b)`), column group stats (Oracle) |
| Multi-column join keys `ON a.x = b.x AND a.y = b.y` | Multi-column statistics help the filters; multi-column join estimates stay weak in most engines, so consider a single surrogate join key |
| Skewed join key (one customer owns 40% of rows) | Histograms / MCV lists with larger statistics targets; literal values instead of parameters for skewed lookups |
| Function/expression on join or filter column | Index or statistics on the expression; rewrite predicate |
| Stale stats after bulk load | ANALYZE / UPDATE STATISTICS right after loads |
| Table variables / temp tables without stats | Use temp tables with stats, or recompile |

## Engine-specific tools
- PostgreSQL: `default_statistics_target` / `ALTER TABLE ... ALTER COLUMN ... SET STATISTICS 1000`; `pg_hint_plan` for emergency control; `join_collapse_limit` to fix join order of explicit JOINs.
- SQL Server: choose cardinality estimator model (`LEGACY_CARDINALITY_ESTIMATION` database scoped config or `USE HINT('FORCE_LEGACY_CARDINALITY_ESTIMATION')`); Query Store plan forcing; CE feedback (2022).
- Oracle: dynamic sampling, SQL plan directives, adaptive joins; SQL profiles via SQL Tuning Advisor.
- MySQL: histograms (`ANALYZE TABLE t UPDATE HISTOGRAM ON col`), optimizer hints `JOIN_ORDER`, `STRAIGHT_JOIN`.

## Structural fixes
Break a 10-way join into a staged query (materialise an intermediate with accurate row count, e.g. temp table + ANALYZE) when estimates cannot be made right.

## Verify
After the fix, estimated and actual rows on the formerly bad node are within ~10x, and the join method/order changes to the expected one with lower runtime.
