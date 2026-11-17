---
id: computing-software.database-administration.dragonfly.multi-shard-cluster-setup
name: multi-shard-cluster-setup
category: computing-software
field: database-administration
product: dragonfly
tags: [multi-shard-cluster, cluster-mode, admin-port, control-plane, dragonfly-swarm]
level: advanced
status: docs-checked
description: "Start a Dragonfly multi-shard cluster with cluster_mode=yes and an admin port, and understand that Dragonfly supplies only the data plane."
sources:
  - https://raw.githubusercontent.com/dragonflydb/documentation/main/docs/managing-dragonfly/cluster-mode.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A Dragonfly Cluster distributes keys and supports hash tags like Valkey Cluster, and offers the cluster commands client libraries need. Client code written for Redis Cluster should migrate unchanged.

**Key distinction:** Dragonfly provides only the data plane (the server). It does **not** provide a control plane: node health monitoring, automatic failover and slot migration for rebalancing are provided by Dragonfly Cloud (Dragonfly Swarm), or you build your own. Nodes do not communicate with each other except for replication and slot migration.

Steps:

1. Start every node (masters and replicas) with `--cluster_mode=yes` and `--admin_port=X`. Do not expose the admin port to data store users.
2. Until configured, a node answers user requests with errors.
3. Configure replication with `REPLICAOF`, even though the cluster configuration lists replicas too.
4. Push the cluster configuration through the admin port (see the DFLYCLUSTER config skill).

Notes:

- Multi-shard cluster mode supports only database 0.
- After configuration a node deletes keys it does not own and rejects access to them.
- If `DFLYCLUSTER CONFIG` errors, run with `--logtostderr` to see why it was rejected.

## Checked

2026-11-04. Confirmed in the Cluster Mode page (multi-shard section: data plane only, start flags, errors until configured, REPLICAOF, DFLYCLUSTER CONFIG, database 0 only, key deletion, `--logtostderr`). Nothing removed.

Method: documentation only; no commands were run.
