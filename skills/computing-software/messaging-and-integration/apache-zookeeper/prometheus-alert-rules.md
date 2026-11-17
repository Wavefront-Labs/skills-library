---
id: computing-software.messaging-and-integration.apache-zookeeper.prometheus-alert-rules
name: prometheus-alert-rules
category: computing-software
field: messaging-and-integration
product: apache-zookeeper
tags: [messaging-and-integration, apache-zookeeper, alerting, alertmanager, promtool, znode-count, election-time, thresholds]
level: advanced
status: docs-checked
description: "Starter Prometheus alert expressions for ZooKeeper from the monitoring guide: server down, znode and watch counts, connections, elections, fsync and heap."
sources:
  - https://zookeeper.apache.org/doc/current/zookeeperMonitor.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Example alert rules

Thresholds below are the guide's examples; tune them.

- `up == 0` for 1 minute: server down (critical).
- `znode_count > 1000000`.
- `num_alive_connections > 50` (default maxClientCnxns is 60).
- `approximate_data_size / 1024 / 1024 > 1024` (over 1 GB of data).
- `watch_count > 10000`.
- `increase(election_time_count[5m]) > 0`: a leader election occurred.
- `open_file_descriptor_count > 300`.
- `rate(fsynctime_sum[1m]) > 100`: slow fsync.
- `rate(snapshottime_sum[5m]) > 100`: slow snapshots.
- `avg_latency > 100`.
- `jvm_memory_bytes_used / jvm_memory_bytes_max{area="heap"} > 0.8` for 5 minutes.

Send notifications through Prometheus Alertmanager and validate rule files with `promtool check rules`.

Verify: `promtool check rules` passes and a test stop of one server fires the down alert.

## Checked

Method: docs-checked 2026-11-09 against zookeeperMonitor.html (full page read, alert rule example compared expression by expression)
