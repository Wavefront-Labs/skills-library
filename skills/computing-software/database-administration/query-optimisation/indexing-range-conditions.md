---
id: computing-software.database-administration.query-optimisation.indexing-range-conditions
name: indexing-range-conditions
category: computing-software
field: database-administration
product: query-optimisation
tags: [database-administration, query-optimisation, composite-index, range-condition-index, index-column-order, between, access-predicate]
level: practitioner
status: draft
description: "Order composite index columns for queries mixing equality and range predicates: equality first, range last, and why a range on the leading column wastes the rest of the index."
sources:
  - https://use-the-index-luke.com/sql/where-clause/searching-for-ranges/greater-less-between-tuning-sql-access-filter-predicates
  - https://use-the-index-luke.com/sql/where-clause/the-equals-operator/concatenated-keys
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Indexing range conditions

## The rule: equality first, range last
```sql
SELECT * FROM orders
WHERE customer_id = :c AND created_at >= :from AND created_at < :to;
```
- Index `(customer_id, created_at)`: the database seeks to `customer_id = :c`, then walks only the
  date range within it. Every entry read is a match. Both columns are **access predicates**.
- Index `(created_at, customer_id)`: the database walks the whole date range for **all**
  customers and checks `customer_id` on each entry. `customer_id` becomes a **filter predicate**
  inside the index. With a wide range this reads far more index entries.

Columns after the first range column in an index can only filter, not narrow the scan (except
special techniques like skip scan / loose index scan in some engines).

## Several ranges
`WHERE price BETWEEN 10 AND 20 AND created_at > :d` can use only one range as an access path in
a B-tree. Put the **more selective** range column right after the equality columns; the other
becomes a filter (or consider separate indexes combined via bitmap/index merge, or a different
design such as a spatial/GiST index for two-dimensional ranges).

## LIKE and ranges
`LIKE 'abc%'` is a range on the prefix (`>= 'abc' AND < 'abd'`), so the same rule applies:
put it after equality columns. `LIKE '%abc'` cannot use a B-tree range at all.

## IN lists
`customer_id IN (1,2,3)` is a set of equality lookups: still "equality" for column ordering, and
most engines perform one range scan per value.

## Seeing it in plans
- PostgreSQL: `Index Cond` lists access predicates; conditions under `Filter` were applied after reading.
- Oracle: `access(...)` vs `filter(...)` in DBMS_XPLAN predicate information.
- SQL Server: `Seek Predicates` vs `Predicate` on the Index Seek operator.
- MySQL: `key_len` in EXPLAIN shows how many index bytes (columns) were used for access.

## Verify
Compare `EXPLAIN (ANALYZE, BUFFERS)` (or logical reads) for both column orders on realistic data:
the equality-first index reads close to the number of returned rows.
