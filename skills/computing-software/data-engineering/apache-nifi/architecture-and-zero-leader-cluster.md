---
id: computing-software.data-engineering.apache-nifi.architecture-and-zero-leader-cluster
name: architecture-and-zero-leader-cluster
category: computing-software
field: data-engineering
product: apache-nifi
tags: [data-engineering, apache-nifi, architecture, cluster-coordinator, primary-node, zookeeper]
level: intro
status: docs-checked
description: "NiFi core concepts and architecture: FlowFile, processor, connection, flow controller, process group, three repositories, and the Zero-Leader cluster with coordinator and primary."
sources:
  - https://nifi.apache.org/docs/nifi-docs/html/overview.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Architecture

Concepts: FlowFile (attributes plus content), FlowFile Processor, Connection (a queue with prioritization and back-pressure limits), Flow Controller (threads and scheduling), Process Group (processors exposed by ports).

Inside the JVM: web server (HTTP command and control), flow controller, extensions, and three pluggable repositories: FlowFile (default persistent write-ahead log), Content (default file system blocks, multiple locations allowed) and Provenance (indexed, searchable, disk-based).

Cluster (Zero-Leader since 1.0): every node does the same work on different data; ZooKeeper elects one Cluster Coordinator (receives heartbeats, connects and disconnects nodes) and one Primary Node. Use any node's UI and changes replicate to all.

Verify: the Cluster dialog shows one coordinator and one primary node.

## Checked

Confirmed against the NiFi Overview (core concepts, NiFi Architecture). Failover of the coordinator is handled automatically by ZooKeeper; nodes report heartbeats to the coordinator.

Method: docs-only read of cited pages, 2026-11-08
