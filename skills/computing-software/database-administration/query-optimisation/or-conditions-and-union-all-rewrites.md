---
id: computing-software.database-administration.query-optimisation.or-conditions-and-union-all-rewrites
name: or-conditions-and-union-all-rewrites
category: computing-software
field: database-administration
product: query-optimisation
tags: [database-administration, query-optimisation, or-to-union, or-conditions, union-all, query-rewrite, query-patterns]
level: practitioner
status: draft
description: "Speed up queries with OR across different columns or optional filters by rewriting to UNION ALL branches, OR-expansion, or IN lists, keeping each branch index-friendly."
sources:
  - https://use-the-index-luke.com/sql/where-clause/obfuscation/smart-logic
  - https://www.postgresql.org/docs/current/indexes-bitmap-scans.html
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/tgsql/query-transformations.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# OR conditions and UNION ALL rewrites

## The problem
```sql
SELECT * FROM customers WHERE email = :x OR phone = :x;
```
One index can serve only one of the columns. Engines may combine indexes (PostgreSQL BitmapOr, MySQL index_merge union, Oracle OR-expansion), but often they scan, especially when OR mixes with other predicates or joins.

## Rewrite to UNION ALL
```sql
SELECT * FROM customers WHERE email = :x
UNION ALL
SELECT * FROM customers WHERE phone = :x AND email IS DISTINCT FROM :x;   -- exclude rows already returned
```
Each branch uses its own index. The second predicate prevents duplicates without the cost of `UNION` (distinct). Use plain `UNION` when the exclusion predicate is complex and result sets are small.

## OR across joined tables
```sql
SELECT o.* FROM orders o JOIN customers c ON c.id = o.customer_id
WHERE o.ref = :r OR c.email = :e;      -- optimisers struggle: neither index alone can drive
```
Split into two queries driven from each table and union them.

## Same column: use IN
`status = 'a' OR status = 'b'` is the same as `status IN ('a','b')`; optimisers handle both well, but IN is clearer.

## Optional filters ("smart logic")
```sql
WHERE (:status IS NULL OR status = :status) AND (:region IS NULL OR region = :region)
```
A cached plan must work for every combination, so it typically scans. Build the SQL dynamically with only the present filters (with bind parameters), or use `OPTION (RECOMPILE)` (SQL Server) for such queries.

## Range ORs
`created_at < :a OR created_at > :b` on one column can use one index twice (two ranges); engines handle this as an index scan with two ranges or a BitmapOr.

## Verify
Plan for the rewrite shows index scans in both branches (`Append` of two `Index Scan`s in PostgreSQL); results equal the original query's results on test data including rows that match both conditions.
