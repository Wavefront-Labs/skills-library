---
id: computing-software.database-administration.query-optimisation.planner-cost-model
name: planner-cost-model
category: computing-software
field: database-administration
product: query-optimisation
tags: [database-administration, query-optimisation, planner-cost-model, cost-based-optimizer, random-page-cost, execution-plans, cardinality]
level: practitioner
status: draft
description: "Understand how cost-based optimisers price plans (page and CPU cost units, cardinality, selectivity) and which cost settings to tune, such as random_page_cost on SSDs."
sources:
  - https://www.postgresql.org/docs/current/runtime-config-query.html#RUNTIME-CONFIG-QUERY-CONSTANTS
  - https://www.postgresql.org/docs/current/planner-stats-details.html
  - https://dev.mysql.com/doc/refman/8.4/en/cost-model.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Cost units and how the planner chooses a plan

## The model
A cost-based optimiser enumerates candidate plans (scan types, join orders, join methods) and picks the lowest **estimated** cost. Cost = I/O + CPU, computed from:
- **Cardinality estimates** (rows per step) from statistics: histograms, distinct counts, MCVs, null fraction.
- **Cost constants** per unit of work.

PostgreSQL constants (arbitrary units, sequential page = 1.0):
| Setting | Default | Meaning |
|---|---|---|
| `seq_page_cost` | 1.0 | read a page sequentially |
| `random_page_cost` | 4.0 | read a page randomly |
| `cpu_tuple_cost` | 0.01 | process a row |
| `cpu_index_tuple_cost` | 0.005 | process an index entry |
| `cpu_operator_cost` | 0.0025 | evaluate an operator/function |
| `effective_cache_size` | 4GB | how much data is likely cached (affects index scan costing) |

Plan line `cost=0.43..8.45 rows=1 width=64`: startup cost..total cost, estimated rows, average row bytes.

## Tuning that is usually right
- SSD/NVMe or fully cached data: `random_page_cost = 1.1` to 1.5. Leaving 4.0 makes the planner prefer sequential scans over index scans too often.
- `effective_cache_size` ≈ 50-75% of RAM (it allocates nothing; it is a hint).
- Change at database/role level first (`ALTER DATABASE app SET random_page_cost = 1.1`) and verify plans.

## Most bad plans are estimate problems, not cost-constant problems
If `rows=10` but actual is 100,000, no constant will fix it. Look for: stale statistics, correlated predicates, functions on columns, parameter sniffing/generic plans, skewed data, join cardinality errors. Fix with ANALYZE, extended statistics, rewriting predicates, or better indexes.

## Other engines
- MySQL 8: cost model tables `mysql.server_cost` and `mysql.engine_cost` (`io_block_read_cost`, `memory_block_read_cost`); `EXPLAIN FORMAT=JSON` shows `cost_info`. Rarely changed.
- SQL Server: costs are internal units (historically "seconds on a 1990s machine"); you influence plans via statistics, indexes, compatibility level and hints, not constants.
- Oracle: system statistics (`DBMS_STATS.GATHER_SYSTEM_STATS`) and `optimizer_index_cost_adj` (legacy; avoid).

## Experimenting safely
```sql
BEGIN; SET LOCAL enable_seqscan = off; EXPLAIN ANALYZE ...; ROLLBACK;
```
`enable_*` switches add a huge cost penalty to a method, revealing the alternative plan's real performance. Never leave them set globally.

## Verify
After changing `random_page_cost`, compare plans and actual times for a set of representative queries; keep the change only if the set improves overall.
