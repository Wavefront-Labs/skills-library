---
id: computing-software.database-administration.yugabytedb.metrics-reference-for-operations
name: metrics-reference-for-operations
category: computing-software
field: database-administration
product: yugabytedb
tags: [metrics, monitoring, prometheus, handler-latency, hybrid-clock-skew, ts-live-tablet-peers, throughput, percentile]
level: practitioner
status: docs-checked
description: "Which YugabyteDB metrics to watch: master and YSQL handler latencies, Raft counters, clock skew, cache and SST metrics, and the attributes each metric exposes."
sources: ["https://github.com/yugabyte/yugabyte-db/blob/master/docs/content/stable/launch-and-manage/monitor-and-alert/metrics/ybmaster.md", "https://github.com/yugabyte/yugabyte-db/blob/master/docs/content/stable/launch-and-manage/monitor-and-alert/metrics/raft-dst.md", "https://github.com/yugabyte/yugabyte-db/blob/master/docs/content/stable/launch-and-manage/monitor-and-alert/metrics/throughput.md", "https://github.com/yugabyte/yugabyte-db/blob/master/docs/content/stable/launch-and-manage/monitor-and-alert/metrics/cache-storage.md", "https://github.com/yugabyte/yugabyte-db/blob/master/docs/content/stable/launch-and-manage/monitor-and-alert/metrics/replication.md", "https://github.com/yugabyte/yugabyte-db/blob/master/docs/content/stable/architecture/docdb-sharding/cluster-balancing.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Metrics reference for operations

The yb-master and yb-tserver reference pages show the Prometheus endpoint as `/prometheus-metrics` on the web UI port (master 7000, tserver 9000); `?show_help=true` adds type and help text.

Handler latency metrics are counters in microseconds with these attributes: `total_count`, `min`, `mean`, `Percentile_75`, `Percentile_95`, `Percentile_99`, `Percentile_99_9`, `Percentile_99_99`, `max` and `total_sum`. `total_count` is how many times the metric was measured, so its change over time gives throughput; `total_sum` is the sum of all measured values (two SELECTs of 10 and 6 microseconds give total_count=2, total_sum=16, mean=8). The attributes are present on all handler_latency metrics but may not be calculated for every one.

Throughput at the tablet level: `handler_latency_yb_tserver_TabletServerService_Read` and `handler_latency_yb_tserver_TabletServerService_Write`. YSQL statement time is split by statement type: Insert, Select, Update, Begin, Commit, Rollback, OtherStmts and Transactions.

Key groups:
- **Master:** `handler_latency_yb_master_MasterClient_GetTabletLocations`, `handler_latency_yb_master_MasterDdl_CreateTable` and `handler_latency_yb_master_MasterDdl_DeleteTable`. The tablet-level Read and Write handlers above also measure reads and writes of the PostgreSQL system tables during DDL.
- **Raft and tablets:** `ts_live_tablet_peers` (live Raft tablet peers on a tserver, including system tablets); `handler_latency_yb_consensus_ConsensusService_UpdateConsensus`, `..._RequestConsensusVotes` (a high count means many replicas are looking for an election after missing leader heartbeats, for example from high CPU or a partition) and `..._ChangeConfig` (peer adds or removals, which rise when data moves); `handler_latency_yb_consensus_ConsensusService_StartRemoteBootstrap`; and `hybrid_clock_skew`, a gauge in microseconds, where skew above 500 ms may impact consistency guarantees.
- **YSQL:** `handler_latency_yb_ysqlserver_SQLProcessor_InsertStmt`, `_SelectStmt`, `_UpdateStmt`, `_BeginStmt`, `_CommitStmt` and `_RollbackStmt`. These cover parse and execute after query processing begins, and do not include deserializing network bytes or parsing the query. `handler_latency_yb_ysqlserver_SQLProcessor_CatalogCacheTableMisses_count` counts catalog cache misses per pg_catalog table.
- **Storage:** `rocksdb_number_db_seek`, `rocksdb_number_db_next` and `rocksdb_number_db_prev`; `rocksdb_block_cache_hit` and `rocksdb_block_cache_miss`; `rocksdb_bloom_filter_checked` and `rocksdb_bloom_filter_useful`; `rocksdb_current_version_sst_files_size` and `rocksdb_current_version_num_sst_files`; `ts_active_data_size` (excludes snapshots and hidden tablets) and `ts_data_size` (includes snapshots; the difference is snapshot overhead). WAL metrics include `log_sync_latency` and `log_append_latency`.
- **Balancing** (from the cluster balancing page): `total_table_load_difference`, `blacklisted_leaders`, `tablets_in_wrong_placement` and `estimated_data_to_balance_bytes`; the cluster is balanced when the first three reach 0, and the bytes metric is the best indicator of how long balancing will take.
- **xCluster replication:** `async_replication_committed_lag_micros` and `time_since_last_getchanges` (source cluster only, microseconds); `consumer_safe_time_lag` and `consumer_safe_time_skew` (target cluster only, transactional xCluster only). The page's intro says all replication metrics are in microseconds, but its table gives the two consumer metrics in milliseconds; trust the per-metric description.

## Checked

2026-11-04. Confirmed against the YB-Master, Raft, Throughput and latency, Cache and storage, and xCluster metrics pages (metric names, attributes, units, descriptions, 500 ms skew warning). Removed: the `/metrics` path and YCQL/YSQL port claims (the reference pages show `/prometheus-metrics`), `async_replication_sent_lag_micros`, the Limits group (`ts_supportable_tablet_peers`, `create_table_too_many_tablets`), none of which appear on the cited pages. Corrected the bloom filter and SST metric names to their `rocksdb_` prefixed forms. Page inconsistency noted in the skill: the xCluster page says all metrics are microseconds but lists the consumer ones in milliseconds.

Method: documentation only; no commands were run.
