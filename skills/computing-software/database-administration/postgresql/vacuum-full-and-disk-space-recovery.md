---
id: computing-software.database-administration.postgresql.vacuum-full-and-disk-space-recovery
name: vacuum-full-and-disk-space-recovery
category: computing-software
field: database-administration
product: postgresql
tags: [database-administration, postgresql, vacuum, vacuum-full, table-bloat, disk-space, cluster-command, maintenance]
level: practitioner
status: verified
description: "Decide between plain VACUUM, VACUUM FULL, CLUSTER and pg_repack to return disk space, and run VACUUM FULL safely given its exclusive lock and 2x space need."
sources:
  - https://www.postgresql.org/docs/current/routine-vacuuming.html#VACUUM-FOR-SPACE-RECOVERY
  - https://www.postgresql.org/docs/current/sql-vacuum.html
  - https://www.postgresql.org/docs/current/sql-cluster.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# VACUUM FULL and recovering disk space

## What each option does
| Command | Frees space to OS? | Lock | Extra disk |
|---|---|---|---|
| `VACUUM` | only trailing empty pages (truncation: a table of 200,000 rows shrank from 7.3 MB to 40 kB after deleting all but the first 1,000; deleting every other row left it at 7.3 MB); otherwise marks space reusable inside the table | SHARE UPDATE EXCLUSIVE (reads and writes continue) | none |
| `VACUUM FULL` | yes, rewrites table + indexes compactly | **ACCESS EXCLUSIVE** for the whole run (no reads) | size of the new copy |
| `CLUSTER tbl USING idx` | yes, rewrites in index order | ACCESS EXCLUSIVE | new copy |
| `pg_repack` | yes, online rewrite | brief exclusive locks at start/end | new copy |

Plain VACUUM is enough when the table will grow back into its free space. Rewrite only when
the bloat is permanent (a big one-off delete) and the space is needed elsewhere.

## Measure first
```sql
SELECT pg_size_pretty(pg_total_relation_size('events')) AS total,
       n_live_tup, n_dead_tup, last_autovacuum
FROM pg_stat_user_tables WHERE relname = 'events';
-- accurate free-space figure (reads the whole table):
CREATE EXTENSION IF NOT EXISTS pgstattuple;
SELECT * FROM pgstattuple_approx('events');
```

## Running VACUUM FULL safely
```sql
SET lock_timeout = '5s';        -- do not queue behind a long transaction and block everyone (checked: while VACUUM FULL waited for ACCESS EXCLUSIVE behind an open reader, a new SELECT queued behind it)
VACUUM (FULL, VERBOSE, ANALYZE) events;
```
- Needs free disk for a new copy of table + indexes (docs: it writes a new copy and does not release the old one until the operation is complete). A 400,000-row test table went from 43 MB to 4.3 MB total after deleting 90% of the rows.
- Every query on the table waits for the duration; on a 200 GB table that is hours. Use
  pg_repack for anything that must stay online.
- A long-running transaction elsewhere holding back xmin means dead rows still visible to it are copied, not removed (checked: with a REPEATABLE READ session open on another table, `VACUUM FULL` left a 3.6 MB table that shrank to 1.8 MB after the session ended). Check
  `backend_xmin` in `pg_stat_activity` first; the same applies to replication slots and `hot_standby_feedback` holding xmin back.
- Never run database-wide `VACUUM FULL` as routine maintenance.

## Freeing space urgently on a full disk
VACUUM FULL needs space you do not have. Options in order: drop unneeded indexes or old
partitions (immediate), move a table to another tablespace (`ALTER TABLE ... SET TABLESPACE`,
also exclusive), `TRUNCATE` scratch tables, extend the volume.

## Verify
Re-run the size query; `pg_total_relation_size` drops and `df` on the data volume shows the
space back.

## Checked
PostgreSQL 17.6: plain `VACUUM` truncated trailing empty pages but not mid-table holes (sizes above); `VACUUM (FULL, ANALYZE)` rewrote a bloated table to about a tenth of its size; with a session holding AccessShareLock, `VACUUM (FULL)` with `lock_timeout = '3s'` failed with `canceling statement due to lock timeout` and a second reader timed out behind it; the `backend_xmin` effect measured as quoted; `pgstattuple_approx` is installed with pgstattuple (columns include `approx_free_percent`). Docs (sql-vacuum): FULL takes an exclusive lock and needs extra disk space. Docs: sql-cluster (ACCESS EXCLUSIVE lock for the whole run) and the pg_repack README (short exclusive locks at the start and end, works online).
