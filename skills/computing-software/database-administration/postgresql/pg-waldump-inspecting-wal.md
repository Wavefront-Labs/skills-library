---
id: computing-software.database-administration.postgresql.pg-waldump-inspecting-wal
name: pg-waldump-inspecting-wal
category: computing-software
field: database-administration
product: postgresql
tags: [database-administration, postgresql, postgres, wal-configuration, pg-waldump, wal-analysis, wal-volume, recovery-target-lsn, pg-walinspect, forensics]
level: advanced
status: verified
description: "Read PostgreSQL WAL with pg_waldump and pg_walinspect to find what generates WAL volume, or the LSN/xid of a destructive statement for point-in-time recovery."
sources:
  - https://www.postgresql.org/docs/current/pgwaldump.html
  - https://www.postgresql.org/docs/current/pgwalinspect.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Inspecting WAL with pg_waldump

**Goal:** answer "what is writing all this WAL?" and "exactly where did the bad
DELETE happen?" from the WAL itself.

## Volume breakdown by resource manager
```bash
pg_waldump --stats=record -p <datadir>/pg_wal 000000010000002A00000010 000000010000002A0000001F
```
Output ranks record types by count and bytes, with full-page-image share. Heavy
`Heap/HOT_UPDATE` vs `Btree/INSERT_LEAF` vs `FPI` tells you whether the cost is
updates, index maintenance or checkpoint frequency.

## Find a transaction for PITR
```bash
pg_waldump -p /archive --start=2A/10000000 --end=2A/20000000 | grep -E 'COMMIT 2026-10-16 14:0[23]'
pg_waldump -p /archive -s 2A/10000000 -x 912345      # all records of xid 912345
pg_waldump ... -r Heap -R 1663/16384/24576            # records touching one relation (tblspc/db/relfilenode)
```
Map a table to its relfilenode: `SELECT pg_relation_filenode('invoices');`.
Then use `recovery_target_xid = '912345'` with `recovery_target_inclusive = false`,
or the LSN of the COMMIT record as `recovery_target_lsn`.

## From SQL (PG15+)
```sql
CREATE EXTENSION pg_walinspect;
SELECT * FROM pg_get_wal_stats('2A/10000000', '2A/20000000', per_record => false);
SELECT start_lsn, xid, resource_manager, record_type, description
FROM pg_get_wal_records_info('2A/10000000', '2A/10100000') WHERE xid = 912345;
```
Needs superuser or `pg_read_server_files`.

## Gotchas
- pg_waldump must match the server's major version (a 16.15 pg_waldump failed with `could not find a valid record` on 18.6 WAL that the 18.6 binary read fine).
- Segments must be contiguous; the timeline is in the file name (first 8 hex digits) and only that timeline is displayed (docs).
- Reading a segment that is still being written yields `invalid record length`
  at the end: that is just the current insert position.
- WAL contains row data: treat copies as sensitive.

## Verify
`SELECT pg_current_wal_lsn(), pg_walfile_name(pg_current_wal_lsn());` gives a
known position to test a pg_waldump range against.

## Checked
- PostgreSQL 18.6 scratch cluster (a table `inv` with 1000 inserts, 499 updates, 100 deletes): `pg_waldump --stats=record -p <datadir>/pg_wal <startseg> <endseg>` printed the per-record table (`XLOG/FPI_FOR_HINT`, `Heap2/PRUNE_VACUUM_SCAN`, `Transaction/COMMIT` ...) with FPI size and percentages; `pg_waldump -p <dir> -s 0/20000028 | grep COMMIT` gave lines like `desc: COMMIT 2026-10-22 19:46:25.516882 E. Australia Standard Time` (the skill's date/time grep pattern shape fits); `-r Heap -R 1663/5/16423` returned `INSERT+INIT ... blkref #0: rel 1663/5/16423` with `pg_relation_filenode('inv')` = 16423, database oid 5, tablespace oid 1663; `-x 794 -s ...` returned only xid 794's records; reading to the live end printed `invalid record length at 0/2069A1C8: expected at least 24, got 0`. `CREATE EXTENSION pg_walinspect`, `pg_get_wal_stats(start, end, per_record => false)` and `pg_get_wal_records_info(...)` filtered by `resource_manager = 'Transaction'` ran; `SELECT pg_current_wal_lsn(), pg_walfile_name(...)` gave `0/2068C8A0`, `000000010000000000000020`. A 16.15 pg_waldump on the 18.6 segment failed; the 18.6 one read it.
- Docs: pg_walinspect page (default access: superusers and `pg_read_server_files`, `per_record` default false), pg_waldump page (only the specified timeline; `-r`, `-R`, `-B`; `.partial` files not readable), PG15 notes add pg_walinspect, recovery-target settings include `recovery_target_xid` and `recovery_target_inclusive`.
