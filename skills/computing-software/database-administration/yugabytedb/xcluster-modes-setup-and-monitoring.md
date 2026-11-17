---
id: computing-software.database-administration.yugabytedb.xcluster-modes-setup-and-monitoring
name: xcluster-modes-setup-and-monitoring
category: computing-software
field: database-administration
product: yugabytedb
tags: [xcluster, async-replication, transactional-xcluster, non-transactional-xcluster, safe-time, setup-universe-replication, replication-lag]
level: advanced
status: docs-checked
description: "Choose between non-transactional and transactional xCluster, set up replication with setup_universe_replication, and monitor lag and safe time with yb-admin."
sources: ["https://github.com/yugabyte/yugabyte-db/blob/master/docs/content/stable/architecture/docdb-replication/async-replication.md", "https://github.com/yugabyte/yugabyte-db/blob/master/docs/content/stable/deploy/multi-dc/async-replication/async-deployment.md", "https://github.com/yugabyte/yugabyte-db/blob/master/docs/content/stable/deploy/multi-dc/async-replication/async-transactional-setup-manual.md", "https://github.com/yugabyte/yugabyte-db/blob/master/docs/content/stable/launch-and-manage/monitor-and-alert/xcluster-monitor.md", "https://github.com/yugabyte/yugabyte-db/blob/master/docs/content/stable/launch-and-manage/monitor-and-alert/metrics/replication.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# xCluster modes, setup and monitoring

xCluster replicates WAL records asynchronously from source universe tablets to target universe tablets, using pollers in the target.

**Non-transactional:** writes are replicated to target tablets independently and applied with the timestamp they committed on the source. Reads on the target do not wait for the latest source data or for all related writes, so they can be inconsistent within a table (across tablets) and across tables and indexes; YSQL transactions on the target can see non-repeatable and phantom reads. If both universes write the same primary key row, the last writer (by hybrid time) wins, and concurrent writes can corrupt YSQL indexes. If the source fails, torn transactions can remain on the target and do not heal automatically. For YSQL deployments, transactional mode is preferred.

**Transactional (YSQL only):** reads on the target happen as of the xCluster safe time, typically 1 to 2 seconds in the past, and writes to the target are not allowed (so no bidirectional replication). It has three modes: automatic (recommended for new deployments), semi-automatic, and manual, which is deprecated. In the fully manual setup you need PITR on the standby: `yb-admin create_snapshot_schedule 1 10 ysql.yugabyte` against the standby masters, set up replication with the `transactional` option, then run `yb-admin change_xcluster_role STANDBY` against the standby masters.

Setup (non-transactional), run against the target masters:
```
yb-admin --master_addresses <target_masters> setup_universe_replication <source_universe_UUID>_<replication_stream_name> <source_masters> <table_id1>,<table_id2>
```
Find table ids with `yb-admin --master_addresses <source_masters> list_tables include_table_id` (include index tables); the source universe UUID is the `--cluster_uuid` value on `http://yb-master-ip:7000/varz`.

Monitor:
```
yb-admin --master_addresses <target_masters> get_replication_status
yb-admin --master_addresses <target_masters> list_universe_replications
yb-admin --master_addresses <source_masters> list_xcluster_outbound_replication_groups
yb-admin --master_addresses <target_masters> get_xcluster_safe_time include_lag_and_skew
```
`get_replication_status` covers consumer-side streams; an empty `errors` field means the stream is healthy. `list_universe_replications` lists inbound groups on the standby and `list_xcluster_outbound_replication_groups` outbound groups on the primary.

Metrics: `async_replication_sent_lag_micros` and `async_replication_committed_lag_micros` (source cluster; take the maximum across the source tservers), plus `consumer_safe_time_lag` and `consumer_safe_time_skew` (target cluster, in milliseconds, transactional xCluster only). The `/xcluster` page on the master and tserver UIs shows replication health.

## Checked

2026-11-09: mode behaviour, 1 to 2 second safe-time reads, deprecation of manual mode, the setup_universe_replication and monitoring commands, the manual transactional steps, the `/varz` UUID lookup, metric names and the `/xcluster` pages confirmed against the five cited pages (yugabyte-db docs async-replication.md, async-deployment.md, async-transactional-setup-manual.md, xcluster-monitor.md, metrics/replication.md; relevant sections read, others searched). Replaced the vague "target accepts writes" wording with the documented non-transactional behaviour and added the documented UUID lookup and metric scopes.

Method: docs-checked 2026-11-09 against the five yugabyte-db docs pages cited above (sections read, not every line)
