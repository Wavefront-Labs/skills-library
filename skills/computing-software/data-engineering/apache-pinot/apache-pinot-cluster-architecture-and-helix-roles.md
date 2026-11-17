---
id: computing-software.data-engineering.apache-pinot.apache-pinot-cluster-architecture-and-helix-roles
name: apache-pinot-cluster-architecture-and-helix-roles
category: computing-software
field: data-engineering
product: apache-pinot
tags: [apache-pinot, architecture, helix, zookeeper, controller, broker, server, minion, participant, spectator]
level: intro
status: docs-checked
description: "How Pinot maps onto Helix and ZooKeeper: participant, spectator and controller roles, what ZooKeeper stores, and the realtime segment lifecycle."
sources: ["https://github.com/pinot-contrib/pinot-docs/blob/latest/basics/architecture.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Pinot cluster architecture and Helix roles

Pinot delegates cluster state to Apache Helix, which keeps its state in ZooKeeper. The Helix vocabulary maps onto Pinot objects like this:

- A **segment** is a Helix partition, and a **table** is a Helix resource.
- A **server** is a participant that hosts segments.
- A **broker** is a spectator that watches segment and server state. To support multi-tenancy, brokers are also modelled as participants.
- The **controller** coordinates all state transitions in the cluster and keeps state constraints satisfied.
- A **minion** is a participant that performs computation rather than storing data.

ZooKeeper stores: the current controller leader; the list, configuration and health of servers and brokers; tables, table configs, schemas and each table's segment list; and for each segment its exact server locations, its state (online, offline, error, consuming) and its metadata.

Only one controller is active at a time; the others elect a new leader if it fails. A cluster can serve queries without an active controller but cannot modify metadata (add a table, consume a new segment).

Realtime ingest sequence:
1. The controller creates a consuming-segment entry for each selected realtime server, and servers create consuming segments in memory and connect to the stream (with Kafka each server is a consumer directly).
2. Brokers learn of the consuming segments and include them in query routing immediately.
3. When a server decides its consuming segment is complete, it commits it to a segment file, uploads it to the deep store and notifies the controller.
4. The controller and server create a new consuming segment, and the controller marks the committed segment online; brokers discover it through Helix.

Gotcha: "offline server" and "realtime server" are a convention reflected in table assignment strategy, not different server processes or configurations.

## Checked

2026-11-09. Read the Helix and ZooKeeper, controller, server, minion and ingestion-flow sections of the Pinot docs page `architecture.md`. Confirmed the role mapping, ZooKeeper contents, leader behaviour, ingest sequence and the offline/realtime convention. Removed: the statement that losing ZooKeeper loses the cluster map even if deep-store data survives (not on the page), and a broker "tag membership" phrasing replaced by the documented multi-tenancy reason.
Method: documentation only; no commands were run.
