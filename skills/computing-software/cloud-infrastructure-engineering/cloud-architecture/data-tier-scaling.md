---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.data-tier-scaling
name: data-tier-scaling
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, scalability, data-tier-scaling, vertical-scaling, read-scaling, write-scaling, database-partitioning, caching-tier]
level: advanced
status: draft
description: "Scale the data tier in the right order: query and index fixes, vertical scaling, caching, read replicas, functional partitioning, then sharding or distributed SQL."
sources: ["https://learn.microsoft.com/azure/architecture/best-practices/data-partitioning", "https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_ReadRepl.html", "https://cloud.google.com/spanner/docs/schema-design"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Scaling the data tier

## Ladder (cheapest first)
1. **Fix queries**: missing indexes, N+1 queries, unbounded scans, lock contention. Use slow query
   logs, Performance Insights / Query Store / Query Insights.
2. **Connection management**: poolers/proxies (PgBouncer, RDS Proxy) before buying CPU.
3. **Vertical scale**: bigger instance, faster storage (provisioned IOPS). Simple, has a ceiling
   and usually needs a failover/restart.
4. **Caching**: cache-aside for hot reads; materialized views for expensive aggregates.
5. **Read replicas**: route read-only, staleness-tolerant queries; watch replica lag.
6. **Functional partitioning**: split by bounded context (orders DB vs catalogue DB).
7. **Horizontal partitioning / sharding**: by tenant or key; or adopt distributed SQL / NoSQL
   (Spanner, Aurora Limitless, Cosmos DB, DynamoDB, CockroachDB) designed for it.
8. **Archive** cold data out of the hot store.

## Write scaling specifics
Batch writes, async via queues, avoid hot keys (monotonic IDs in range-partitioned stores), reduce
secondary indexes, use append-only patterns.

## Gotchas
- Read replicas do nothing for write-bound databases.
- Sharding before exhausting simpler steps adds permanent complexity (cross-shard queries, rebalancing).
- Hot partitions from timestamp-prefixed keys.

## Verify
- [ ] Load test identifies the bottleneck resource before choosing the step.
- [ ] Capacity headroom tracked against the next ceiling.
