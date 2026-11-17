---
id: computing-software.database-administration.postgresql.database-and-relation-size-monitoring
name: database-and-relation-size-monitoring
category: computing-software
field: database-administration
product: postgresql
tags: [database-administration, postgresql, postgres, pg-monitoring, pg-database-size, pg-relation-size, pg-total-relation-size, disk-usage, toast, pg-ls-waldir, capacity-planning]
level: practitioner
status: verified
description: "Measure PostgreSQL disk use by database, table, index, TOAST and WAL with pg_database_size, pg_relation_size and friends, and find what is filling the disk."
sources:
  - https://www.postgresql.org/docs/current/diskusage.html
  - https://www.postgresql.org/docs/current/functions-admin.html#FUNCTIONS-ADMIN-DBSIZE
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Database and relation size monitoring

**Goal:** when the volume alarms, find within minutes whether it is a table, an index, TOAST, WAL, or temp files.

## Per database
```sql
SELECT datname, pg_size_pretty(pg_database_size(datname)) FROM pg_database ORDER BY pg_database_size(datname) DESC;
```

## Biggest relations, split by component
```sql
SELECT c.oid::regclass AS rel,
       pg_size_pretty(pg_total_relation_size(c.oid)) AS total,
       pg_size_pretty(pg_relation_size(c.oid))       AS heap,
       pg_size_pretty(pg_indexes_size(c.oid))        AS indexes,
       pg_size_pretty(pg_total_relation_size(c.oid) - pg_relation_size(c.oid) - pg_indexes_size(c.oid)) AS toast_etc
FROM pg_class c JOIN pg_namespace n ON n.oid = c.relnamespace
WHERE c.relkind IN ('r','m','p') AND n.nspname NOT IN ('pg_catalog','information_schema')
ORDER BY pg_total_relation_size(c.oid) DESC LIMIT 20;
```
| Function | Includes |
|---|---|
| `pg_relation_size(rel)` | Main fork only (add `'fsm'`/`'vm'` for other forks) |
| `pg_table_size(rel)` | Heap + TOAST + FSM + VM, no indexes |
| `pg_indexes_size(rel)` | All indexes of the table |
| `pg_total_relation_size(rel)` | Everything |

Partitioned parents report 0 (checked: all four functions returned 0 for a partitioned table); sum the children: `SELECT sum(pg_total_relation_size(relid)) FROM pg_partition_tree('parent')`.

## Outside the tables
```sql
SELECT pg_size_pretty(sum(size)) FROM pg_ls_waldir();               -- pg_wal
SELECT slot_name, active, pg_size_pretty(pg_wal_lsn_diff(pg_current_wal_lsn(), restart_lsn)) AS retained
FROM pg_replication_slots;                                             -- slots pinning WAL
SELECT datname, temp_files, pg_size_pretty(temp_bytes) FROM pg_stat_database;  -- temp spill since reset
```
On disk: `du -sh $PGDATA/base $PGDATA/pg_wal` plus your `log_directory` (default `log`; `pg_log` was the name before PG10; there are no log files at all unless `logging_collector` is on). Map a big file to a relation with `SELECT pg_filenode_relation(0, <filenode>)`.

## Usual culprits
- An inactive replication slot retaining WAL: drop it or set `max_slot_wal_keep_size`.
- Failing `archive_command`: WAL accumulates; check `pg_stat_archiver.last_failed_time`.
- Bloat after mass deletes: size stays high until `pg_repack` / `VACUUM FULL`.
- Log files without rotation.

## Gotchas
- The size functions read file sizes for every file of every relation they cover: cheap per call, but avoid per-second polling across thousands of partitions.
- `pg_database_size` needs CONNECT privilege on the database (`permission denied for database pd` after `REVOKE CONNECT ... FROM PUBLIC`) or membership in `pg_read_all_stats`.

## Verify
`sum(pg_database_size)` + `pg_wal` + logs roughly equals `du -sh $PGDATA`.

## Checked
PostgreSQL 17.6: the database, relation-breakdown, `pg_ls_waldir`, `pg_replication_slots`, `pg_stat_database` temp-file and `pg_stat_archiver` queries all run; `pg_relation_size(rel, 'fsm')` and `'vm'` return 24 kB and 8 kB for a 17 MB table; `pg_partition_tree` sum gave 1600 kB for a partitioned table whose own size functions return 0; `pg_filenode_relation(0, filenode)` mapped a filenode to its table and `1259` to `pg_class`; `log_directory` defaults to `log`; a role without CONNECT got the quoted error. `max_slot_wal_keep_size` is -1 by default.
