---
id: computing-software.database-administration.yugabytedb.raft-replication-and-failure-handling
name: raft-replication-and-failure-handling
category: computing-software
field: database-administration
product: yugabytedb
tags: [raft, replication-factor, leader-election, remote-bootstrap, fault-tolerance, tablet-peers, follower-unavailable]
level: practitioner
status: docs-checked
description: "How Raft replication and RF=2f+1 govern failure recovery in YugabyteDB: leader failover timing, re-replication delay, and when a node needs remote bootstrap."
sources: ["https://github.com/yugabyte/yugabyte-db/blob/master/docs/content/stable/architecture/docdb-replication/raft.md", "https://github.com/yugabyte/yugabyte-db/blob/master/docs/content/stable/architecture/docdb-replication/replication.md", "https://github.com/yugabyte/yugabyte-db/blob/master/docs/content/stable/architecture/docdb-sharding/cluster-balancing.md", "https://github.com/yugabyte/yugabyte-db/blob/master/docs/content/stable/admin/yb-admin.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Raft replication and failure handling

Each tablet is a Raft group of RF peers (one leader, the rest followers; a peer that is campaigning is a candidate). All writes go through the leader and commit once a majority has them. With RF = 2f+1 the group tolerates f failures.

What happens when a tserver or node dies:
1. Leaders on that node are replaced once the leader failure timeout passes: `--raft_heartbeat_interval_ms` times `--leader_failure_max_missed_heartbeat_periods`, which is 3 seconds with the defaults below.
2. Re-replication of the lost replicas starts only after `follower_unavailable_considered_failed_sec` (tserver reference default 900 seconds). Keep it aligned with `--log_min_seconds_to_retain` (900), because a replica down longer than the retained WAL cannot catch up from the log.
3. A follower unavailable longer than `follower_unavailable_considered_failed_sec` is evicted from the Raft group and its data is re-replicated elsewhere; when a peer fails, an automatic remote bootstrap creates a new peer from the remaining ones.

Heartbeat tuning: `--raft_heartbeat_interval_ms` is 500 ms and `--leader_failure_max_missed_heartbeat_periods` defaults to 6. The multi-data-center deployment guide sets it to 10 for geo-replicated clusters, giving a 5 second failure timeout, and the reference says to use 10 for read replica clusters.

Remote bootstrap traffic is throttled by `remote_bootstrap_rate_limit_bytes_per_sec`. Metrics worth watching: `ts_live_tablet_peers`, the `ChangeConfig`, `StartRemoteBootstrap`, `UpdateConsensus` and `RequestConsensusVotes` handlers, and `hybrid_clock_skew`.

## Checked

2026-11-04. Confirmed against the yb-tserver and yb-master references (follower_unavailable_considered_failed_sec 900 and its match with log_min_seconds_to_retain, heartbeat interval and missed-period defaults, remote bootstrap rate limit), the multi-DC deployment page (value 10, 5 second timeout) and the Raft metrics page (ts_live_tablet_peers, ChangeConfig, StartRemoteBootstrap, UpdateConsensus, RequestConsensusVotes, hybrid_clock_skew). Removed the 3 second leader election claim and the 15 minute catch-up claim, which the pages do not state in that form.

Method: documentation only; no commands were run.
