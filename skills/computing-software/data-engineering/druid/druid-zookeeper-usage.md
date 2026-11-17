---
id: computing-software.data-engineering.druid.druid-zookeeper-usage
name: druid-zookeeper-usage
category: computing-software
field: data-engineering
product: druid
tags: [zookeeper, leader-election, curator, service-discovery]
level: practitioner
status: docs-checked
description: "List what Druid still uses ZooKeeper for and what moved to HTTP."
sources:
  - https://github.com/apache/druid/blob/master/docs/design/zookeeper.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Druid uses Apache ZooKeeper to manage current cluster state. It supports all stable ZooKeeper versions.

The operations that happen over ZooKeeper are:
1. Coordinator leader election.
2. Overlord leader election.
3. Service (node) announcement and discovery, where services announce their presence so others can find them.

Segment loading, segment discovery and Overlord to Middle Manager task management no longer use ZooKeeper; they are served over HTTP. This matters when sizing or debugging ZooKeeper, because load on it comes from membership and elections rather than from segment traffic.

Both elections use the Curator LeaderLatch recipe. The Coordinator election happens at the path `${druid.zk.paths.coordinatorPath}/_COORDINATOR`, and the Overlord uses the same recipe at `${druid.zk.paths.overlordPath}/_OVERLORD`.

Each service announces a DruidNode record (host, port, role, services) at `${druid.zk.paths.base}/internal-discovery/${nodeRole}/${druid.host}`. Brokers and Coordinators use this path to find Historicals, Peons and Indexers, then poll each service's HTTP `/druid-internal/v1/segments` endpoint for the segments it serves.

Druid supports all stable ZooKeeper versions, so there is no pinned minimum release to track; the docs point to the ZooKeeper releases page for which versions are stable. Curator is the client library behind the LeaderLatch recipe used for both the Coordinator and the Overlord elections.

## Checked

2026-11-08. Read design/zookeeper.md in full. Replaced a vague Overlord path description with the documented path and added the internal-discovery path.

Method: documentation only; no commands were run.
