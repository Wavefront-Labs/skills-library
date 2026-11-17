---
id: computing-software.database-administration.postgresql.amcheck-corruption-detection
name: amcheck-corruption-detection
category: computing-software
field: database-administration
product: postgresql
tags: [database-administration, postgresql, postgres-extensions, amcheck, pg-amcheck, corruption, data-checksums, index-corruption, collation-version]
level: advanced
status: verified
description: "Detect B-tree and heap corruption with amcheck and pg_amcheck, interpret results, and respond (reindex, restore) after storage faults or glibc collation changes."
sources:
  - https://www.postgresql.org/docs/current/amcheck.html
  - https://www.postgresql.org/docs/current/app-pgamcheck.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Detecting corruption with amcheck / pg_amcheck

## Install
```sql
CREATE EXTENSION amcheck;     -- in each database to check
```
`pg_amcheck` (PG14+) is the command-line driver; it installs nothing itself but needs the
extension in every target database (`--install-missing` creates it).

## Run
```bash
pg_amcheck --all -j 4 --heapallindexed --progress            # all databases
pg_amcheck -d app -t 'public.orders*' --rootdescend           # specific tables
pg_amcheck -d app --index='*_pkey'                             # indexes only (there is no --skip-heap option)
```
SQL equivalents:
```sql
SELECT bt_index_check('orders_pkey'::regclass, heapallindexed => true);        -- AccessShareLock, OK on primary
SELECT bt_index_parent_check('orders_pkey'::regclass, heapallindexed => true); -- ShareLock: blocks writes; stronger
SELECT * FROM verify_heapam('orders', check_toast => true);                   -- heap/TOAST, PG14+
```
- `heapallindexed` verifies every heap tuple has an index entry (catches missing entries;
  costs a full heap scan).
- `bt_index_parent_check` / `--parent-check` checks cross-level invariants but blocks writes;
  run it on a restored copy or standby-promoted clone.
- PG18 adds `gin_index_check` (absent from the 17 amcheck docs, present in the current ones and the 18 release notes).
- `bt_index_parent_check` cannot be used on a hot standby (docs); `bt_index_check` can. The amcheck docs state `bt_index_check` takes `AccessShareLock` on the index and its table.

## Reading results
No output / empty set = no corruption found. Typical findings:
- `item order invariant violated for index "x"` - keys out of order. Most common cause:
  **collation change** after an OS/glibc upgrade (e.g. glibc 2.28) on text indexes. Fix:
  `REINDEX INDEX CONCURRENTLY x;` then `ALTER DATABASE ... REFRESH COLLATION VERSION`.
- `heap tuple ... lacks matching index tuple` - index missing entries; REINDEX.
- `verify_heapam` rows (blkno, offnum, attnum, msg) like `xmin 4294967040 precedes oldest valid transaction ID 0:730` (produced by a bogus xmin written into a heap page) or `xmin ... precedes relation freeze threshold`
  or invalid TOAST pointers - **heap** damage; REINDEX will not help. Restore the affected
  table from backup/PITR, or salvage readable rows to a new table.

## When to run
- After storage incidents, unclean failovers, filesystem errors, or `checksum_failures` > 0
  in `pg_stat_database`.
- After OS upgrades that change glibc/ICU (text indexes).
- Routinely (weekly) on a restored backup copy as part of restore testing.

## Gotchas
- amcheck reads every page: heavy I/O; throttle with `-j` and run off-peak.
- Data checksums (`initdb -k`) catch torn/bit-flipped pages at read time; amcheck catches
  logical inconsistencies checksums miss. Use both.
- Corruption on the primary is usually replicated to physical standbys only if it came
  through WAL; storage-level corruption is often local, so check the standby too.

## Verify
`pg_amcheck --all` exits 0 with no messages; after a REINDEX, re-run on the affected index.

## Checked
Run on PostgreSQL 17.6 (Windows build, data checksums off) with real damage: a 200-row table, then with the server stopped a bogus xmin was written into a heap tuple and two index items were swapped in the primary-key btree. Clean state: `bt_index_check` and `bt_index_parent_check` with `heapallindexed => true` return one empty row, `verify_heapam(..., check_toast => true)` returns no rows, `pg_amcheck` exits 0 with no output. Damaged state: all three index checks raise `item order invariant violated for index "orders_pkey"` (the `DETAIL` names both index tids and heap tids); `verify_heapam` reports `xmin 4294967040 precedes oldest valid transaction ID 0:730` at block 0 offset 1; `pg_amcheck --heapallindexed` printed both findings and exited 2, while a check limited to another table (`-t 'public.good*' --parent-check --rootdescend`) exited 0; ordinary `SELECT count(*)` still worked on the damaged table (no checksums, so nothing noticed); `REINDEX INDEX` fixed the index but the heap finding remained. `pg_amcheck` against a database without the extension warns `amcheck is not installed` and errors with `no relations to check`; `--install-missing` is accepted; the `--help` output has `--heapallindexed`, `--parent-check`, `--rootdescend`, `--progress`, `--jobs`, `--index`, `--table`, `--exclude-index`, `--on-error-stop` and `--startblock` but no `--skip-heap`. `checksum_failures` in `pg_stat_database` is NULL when checksums are off, and `ALTER DATABASE ... REFRESH COLLATION VERSION` runs. Fetched: the current amcheck docs (lock mode, standby restriction, `gin_index_check`) and the 17 docs (no `gin_index_check`). Not run: the `lacks matching index tuple` message, TOAST corruption, a real glibc/ICU collation change, `REINDEX INDEX CONCURRENTLY`, the lock modes observed directly (amcheck releases them when the function returns), parallel `-j` on large data, Linux (file layout and checks are the same; the corruption script is Windows-path specific).
