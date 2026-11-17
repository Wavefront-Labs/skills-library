---
id: computing-software.data-engineering.apache-nifi.cluster-heartbeat-and-election
name: cluster-heartbeat-and-election
category: computing-software
field: data-engineering
product: apache-nifi
tags: [data-engineering, apache-nifi, clustering, heartbeat, flow-election, coordinator]
level: advanced
status: docs-checked
description: "Cluster heartbeat interval 5 sec, 8 missable beats (40 sec disconnect), flow election wait 5 mins and max candidates, plus node connection and read timeouts."
sources:
  - https://nifi.apache.org/docs/nifi-docs/html/administration-guide.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Heartbeats and flow election

Configure identically on all nodes:
- `nifi.cluster.protocol.heartbeat.interval`: 5 sec
- `nifi.cluster.protocol.heartbeat.missable.max`: 8, the number of heartbeats the Cluster Coordinator can miss before it marks the node Disconnected (8 x 5 sec = 40 sec by arithmetic on the defaults)
- `nifi.cluster.protocol.is.secure`: false

Flow election when a cluster starts:
- `nifi.cluster.flow.election.max.wait.time`: 5 mins, counted from the first vote.
- `nifi.cluster.flow.election.max.candidates`: the number of voted nodes that ends the wait early; no default is stated.

Request handling:
- `nifi.cluster.node.connection.timeout` and `nifi.cluster.node.read.timeout`: 5 secs
- `nifi.cluster.node.max.concurrent.requests`: 100 outstanding replicated web requests; beyond that Jetty returns 409 Conflict

Verify: set max.candidates to your node count and the cluster elects its flow without waiting the full 5 minutes.

## Checked

Confirmed in the NiFi Administration Guide, Cluster Common Properties and Cluster Node Properties tables: heartbeat interval 5 sec, missable max 8, is.secure false, election max wait 5 mins (clock starts at the first vote), election max candidates (early election), connection and read timeouts 5 secs, max concurrent requests 100 with a 409 Conflict response, and the instruction to configure the common properties the same on all nodes. The 40 second figure is arithmetic, not stated by the guide.

Method: docs-only read of cited pages, 2026-11-08
