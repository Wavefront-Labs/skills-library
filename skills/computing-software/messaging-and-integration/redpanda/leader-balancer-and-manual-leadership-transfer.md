---
id: computing-software.messaging-and-integration.redpanda.leader-balancer-and-manual-leadership-transfer
name: leader-balancer-and-manual-leadership-transfer
category: computing-software
field: messaging-and-integration
product: redpanda
tags: [leader-balancer, leadership, transfer-leadership, admin-api, hotspots, heartbeat]
level: advanced
status: docs-checked
description: "How topic-aware leadership balancing works (enable_leader_balancer) and how to move a partition leader by hand with the Admin API transfer_leadership endpoint."
sources:
  - https://docs.redpanda.com/streaming/current/manage/cluster-maintenance/cluster-balancing/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Every partition has one Raft leader that handles all writes. Leadership balancing moves leadership between replicas to avoid hotspots on a few brokers. It transfers no data, only changes where writes land first.

- Controlled by `enable_leader_balancer`, enabled by default, and topic-aware.
- Leaders send heartbeats at `raft_heartbeat_interval_ms`; a follower that misses them triggers an election.
- Besides periodic runs, balancing can occur when a broker restarts or the controller leader changes. The controller leader manages the cluster, for example creating the reallocation plan when decommissioning.

**Manual transfer.** Even leader distribution can still leave traffic-heavy partitions on one broker and cause latency spikes (see the Partition health metrics). Use the Admin API:

```bash
curl -X POST http://<broker_address>:9644/v1/partitions/kafka/<topic>/<partition>/transfer_leadership?target=<destination-broker-id>
```

Example: partition 0 of topic `test` to broker 2:

```bash
curl -X POST "http://localhost:9644/v1/partitions/kafka/test/0/transfer_leadership?target=2"
```

On Kubernetes, send the request to the Pod running the current partition leader.

## Checked

2026-11-04. The balancer behavior, property names, endpoint and examples were confirmed on the Cluster Balancing page. An unsupported closing paragraph about leader pinning was removed.

Method: documentation only; no commands were run.
