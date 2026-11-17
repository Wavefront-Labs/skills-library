---
id: computing-software.data-engineering.apache-nifi.cluster-load-balance-properties
name: cluster-load-balance-properties
category: computing-software
field: data-engineering
product: apache-nifi
tags: [data-engineering, apache-nifi, load-balancing, clustering, nifi-properties, connections]
level: advanced
status: docs-checked
description: "Node-side load balancing keys: port 6342, host fallback, connections per node, max threads 8, comms timeout 30 sec, used by connection load balance strategies."
sources:
  - https://nifi.apache.org/docs/nifi-docs/html/administration-guide.html
  - https://nifi.apache.org/docs/nifi-docs/html/user-guide.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cluster load balancing properties

- `nifi.cluster.load.balance.port`: 6342
- `nifi.cluster.load.balance.host`: falls back to `nifi.cluster.node.address`
- `nifi.cluster.load.balance.connections.per.node`: 1
- `nifi.cluster.load.balance.max.thread.count`: 8 (no benefit above nodes x connections per node)
- `nifi.cluster.load.balance.comms.timeout`: 30 sec

These govern the transport that moves FlowFiles between nodes when a connection uses a load balance strategy (partition by attribute, round robin or single node). The admin guide's port table also lists `nifi.cluster.node.load.balance.port` with default 6342.

Verify: with a round-robin connection on a multi-node cluster, the Cluster Connection Summary shows data on every node.

## Checked

Confirmed in the NiFi Administration Guide Cluster Common Properties: load balance port 6342, host fallback to nifi.cluster.node.address, connections per node default 1, max thread count 8 with its note, comms timeout 30 sec; and the port table entry for nifi.cluster.node.load.balance.port 6342. The User Guide confirms the Do not load balance (default), Round robin and Single node strategies and the Cluster Connection Summary dialog.

Method: docs-only read of cited pages, 2026-11-08
