---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.consensus-system-monitoring
name: consensus-system-monitoring
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [consensus-monitoring-metrics, etcd-monitoring, distributed-consensus, prometheus, raft, alerting-rules]
level: advanced
status: docs-checked
description: "Monitor consensus clusters per the SRE Book list (members, leader changes, proposals, lag, latency, disk) mapped to documented etcd Prometheus metrics."
sources: ["https://sre.google/sre-book/managing-critical-state/", "https://etcd.io/docs/v3.5/metrics/", "https://etcd.io/docs/v3.5/op-guide/monitoring/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Monitoring consensus systems

SRE Book "Monitoring Distributed Consensus Systems" lists what to watch:
- number of members running in each consensus group and the status of each process (a process may run but be
  unable to make progress);
- persistently lagging replicas (members may be recovering, lagging, up to date, or the leader);
- whether a leader exists (with no leader a leader-based system is totally unavailable);
- number of leader changes (rapid increase means the leader is flapping, perhaps from network problems; a
  decrease in the view number could signal a serious bug);
- consensus transaction number, which should increase over time if the system is healthy;
- number of proposals seen and agreed;
- throughput and latency;
and, for troubleshooting: latency distributions for proposal acceptance, network latencies between locations,
time acceptors spend on durable logging, and overall bytes accepted per second.

## etcd metrics mapping (etcd v3.5 metrics page)
The `etcd`-prefixed metrics are stable and meant for monitoring and alerting; `etcd_debugging` metrics are
volatile and may change without warning.

| Book item | etcd metric |
|---|---|
| leader exists | `etcd_server_has_leader` (1 or 0; without a leader the member is totally unavailable) |
| leader changes | `etcd_server_leader_changes_seen_total` (rapid changes hurt performance) |
| proposals committed / applied / pending / failed | `etcd_server_proposals_committed_total`, `etcd_server_proposals_applied_total`, `etcd_server_proposals_pending`, `etcd_server_proposals_failed_total` |
| progress | `proposals_committed_total` should increase over time on a healthy cluster |
| lagging replica | compare `proposals_committed_total` across members; a consistently large lag between one member and its leader means it is slow or unhealthy |
| apply backlog | the gap between committed and applied should usually be small; a continuously rising gap means the server is overloaded (for example heavy range queries or large txns) |
| pending proposals | rising `proposals_pending` suggests high client load or a member that cannot commit |
| disk latency | `etcd_disk_wal_fsync_duration_seconds`, `etcd_disk_backend_commit_duration_seconds` (histograms; high values often indicate disk issues) |
| network latency | `etcd_network_peer_round_trip_time_seconds` (histogram between peers) |
| file descriptors | `process_open_fds` against `process_max_fds`; exhaustion can make etcd panic when it cannot create WAL files |

`proposals_failed_total` normally relates to temporary leader-election failures or longer downtime from losing
quorum.

## Alert rules
etcd publishes a default set of alerts for Prometheus (see its monitoring guide). Thresholds and `for:`
durations are yours to choose; a minimal example for the most important condition:
```yaml
- alert: EtcdNoLeader
  expr: etcd_server_has_leader == 0
  for: 1m
```

## Gotchas
- A cluster with quorum but no progress is effectively down for writers; alert on lack of progress (committed
  proposals not increasing), not only on leader existence.
- etcd does not persist metrics: a member restart resets them.

## Verify
- [ ] Dashboard shows the full SRE Book list per cluster.
- [ ] Stopping a majority of members pages; stopping a minority does not.

## Checked

Checked 2026-11-09. Confirmed against the SRE Book Managing Critical State page (monitoring list) and the etcd v3.5 metrics page (server, disk, network and process metrics and their descriptions); the etcd monitoring page was read and confirms only that a default Prometheus alert set exists. Removed: the quota and DB-size metrics, mvcc revision and cluster_version metrics, numeric alert thresholds and the mixin path, which appeared on no page read.

Method: docs-checked 2026-11-09 against the pages above, read from downloaded copies; no commands were run.
