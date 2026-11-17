---
id: computing-software.database-administration.query-optimisation.indexing-for-joins
name: indexing-for-joins
category: computing-software
field: database-administration
product: query-optimisation
tags: [database-administration, query-optimisation, join-indexing, nested-loop-join, hash-join, merge-join, indexing]
level: practitioner
status: draft
description: "Index for each join algorithm: nested loops need an index on the inner join column, hash joins need none on keys but benefit from filter indexes, merge joins want sorted input."
sources:
  - https://use-the-index-luke.com/sql/join
  - https://www.postgresql.org/docs/current/planner-optimizer.html
  - https://learn.microsoft.com/en-us/sql/relational-databases/performance/joins
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Indexing for joins

## Nested loops
For each outer row, look up matching inner rows. Fast only when the inner lookup uses an index on the **join column** of the inner table and the outer side is small.
```sql
SELECT ... FROM orders o JOIN order_items i ON i.order_id = o.id WHERE o.customer_id = 42;
-- needs: orders(customer_id) for the outer filter, order_items(order_id) for the inner lookup
```
Foreign key columns are not indexed automatically in PostgreSQL, SQL Server or Oracle (MySQL InnoDB creates them): unindexed FKs are the most common nested-loop disaster (a seq scan per outer row) and also slow cascading deletes.

## Hash join
Builds a hash table on the smaller input (after filters), probes with the other. Join-column indexes do not help the join itself; indexes on the **filter predicates** of each side reduce input sizes. Needs memory: hash spills when the build side exceeds `work_mem` / memory grant. Equality joins only.

## Merge join
Both inputs sorted on the join key, then merged. Indexes that deliver sorted order on the join columns let the optimiser skip sorts; good for large, already-ordered inputs (e.g. both clustered on the key).

## Composite indexes for join + filter
Index the inner table with equality filter columns plus the join column:
```sql
-- join on customer_id, filter on status
CREATE INDEX ON orders (customer_id, status);         -- serves "orders of customer X with status Y" lookups
```
Add included columns to make the inner lookup index-only: `CREATE INDEX ON order_items (order_id) INCLUDE (sku, qty);`.

## Join order and estimates
The optimiser picks the outer/inner sides from cardinality estimates. A misestimate (expects 1 outer row, gets 100k) turns a nested loop into the slow path even with good indexes. Fix statistics first; the right index is useless with the wrong plan.

## MySQL specifics
MySQL 8.0.18+ has hash joins for equi-joins without usable indexes; before that, Block Nested Loop. EXPLAIN `type: ref/eq_ref` on the inner table means index lookups; `ALL` with "Using join buffer (hash join)" means no index used.

## Verify
`EXPLAIN ANALYZE`: inner side of nested loops shows `Index Scan` / `Index Only Scan` with low per-loop time; no `Seq Scan` inside a loop with high `loops=` count.
