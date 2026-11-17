---
id: computing-software.database-administration.query-optimisation.combining-single-column-indexes-vs-composite
name: combining-single-column-indexes-vs-composite
category: computing-software
field: database-administration
product: query-optimisation
tags: [database-administration, query-optimisation, index-combine, bitmap-index-scan, index-merge, composite-index, indexing]
level: practitioner
status: draft
description: "Decide between several single-column indexes combined at runtime (bitmap AND/OR, MySQL index merge) and one composite index, with plan signs and trade-offs."
sources:
  - https://www.postgresql.org/docs/current/indexes-bitmap-scans.html
  - https://dev.mysql.com/doc/refman/8.4/en/index-merge-optimization.html
  - https://use-the-index-luke.com/sql/where-clause/searching-for-ranges/index-combine-performance
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Combining single-column indexes vs one composite index

## What the engines can do
- **PostgreSQL**: `BitmapAnd` / `BitmapOr` of several bitmap index scans, then one heap pass.
- **MySQL**: `index_merge` (intersection, union, sort-union); EXPLAIN `type: index_merge`, `Using intersect(...)`.
- **Oracle**: bitmap conversion of B-tree rowids (`BITMAP AND`), native bitmap indexes in warehouses.
- **SQL Server**: index intersection exists but is rarely chosen; it prefers one index plus lookups.

```text
Bitmap Heap Scan on orders
  Recheck Cond: ((status = 'open') AND (region = 'EU'))
  ->  BitmapAnd
        ->  Bitmap Index Scan on orders_status_idx
        ->  Bitmap Index Scan on orders_region_idx
```

## Composite wins for AND on hot queries
`WHERE status = 'open' AND region = 'EU'`: an index on `(status, region)` (or `(region, status)`) goes straight to matching entries. Combining two single-column indexes reads all `open` entries and all `EU` entries, builds bitmaps and intersects: more I/O and CPU, and no ordering for `ORDER BY ... LIMIT`.

Rule of thumb (Winand): one well-designed composite index beats combining indexes for a known query; combining is a fallback for ad-hoc filter combinations.

## When single-column indexes are the right design
- Ad-hoc search screens filtering on any subset of 6+ columns: you cannot build every composite.
- `OR` across columns: `WHERE email = ? OR phone = ?` needs separate indexes (BitmapOr / index_merge union) or a `UNION` rewrite.
- Data warehouse star queries with low-cardinality columns: bitmap indexes (Oracle) or columnstore.

## Signs you need a composite
- Frequent `BitmapAnd`/`index_merge intersect` on the same column pair in slow logs.
- `Recheck Cond` with `lossy` heap blocks (bitmap exceeded `work_mem`).
- Many rows from each single index but few after intersection.

## Cost of extra indexes
Every index slows writes and uses cache. After adding the composite, check whether a single-column index is now redundant (a composite `(a, b)` covers queries on `a` alone).

## Verify
Plan changes from `BitmapAnd` to a single `Index Scan` on the composite with lower buffers; then confirm with index usage stats (`pg_stat_user_indexes.idx_scan`) before dropping old indexes.
