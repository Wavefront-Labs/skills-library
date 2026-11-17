---
id: computing-software.database-administration.postgresql.bitmap-scans-combining-indexes
name: bitmap-scans-combining-indexes
category: computing-software
field: database-administration
product: postgresql
tags: [database-administration, postgresql, postgres, bitmap-scan, bitmap-heap-scan, bitmapand, bitmapor, lossy-blocks, work-mem, explain]
level: practitioner
status: verified
description: "Read PostgreSQL Bitmap Index/Heap Scan plans: BitmapAnd/BitmapOr combining indexes, lossy blocks and Recheck, and when a composite index is better."
sources:
  - https://www.postgresql.org/docs/current/indexes-bitmap-scans.html
  - https://www.postgresql.org/docs/current/using-explain.html
  - https://www.postgresql.org/docs/current/runtime-config-resource.html#GUC-WORK-MEM
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Combining multiple indexes with bitmap scans

A bitmap scan reads matching TIDs from one or more indexes into an in-memory bitmap, combines them, then visits heap pages in physical order. Good for "too many rows for an index scan, too few for a seq scan", and the only way to use several single-column indexes in one query.

## Reading the plan
```
Bitmap Heap Scan on orders  (actual rows=4210 loops=1)
  Recheck Cond: ((status = 'open') AND (region_id = 7))
  Heap Blocks: exact=3120 lossy=0
  ->  BitmapAnd
        ->  Bitmap Index Scan on orders_status_idx   (actual rows=150000)
        ->  Bitmap Index Scan on orders_region_idx   (actual rows=38000)
```
- `BitmapAnd` / `BitmapOr`: indexes combined for AND / OR (OR across columns is a key use).
- `Heap Blocks: lossy=N`: the bitmap exceeded `work_mem`, degraded to page-level bits; every row on those pages is rechecked (`Rows Removed by Index Recheck` appears and grows; it is omitted when zero).
- `Recheck Cond` is always shown; it only costs when blocks are lossy (or for lossy index types like GIN/BRIN).

## Tuning
- Lossy blocks: raise `work_mem` for that session/role: `SET work_mem = '64MB';` and compare.
- BitmapAnd where both inputs return many rows: a composite index `(status, region_id)` lets one index scan return only the intersection. Choose composite when the combination is a frequent query; keep single-column indexes when combinations vary.
- `effective_io_concurrency` (and `maintenance_io_concurrency`) controls prefetching for bitmap heap scans on SSD/RAID; the default of `effective_io_concurrency` is 1 up to PG17 (0 where prefetch is unsupported, e.g. Windows builds) and 16 from PG18 (`maintenance_io_concurrency` was 10, now 16). Tune by measuring.

## Why not always a bitmap
- Loses index order: an `ORDER BY ... LIMIT` query can't stop early, so the planner prefers a plain index scan there.
- There is no index-only bitmap scan: the heap is visited for every matching page, so an index-only scan on a covering index can be cheaper.

## Gotchas
- A `BitmapOr` over 20 values (`IN` list on different indexes) may be slower than one seq scan; check `actual time`.
- Statistics misestimates show up as a bitmap scan that returns 30% of the table; fix stats rather than forcing plans with `enable_bitmapscan = off` (test only).

## Checked
PostgreSQL 17.6, 300,000 rows with single-column indexes on `status` and `region_id`: `BitmapAnd` for AND, `BitmapOr` for OR on different columns, `Recheck Cond` always printed, `Heap Blocks: exact=557 lossy=3093` with `Rows Removed by Index Recheck: 190882` at `work_mem = '64kB'` (and no recheck line when exact), one `Bitmap Index Scan` on the composite index, and `ORDER BY id LIMIT 10` over an OR gave Gather Merge/top-N sort over a parallel bitmap scan (the bitmap loses index order). Defaults checked in the PG17 and PG18 docs and the PG18 release notes.
