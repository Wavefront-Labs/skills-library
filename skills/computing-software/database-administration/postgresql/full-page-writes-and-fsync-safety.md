---
id: computing-software.database-administration.postgresql.full-page-writes-and-fsync-safety
name: full-page-writes-and-fsync-safety
category: computing-software
field: database-administration
product: postgresql
tags: [database-administration, postgresql, postgres, wal-configuration, postgres-checkpoints, full-page-writes, fsync-safety, fsync, torn-pages, write-cache, pg-test-fsync, durability]
level: advanced
status: docs-checked
description: "Keep PostgreSQL crash-safe: why fsync and full_page_writes must stay on, how to check storage honours flushes with pg_test_fsync, and what 'fsyncgate' changed."
sources:
  - https://www.postgresql.org/docs/current/wal-reliability.html
  - https://www.postgresql.org/docs/current/pgtestfsync.html
  - https://wiki.postgresql.org/wiki/Fsync_Errors
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# full_page_writes and fsync safety

**Goal:** a power cut or kernel panic never corrupts the database.

## Settings that must stay on
- `fsync = on`: off means a crash can leave the cluster unrecoverably corrupt.
  The only legitimate use is a throwaway bulk load you would redo from scratch.
- `full_page_writes = on`: a page write in progress during an OS crash can be only partly
  completed, leaving a page with a mix of old and new data that the row-level WAL
  records cannot repair. The first modification of each page after a checkpoint therefore
  logs the whole page. Turning it off risks unrecoverable or silent corruption; the docs say to do so
  only in the same circumstances as `fsync = off`. `pg_rewind` also requires it to be on.
- `wal_sync_method`: the default is the first supported method in the documented list,
  except `fdatasync` on Linux and FreeBSD; the docs say it is not necessarily ideal, so use
  pg_test_fsync to compare methods on your system before changing it.

## The storage must honour flushes
The docs warn that volatile write-back caches in RAID controllers (without a working
battery-backup unit) and in drives (consumer IDE and SATA drives in particular, and many SSDs)
can lose acknowledged writes in a power failure. Compare the rate that
pg_test_fsync reports with what the hardware can physically do:
```bash
pg_test_fsync -f <path-on-data-volume>/testfile
```
The file must be on the same file system as `pg_wal`. On Linux, `hdparm -I` shows whether write caching is enabled on IDE/SATA drives
and `hdparm -W 0` turns it off; `sdparm --get=WCE` and `sdparm --clear=WCE` do the same for SCSI drives. Also check controller battery status.

## Failed data-file flushes (`data_sync_retry`)
On some operating systems the state of kernel page-cache data is unknown after a write-back failure, so a retried flush can be reported as successful when the data was lost. With the default `data_sync_retry = off` the server raises a PANIC-level error on a failed flush of data files and recovers from WAL. Investigate the root cause (check the OS log and replace faulty hardware) and set `data_sync_retry = on` only after studying the OS's treatment of buffered data.

## Gotchas
- Checksums detect corruption after the fact; they do not prevent it.
- Full-page images inflate WAL right after each checkpoint; that is expected
  (wal_compression reduces it).

## Verify
```sql
SELECT name, setting FROM pg_settings WHERE name IN ('fsync','full_page_writes','synchronous_commit','wal_sync_method');
```
For high-stakes systems, a pull-the-plug test on staging hardware, followed by
`pg_amcheck --all` (PG14+), is the real proof.

## Checked
2026-10-25. Against PostgreSQL 18 documentation (REL_18_STABLE doc/src/sgml, branch head 2026-10-24; PostgreSQL 19 is still at release-candidate stage): `fsync` (unrecoverable corruption risk; safe only if the cluster can be recreated), `full_page_writes` (first change per page after a checkpoint; same circumstances as `fsync = off`), `wal_sync_method` (default rules, "not necessarily ideal"), `data_sync_retry` (default off, PANIC on failed flush, server-start setting), `wal_compression` (compresses full page images), the WAL Reliability section (volatile write-back caches, BBU, consumer drives and SSDs, `hdparm -I`/`-W 0`, `sdparm --get=WCE`/`--clear=WCE`), the pg_test_fsync description (file on the `pg_wal` file system) and the pg_rewind requirement for `full_page_writes`. Removed the ZFS recordsize claim, the fsync-rate thresholds, the PG11.2/12 version gate and the NFS mount advice, which the documentation checked does not give.
Method: documentation only; no commands were run.
