---
id: computing-software.software-engineering.software-architecture.space-based-architecture
name: space-based-architecture
category: computing-software
field: software-engineering
product: software-architecture
tags: [software-architecture, architecture-styles, space-based-architecture, in-memory-data-grid, data-grid, high-concurrency]
level: advanced
status: draft
description: "Recognise when space-based architecture fits (extreme, spiky concurrency), and design processing units, replicated in-memory data grids, data pumps and writers."
sources: ["https://www.oreilly.com/library/view/fundamentals-of-software/9781492043447/", "https://hazelcast.com/foundations/software-architecture/space-based-architecture/", "https://ignite.apache.org/docs/latest/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Space-based architecture

**Problem it solves:** the database is the bottleneck under huge, unpredictable concurrent load
(ticket on-sales, auctions, flash sales, online betting). Space-based architecture removes the
database from the synchronous path.

## Components (Richards & Ford)
- **Processing units**: app instances holding the code *and* an in-memory copy of the data they need
  (replicated or partitioned cache: Hazelcast, Apache Ignite, Infinispan, Redis Enterprise).
- **Virtualized middleware**: messaging grid (routes requests), data grid (replicates cache updates
  across units), processing grid (orchestrates multi-unit requests), deployment manager (scales units
  up/down with load).
- **Data pumps**: asynchronously send updates from units to the database (via queues).
- **Data writers / readers**: consume pumps and persist; readers reload caches on cold start.

## Design considerations
- Replicated cache = each unit has everything (fast, small data sets, < ~100 MB); distributed cache =
  partitioned with remote reads (bigger data, more latency, consistency easier).
- **Data collisions**: two units update the same item before replication arrives. Estimate collision
  rate ~ N * (updates/sec)^2 * replication latency / cache size; mitigate with partitioning by key
  so a given item has one owner.
- Eventual consistency to the DB: reporting and other systems read stale data; the DB is a
  backing store, not the source of truth during peaks.
- Cold start and crash recovery: unit rebuilds from peers or from the DB via readers.

## Trade-offs
High elasticity and scalability, but complex, expensive (memory), hard to test at real scale, and
poor for large data volumes or strong cross-entity transactions. Usually applied to one hot
subsystem (the bidding service), not a whole estate. Simpler alternatives first: caching, read
replicas, queue-based load levelling, sharding.
