---
id: computing-software.database-administration.postgresql.reindex-concurrently-and-index-bloat
name: reindex-concurrently-and-index-bloat
category: computing-software
field: database-administration
product: postgresql
tags: [database-administration, postgresql, postgres, reindex-concurrently, index-bloat, pgstattuple, invalid-index, btree-deduplication, routine-reindexing]
level: advanced
status: verified
description: "Measure PostgreSQL B-tree index bloat with pgstattuple, rebuild bloated indexes online with REINDEX CONCURRENTLY, and clean up invalid indexes left by failed builds."
sources:
  - https://www.postgresql.org/docs/current/routine-reindex.html
  - https://www.postgresql.org/docs/current/sql-reindex.html
  - https://www.postgresql.org/docs/current/pgstattuple.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# REINDEX CONCURRENTLY and index bloat

**Goal:** indexes that grew far beyond their data are rebuilt online, and you
rebuild only those that need it.

## Measure
```sql
CREATE EXTENSION pgstattuple;
SELECT avg_leaf_density, leaf_fragmentation, pg_size_pretty(index_size)
FROM pgstatindex('orders_customer_id_idx');
```
A freshly built B-tree has leaf density ~90% (fillfactor; measured 90.15%). After deleting 90% of 300,000 rows and a VACUUM it was 13.7% at the same 4280 kB size, and 89.29% / 656 kB after `REINDEX`. Density well under
~50% on a large index = worth rebuilding. `pgstatindex` reads the whole index
(I/O), so run it on the suspect indexes one at a time rather than across the whole database.

Common causes: mass DELETEs/UPDATEs of indexed columns, random-key inserts
(UUIDv4) with page splits, long-running transactions that blocked cleanup. PG13+
B-tree deduplication and PG14 bottom-up deletion reduce bloat considerably.

## Rebuild online (PG12+)
```sql
REINDEX INDEX CONCURRENTLY orders_customer_id_idx;
REINDEX TABLE CONCURRENTLY orders;            -- all indexes on the table
```
Builds a new index alongside (`..._ccnew`), swaps, drops the old one (`..._ccold`). Takes only
`SHARE UPDATE EXCLUSIVE` on the table and indexes (checked in `pg_locks`; reads and writes continue). Needs disk for a second
copy, cannot run inside a transaction block, and waits for older transactions at
each phase. Set `maintenance_work_mem` high in the session for speed.

## Failed builds leave invalid indexes
An interrupted `CREATE INDEX CONCURRENTLY` / `REINDEX CONCURRENTLY` leaves an
INVALID index that is still maintained on writes (`indisready` stays true) but never used. After cancelling a `REINDEX INDEX CONCURRENTLY` that was waiting on an older transaction, 17.6 left `rb_customer_id_idx_ccold` invalid. Per the docs a leftover suffixed `_ccnew` is the half-built copy (drop it and rerun), one suffixed `_ccold` is the original that could not be dropped (just drop it):
```sql
SELECT indexrelid::regclass, indrelid::regclass FROM pg_index WHERE NOT indisvalid;
DROP INDEX CONCURRENTLY orders_customer_id_idx_ccold;   -- or ..._ccnew
```
A concurrent rebuild also waits for older transactions that hold a lock on the table, not for every old snapshot.

## Gotchas
- Plain `REINDEX` locks out writes (and reads using that index) for the duration.
- Rebuilding indexes on a primary generates WAL ~ index size: replicas lag; pace large jobs.
- Rebuilding is pointless if the bloat cause continues; fix the workload or schedule periodic rebuilds.
- After glibc/ICU changes, reindexing is about correctness, not bloat (see collation skill).

## Verify
`pgstatindex` shows density back near 90% and `pg_relation_size` dropped; no rows
in the invalid-index query.

## Checked
PostgreSQL 17.6, 300,000-row table: `pgstatindex` density and size figures as quoted; `REINDEX INDEX CONCURRENTLY` inside a transaction block fails with `REINDEX CONCURRENTLY cannot run inside a transaction block`; with a concurrent session holding AccessShareLock on the table the reindex waited and `pg_locks` showed ShareUpdateExclusiveLock on the table and the index, with `_ccold` created; cancelling it left an invalid-but-ready `_ccold` index; the invalid-index query and `DROP INDEX CONCURRENTLY` work. Docs (sql-reindex) for the `_ccnew`/`_ccold` recovery advice. PG13 release notes (B-tree duplicates stored more efficiently) and PG14 release notes (index additions remove expired entries to prevent page splits) for the bloat-reduction remark.
