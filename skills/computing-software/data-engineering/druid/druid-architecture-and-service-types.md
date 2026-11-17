---
id: computing-software.data-engineering.druid.druid-architecture-and-service-types
name: druid-architecture-and-service-types
category: computing-software
field: data-engineering
product: druid
tags: [architecture, services, master-server, query-server, data-server, process-types]
level: intro
status: docs-checked
description: "Explain Druid's services, the Master, Query and Data server grouping, colocation advice and the three external dependencies."
sources:
  - https://github.com/apache/druid/blob/master/docs/design/architecture.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Druid is distributed, cloud-friendly and easy to operate. Services scale independently and an outage of one component does not immediately affect others.

## Services

- Coordinator: manages data availability; assigns segments to Historicals and keeps them balanced.
- Overlord: controls ingestion workloads; assigns tasks to Middle Managers and coordinates segment publishing.
- Broker: receives client queries, forwards to Data servers, merges results. Query Brokers, not Historicals or Middle Managers directly.
- Router: unified API gateway in front of Brokers, Overlords and Coordinators; also serves the web console.
- Historical: stores and serves queryable data; downloads segments from deep storage; accepts no writes.
- Middle Manager: reads external sources and publishes segments. Peon: a task execution JVM spawned by a Middle Manager, one task each, always on the same host.
- Indexer (optional, designated experimental): runs tasks as threads in one JVM instead of forking Peons; easier to configure and shares resources across tasks. Deploy only one of: Middle Managers, Kubernetes-based Middle Manager-less ingestion, or Indexers.

## Server types (recommended grouping, not mandatory)

- Master: Coordinator and Overlord.
- Query: Broker and optionally Router.
- Data: Historical and Middle Manager (or Indexer).
The web console Services tab shows running services.

## Colocation

Colocating by server type usually uses hardware best; very large clusters may split services to avoid contention.
- Coordinator load grows with segment count; Overlord load grows too, to a lesser degree. With very high segment counts consider separating them. They can be run as one combined service via `druid.coordinator.asOverlord.enabled`.
- With high ingestion or query load, deploy Historicals and Middle Managers on separate hosts; Historicals also benefit from free memory for memory-mapped segments.

## External dependencies

- Deep storage: shared file storage reachable by every server (S3, HDFS or network filesystem in a cluster; local disk single-server). Holds all ingested data (Historical-loaded segments are also kept there as backup), moves segments between services, and can serve queries from deep storage at some performance cost. Druid bootstraps from it even if every data server is lost. Size it for all data; size Historical disks for frequently queried data.
- Metadata storage: segment usage and task information; typically PostgreSQL or MySQL in a cluster, Derby for single-server.
- ZooKeeper: service discovery, coordination and leader election.

## Checked

2026-11-08. Read the cited architecture page in full. Extended the draft with Peon and Indexer details, colocation guidance and the external dependencies.

Method: documentation only; no commands were run.
