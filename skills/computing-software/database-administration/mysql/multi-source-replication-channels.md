---
id: computing-software.database-administration.mysql.multi-source-replication-channels
name: multi-source-replication-channels
category: computing-software
field: database-administration
product: mysql
tags: [database-administration, mysql, multi-source-replication, replication-channels, channel, data-consolidation, replication, gtid]
level: practitioner
status: docs-checked
description: "Replicate several MySQL sources into one replica with named channels: setup, per-channel filters and control, conflict avoidance and monitoring."
sources:
  - https://dev.mysql.com/doc/refman/8.4/en/replication-multi-source.html
  - https://dev.mysql.com/doc/refman/8.4/en/replication-multi-source-configuration.html
  - https://dev.mysql.com/doc/refman/8.4/en/replication-channels.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Multi-source replication channels

One replica, several sources, each over its own **channel** (own receiver thread, relay log and applier). Typical use: consolidating sharded or per-site databases into one reporting or backup server.

## Prerequisites on the replica
- Replication metadata in TABLE repositories: the default in MySQL 8.4 and the only kind multi-source replication supports (the old FILE repositories are deprecated).
- Distinct `server_id` across all servers; GTIDs on all servers strongly recommended.
- The sources must write to **different schemas or tables**; MySQL does not resolve conflicts between channels.

## Setup (GTID)
```sql
CHANGE REPLICATION SOURCE TO SOURCE_HOST='shard1', SOURCE_USER='repl', SOURCE_PASSWORD='<PASSWORD>',
  SOURCE_AUTO_POSITION=1, SOURCE_SSL=1 FOR CHANNEL 'shard1';
CHANGE REPLICATION SOURCE TO SOURCE_HOST='shard2', SOURCE_USER='repl', SOURCE_PASSWORD='<PASSWORD>',
  SOURCE_AUTO_POSITION=1, SOURCE_SSL=1 FOR CHANNEL 'shard2';
```
Seed data: load each source's backup first. With GTIDs, the replica's `gtid_purged` must be the **union** of the sources' sets: import the dumps, issue `RESET BINARY LOGS AND GTIDS` on the replica, then `SET GLOBAL gtid_purged` to the combined set.

## Per-channel filters
```sql
CHANGE REPLICATION FILTER REPLICATE_WILD_DO_TABLE = ('shard1_db.%') FOR CHANNEL 'shard1';
-- or in my.cnf: replicate-wild-do-table = shard1:shard1_db.%
```

## Control
```sql
START REPLICA FOR CHANNEL 'shard1';
STOP REPLICA FOR CHANNEL 'shard2';
START REPLICA;                          -- all channels
RESET REPLICA ALL FOR CHANNEL 'shard2'; -- remove a channel
```

## Monitoring
```sql
SHOW REPLICA STATUS FOR CHANNEL 'shard1'\G
SELECT CHANNEL_NAME, SERVICE_STATE, LAST_ERROR_MESSAGE FROM performance_schema.replication_connection_status;
SELECT CHANNEL_NAME, SERVICE_STATE, LAST_ERROR_MESSAGE FROM performance_schema.replication_applier_status_by_worker;
```
Alert per channel; one broken channel does not stop the others, so it can go unnoticed.

## Gotchas
- Same schema name from two sources (every shard has `app`) collides. Use `REPLICATE_REWRITE_DB` per channel to map `app` -> `app_shard1` (works with row-based events for tables qualified by default database; test cross-database statements).
- DDL on a shared table name from two channels races; keep schemas disjoint.

## Checked

2026-10-31: confirmed replication channels and per-channel threads (each channel gets the specified applier threads plus a coordinator) on the dev.mysql.com replication-multi-source and replication-threads pages; TABLE repositories as the 8.4 default and FILE as deprecated (replication-multi-source-configuration); CHANGE REPLICATION FILTER ... FOR CHANNEL and the option-file channel-prefix syntax `replicate-wild-do-table=channel:db.tbl` (replication-rules-channel-based-filters); GTID provisioning via RESET BINARY LOGS AND GTIDS and gtid_purged set to the union of the sources' sets (replication-multi-source-provision-replica). Replaced the '+' gtid_purged append syntax with the documented union approach.
Method: documentation only; no commands were run.
- `replica_parallel_workers` applies to every channel: each channel gets that many applier threads plus a coordinator thread.
