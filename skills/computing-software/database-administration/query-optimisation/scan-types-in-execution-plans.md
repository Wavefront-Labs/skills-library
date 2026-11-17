---
id: computing-software.database-administration.query-optimisation.scan-types-in-execution-plans
name: scan-types-in-execution-plans
category: computing-software
field: database-administration
product: query-optimisation
tags: [database-administration, query-optimisation, execution-plan, explain-analyze, scan-types, seq-scan, index-only-scan, bitmap-heap-scan, key-lookup]
level: practitioner
status: draft
description: "Recognise table access operations across engines (full scan, index seek/range scan, index-only, bitmap heap, key lookup) and when each is the right choice."
sources:
  - https://use-the-index-luke.com/sql/explain-plan
  - https://www.postgresql.org/docs/current/using-explain.html
  - https://learn.microsoft.com/en-us/sql/relational-databases/showplan-logical-and-physical-operators-reference
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Scan types in execution plans

## Names across engines
| Access | PostgreSQL | SQL Server | Oracle | MySQL (type / tree) |
|---|---|---|---|---|
| read whole table | Seq Scan | Table Scan / Clustered Index Scan | TABLE ACCESS FULL | `ALL` / Table scan |
| index range / point lookup + fetch row | Index Scan | Index Seek + Key Lookup (RID Lookup on heaps) | INDEX RANGE/UNIQUE SCAN + TABLE ACCESS BY INDEX ROWID | `ref`/`range`/`eq_ref` |
| answer from index only | Index Only Scan | Index Seek (covering) | INDEX RANGE SCAN only | `Using index` |
| collect row ids, then read heap in physical order | Bitmap Index Scan + Bitmap Heap Scan | (n/a; batch mode) | BITMAP AND/OR + BY INDEX ROWID BATCHED | Index merge |
| read whole index in order | Index (Only) Scan without Index Cond | Index Scan | INDEX FULL SCAN / FAST FULL SCAN | `index` |

## When each is right
- **Full scan** is correct when a large fraction of rows is needed (rule of thumb: more than
  ~5-20%, depends on row width and storage). Sequential I/O beats random lookups. A full scan
  on a selective filter is the problem case.
- **Index scan + fetch**: few rows. Cost grows with matches times random heap/clustered reads;
  this is where the **clustering factor** matters.
- **Index-only / covering**: all needed columns in the index (`INCLUDE` columns). PostgreSQL
  additionally needs the visibility map to be current (`Heap Fetches` in EXPLAIN ANALYZE shows
  how often it had to check the table; vacuum keeps it low).
- **Bitmap heap scan** (PostgreSQL): medium selectivity, or combining several indexes with
  AND/OR; `Recheck Cond` and `lossy` blocks appear when `work_mem` is too small for an exact bitmap.
- **Key Lookup** (SQL Server) per row: fine for dozens, terrible for hundreds of thousands; add
  columns to the index `INCLUDE` list or accept a scan.

## Reading the numbers (PostgreSQL)
```
Index Scan using orders_customer_idx on orders (cost=0.43..812.11 rows=210 width=64)
  (actual time=0.03..1.92 rows=198 loops=1)
  Index Cond: (customer_id = 42)
  Filter: (status = 'open')
  Rows Removed by Filter: 1402
  Buffers: shared hit=1450 read=12
```
`Index Cond` is the access predicate (narrows the index range); `Filter` + `Rows Removed by Filter`
shows rows read and thrown away: a composite index `(customer_id, status)` would avoid that.

## Verify
For each slow query: the access type matches the expected selectivity (EXPLAIN ANALYZE actual
rows vs table size), and after an index change the plan uses the new access path with fewer
buffers/logical reads.
