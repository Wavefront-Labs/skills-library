---
id: computing-software.database-administration.query-optimisation.reading-execution-plans
name: reading-execution-plans
category: computing-software
field: database-administration
product: query-optimisation
tags: [database-administration, query-optimisation, query-optimization, sql, execution-plan, query-plan, explain, explain-analyze, explain-buffers, showplan, postgresql, mysql, sql-server, cardinality-estimation, estimated-vs-actual-rows, sargability, sargable, nested-loop, hash-join, merge-join, covering-index, index-only-scan, key-lookup, seq-scan, statistics, query-tuning, slow-query]
level: practitioner
status: draft
description: "Read execution plans in PostgreSQL, MySQL and SQL Server: compare estimated vs actual rows, spot non-sargable predicates, judge join algorithms and add covering indexes."
sources:
  - https://www.postgresql.org/docs/current/using-explain.html
  - https://dev.mysql.com/doc/refman/8.4/en/explain.html
  - https://learn.microsoft.com/en-us/sql/relational-databases/performance/display-an-actual-execution-plan
  - https://use-the-index-luke.com/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Reading execution plans — find the operator where the estimate went wrong

**Goal:** turn a slow query into one specific cause (bad estimate, unusable predicate,
wrong join, missing covering index) by reading the plan the engine actually ran.

## 1. Get the actual plan, not the estimate
| Engine | Command |
|---|---|
| PostgreSQL | `EXPLAIN (ANALYZE, BUFFERS, SETTINGS) SELECT ...;` |
| MySQL 8.0.18+ | `EXPLAIN ANALYZE SELECT ...;` (tree format); `EXPLAIN FORMAT=TREE` without running |
| SQL Server | SSMS *Include Actual Execution Plan* (Ctrl+M), or `SET STATISTICS XML ON;` plus `SET STATISTICS IO, TIME ON;` |

`ANALYZE` executes the statement. For `UPDATE`/`DELETE` wrap it:
`BEGIN; EXPLAIN ANALYZE ...; ROLLBACK;`. Use realistic parameter values: the plan for
`tenant_id = 1` (huge tenant) may differ from `tenant_id = 9999`.

## 2. Read it in this order
1. **Where does the time go?** Postgres shows `actual time=first..last` per node,
   per loop (multiply by `loops`). MySQL shows the same `actual time`. SQL Server
   shows per-operator elapsed time in actual plans (2016 SP1+/2017+; check yours).
   Find the node where time jumps.
2. **Estimated vs actual rows** on that node and its children. Postgres
   `rows=10` (estimate) vs `actual ... rows=480000`; SQL Server "Estimated Number of
   Rows" vs "Actual Number of Rows". Off by 10× or more = the optimiser chose the plan
   for a different query. Fix the estimate first; everything downstream follows.
3. **Rows read vs rows returned.** Postgres `Rows Removed by Filter`, MySQL
   `rows_examined`, SQL Server "Number of Rows Read" vs "Actual Number of Rows". Reading
   1M to return 20 means the index doesn't serve the predicate.
4. **I/O:** Postgres `Buffers: shared hit/read`, SQL Server `logical reads`. Reads are
   a more stable metric than milliseconds.
5. **Spills/warnings:** Postgres `Sort Method: external merge Disk:`, SQL Server
   spill warnings, MySQL `Using temporary; Using filesort`: memory grant or `work_mem`
   too low, or an avoidable sort.

## 3. Common causes of bad estimates
- Stale statistics: `ANALYZE t;` / `ANALYZE TABLE t;` / `UPDATE STATISTICS t;`.
- Correlated columns (`city`, `postcode`): Postgres `CREATE STATISTICS ... (dependencies)`
  on both; SQL Server multi-column stats.
- Skewed values with a cached generic plan (parameter sniffing).
- Functions/table variables/CTEs the optimiser can't see into.

## 4. Sargability: can the index be used?
A predicate is sargable when the indexed column appears bare on one side.
| Not sargable | Sargable rewrite |
|---|---|
| `WHERE date(created_at) = '2026-10-01'` | `WHERE created_at >= '2026-10-01' AND created_at < '2026-10-02'` |
| `WHERE lower(email) = $1` | expression index on `lower(email)`, or a case-insensitive collation |
| `WHERE amount + 10 > 100` | `WHERE amount > 90` |
| `WHERE name LIKE '%son'` | trigram index (Postgres `pg_trgm`) or full-text |
| `WHERE varchar_col = N'abc'` (SQL Server) | match parameter type to column type |
Implicit type conversion is the stealthy case: the plan shows a `CONVERT_IMPLICIT` or
a cast on the column, and a scan instead of a seek.

## 5. Join algorithms: is the choice sane?
| Algorithm | Good when | Red flag |
|---|---|---|
| Nested loop | small outer input, indexed inner lookup | outer actual rows in the hundreds of thousands |
| Hash join | large unsorted inputs, equality joins | build side larger than memory (spill) |
| Merge join | both inputs already sorted on the key | explicit Sort nodes added just to merge |
A nested loop over 500k rows is almost always an underestimate upstream, not a reason
to force hash joins with hints.

## 6. Covering indexes
If the plan shows an index seek followed by a lookup per row (SQL Server Key Lookup,
Postgres `Index Scan` with heap fetches, MySQL lacking `Using index`), add the selected
columns to the index:
```sql
-- Postgres 11+ / SQL Server
CREATE INDEX ix_orders_cust_date ON orders (customer_id, created_at) INCLUDE (status, total);
-- MySQL: no INCLUDE; append columns to the key
CREATE INDEX ix_orders_cust_date ON orders (customer_id, created_at, status, total);
```
Key column order: equality columns first, then the range/sort column. Postgres
`Index Only Scan` still visits the heap unless the visibility map is current (shown as
`Heap Fetches`); vacuum keeps it low. Every index slows writes; drop the old index the
new one supersedes.

## Verify
- [ ] You captured the actual plan with realistic parameters, warm and cold.
- [ ] You can name the node where most time is spent and its estimate vs actual rows.
- [ ] Predicates on indexed columns are sargable and type-matched.
- [ ] Join choices are consistent with the actual row counts.
- [ ] After the fix, reads/buffers dropped, not just elapsed time on a warm cache.
