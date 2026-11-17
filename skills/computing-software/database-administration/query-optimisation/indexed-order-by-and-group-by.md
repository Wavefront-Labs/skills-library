---
id: computing-software.database-administration.query-optimisation.indexed-order-by-and-group-by
name: indexed-order-by-and-group-by
category: computing-software
field: database-administration
product: query-optimisation
tags: [database-administration, query-optimisation, sql, execution-plan, indexed-order-by, pipelined-order-by, top-n-query, sort-avoidance, filesort, group-by-index, asc-desc-index]
level: advanced
status: draft
description: "Let indexes deliver rows already sorted so ORDER BY ... LIMIT and GROUP BY avoid sort steps: column order, mixed ASC/DESC, and how plans show it in each engine."
sources:
  - https://use-the-index-luke.com/sql/sorting-grouping/indexed-order-by
  - https://use-the-index-luke.com/sql/sorting-grouping/indexed-group-by
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Indexed ORDER BY and GROUP BY

**Goal:** "latest 20 orders for customer X" reads 20 index entries and stops,
instead of sorting every matching row.

## The rule
An index can return rows in the ORDER BY order if:
1. equality-filtered columns come first in the index, then
2. the ORDER BY columns follow in the same order (and compatible directions).
```sql
CREATE INDEX ON orders (customer_id, created_at);
SELECT * FROM orders WHERE customer_id = 42 ORDER BY created_at DESC LIMIT 20;
```
The engine walks the index backwards from the end of customer 42's range: a
**pipelined top-N**, cost proportional to 20, not to the customer's order count.

Breaks pipelining:
- a range predicate before the sort column (`WHERE customer_id IN (1,2,3)` or
  `created_at > ...` on a leading column then ordering by another);
- ORDER BY a column not next in the index, or an expression;
- mixed directions (`ORDER BY a ASC, b DESC`) unless the index is defined that
  way: `CREATE INDEX ON t (a ASC, b DESC)` (PostgreSQL, MySQL 8+, SQL Server, Oracle).

## How plans show it
| Engine | Sort avoided | Sort happening |
|---|---|---|
| PostgreSQL | `Limit -> Index Scan Backward` | `Sort` / `Incremental Sort` / `top-N heapsort` |
| MySQL | no `Using filesort` in Extra | `Using filesort` |
| SQL Server | no Sort operator; `Ordered = True` on the seek | `Sort` / `Top N Sort` |
| Oracle | `INDEX RANGE SCAN DESCENDING` + `COUNT STOPKEY` | `SORT ORDER BY STOPKEY` |
| SQLite | no `USE TEMP B-TREE FOR ORDER BY` | `USE TEMP B-TREE` |

## GROUP BY
An index on the grouping columns lets the engine group by streaming
(PostgreSQL `GroupAggregate` over an index scan, MySQL "Using index for
group-by" loose scan) instead of hashing/sorting everything. Hash aggregation is
often fine; streaming wins when combined with LIMIT or when memory is tight.

## Gotchas
- Pipelined top-N matters most with LIMIT; without LIMIT a full sort may be cheaper than random heap access.
- Planner may still prefer a selective filter index plus sort; compare with EXPLAIN ANALYZE.
- Collation affects text sort order: the index must use the query's collation.

## Verify
EXPLAIN shows no sort node and rows read ≈ LIMIT; timing flat as the customer's history grows.
