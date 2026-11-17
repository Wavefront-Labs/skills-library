---
id: computing-software.database-administration.postgresql.visibility-map-and-index-only-scans
name: visibility-map-and-index-only-scans
category: computing-software
field: database-administration
product: postgresql
tags: [database-administration, postgresql, postgres, visibility-map, index-only-scan, heap-fetches, vacuum, all-visible, pg-visibility]
level: practitioner
status: verified
description: "Keep PostgreSQL index-only scans fast by keeping the visibility map current: read Heap Fetches, check relallvisible, and tune vacuum for insert-heavy tables."
sources:
  - https://www.postgresql.org/docs/current/storage-vm.html
  - https://www.postgresql.org/docs/current/indexes-index-only-scans.html
  - https://www.postgresql.org/docs/current/pgvisibility.html
  - https://www.postgresql.org/docs/current/routine-vacuuming.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# The visibility map and index-only scan freshness

Each heap page has two bits in the visibility map (`<relfilenode>_vm`): **all-visible** (every tuple visible to every transaction) and **all-frozen**. An index-only scan skips the heap only for all-visible pages; for others it must fetch the heap page to check visibility. VACUUM sets the bits; any INSERT/UPDATE/DELETE on a page clears them.

## Spot the problem
```sql
EXPLAIN (ANALYZE, BUFFERS) SELECT order_id FROM orders WHERE customer_id = 42;
--  Index Only Scan using orders_customer_id_order_id_idx on orders
--    Heap Fetches: 18234      <- should be near 0
```
```sql
SELECT relname, relpages, relallvisible, round(100.0*relallvisible/nullif(relpages,0),1) AS pct_all_visible
FROM pg_class WHERE relname = 'orders';
```
On the test table `relallvisible` was 0 before the first VACUUM and the planner chose a Bitmap Heap Scan; after `VACUUM` it equalled `relpages` and the plan became `Index Only Scan ... Heap Fetches: 0`. Low `pct_all_visible` on a large table = index-only scans degrade to index scans plus random heap reads.

## Exact per-page view
```sql
CREATE EXTENSION pg_visibility;
SELECT all_visible, all_frozen, count(*) FROM pg_visibility_map('orders') GROUP BY 1, 2;
SELECT * FROM pg_check_visible('orders');   -- returns rows only if the VM is corrupt (should be empty)
```

## Fix: vacuum more often on the hot table
Insert-only/append tables were historically never vacuumed (no dead tuples). PG13+ triggers vacuum on inserts too:
```sql
ALTER TABLE orders SET (autovacuum_vacuum_insert_scale_factor = 0.01, autovacuum_vacuum_insert_threshold = 10000);
ALTER TABLE orders SET (autovacuum_vacuum_scale_factor = 0.02);
VACUUM (VERBOSE) orders;   -- one-off; reports pages set all-visible
```
For bulk-loaded tables, `VACUUM (FREEZE, ANALYZE)` right after the load sets all-visible and all-frozen in one pass, and `COPY ... FREEZE` into a table created/truncated in the same transaction sets them on write.

## Design implications
- Index-only scans need all queried columns in the index (`INCLUDE (...)` for non-key payload).
- Heavily updated tables will never be mostly all-visible; index-only scans there are not a reliable plan.
- HOT updates still clear the page's all-visible bit.

## Gotchas
- `relallvisible` is only refreshed by VACUUM (and ANALYZE); it can be stale. Updating 5 rows cleared 5 pages' bits and the next index-only scan reported `Heap Fetches: 5`.
- The planner costs index-only scans using `relallvisible`; a stale low value makes it avoid them even after the VM is good. Run ANALYZE after a big vacuum.

## Checked
PostgreSQL 17.6, 200,000-row table: plans and `pg_class.relallvisible` as described; `pg_visibility_map` showed 2,470 pages all-visible and not all-frozen after a plain VACUUM, then 5 pages not all-visible after updating 5 rows (all were HOT updates: `n_tup_hot_upd` = 5); `pg_check_visible` returned 0 rows; the three `ALTER TABLE ... SET (autovacuum_vacuum_insert_*)` reloptions are accepted; a table loaded by `INSERT` showed all-visible = f, `VACUUM (FREEZE, ANALYZE)` made it all-visible and all-frozen, and `COPY ... WITH (FREEZE)` into a table created in the same transaction was all-visible and all-frozen immediately. Docs (sql-copy): FREEZE conditions.
