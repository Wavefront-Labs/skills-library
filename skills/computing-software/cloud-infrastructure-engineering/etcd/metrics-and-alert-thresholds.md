---
id: computing-software.cloud-infrastructure-engineering.etcd.metrics-and-alert-thresholds
name: metrics-and-alert-thresholds
category: computing-software
field: cloud-infrastructure-engineering
product: etcd
tags: [alerts, prometheus-alerts, wal-fsync, backend-commit, leader-changes, proposals, disk-latency, slo]
level: advanced
status: docs-checked
description: "Which etcd metrics to watch and why: has_leader, leader changes, proposals, fsync and backend commit latency, file descriptors."
sources:
  - "https://etcd.io/docs/v3.5/op-guide/monitoring/"
  - "https://etcd.io/docs/v3.5/metrics/"
  - "https://etcd.io/docs/v3.5/faq/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

What the etcd documentation says about each metric (the pages give no alert rules or durations, so choose those yourself):

- `etcd_server_has_leader`: 1 if the member has a leader, 0 if not. A member without a leader is totally unavailable; if all members lack a leader the whole cluster is unavailable.
- `etcd_server_leader_changes_seen_total`: leader changes the member has seen since start. Rapid leadership changes significantly impact performance and signal an unstable leader, perhaps from network connectivity issues or excessive load.
- `etcd_server_proposals_failed_total`: normally related to temporary failures during a leader election or longer downtime from loss of quorum.
- `etcd_server_proposals_pending`: proposals queued to commit. Rising pending proposals suggest high client load or that the member cannot commit proposals.
- `etcd_server_proposals_committed_total` minus `etcd_server_proposals_applied_total`: usually small (within a few thousands even under high load). If the gap keeps rising the server is overloaded, for example by heavy range queries or large txn operations. A consistently large lag between one member and its leader in committed proposals indicates a slow or unhealthy member.
- Disk latency: `etcd_disk_wal_fsync_duration_seconds` and `etcd_disk_backend_commit_duration_seconds` histograms; high values often indicate disk issues and can cause high request latency or instability. The FAQ gives p99 targets: `wal_fsync_duration_seconds` under 10ms and `backend_commit_duration_seconds` under 25ms.
- Network: `etcd_network_peer_round_trip_time_seconds` is a round-trip-time histogram between peers. The FAQ says to tune `heartbeat-interval` to roughly match the round trip time between machines and `election-timeout` to at least 5 times the heartbeat interval.
- File descriptors: `process_open_fds` near `process_max_fds` indicates possible exhaustion, and etcd may panic if it cannot create new WAL files.
- Abnormally high `etcd_debugging_snapshot_save_total_duration_seconds` (debugging namespace, volatile) indicates disk issues.

## Checked

2026-11-08. Read in full: etcd v3.5 Monitoring etcd page, Metrics page and FAQ page (added as a source for the p99 disk targets and heartbeat guidance). Confirmed every metric description above. Removed: the one-minute and few-per-hour thresholds, the gRPC handled-total and slow-apply metrics, database size alert guidance and the process restart item (not on the pages read).
Method: documentation only; no commands were run.
