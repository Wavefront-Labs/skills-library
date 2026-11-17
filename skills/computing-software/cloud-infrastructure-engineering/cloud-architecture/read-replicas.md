---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.read-replicas
name: read-replicas
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, database-selection, read-replicas, read-scaling, replication-lag, database-scaling]
level: practitioner
status: docs-checked
description: "Use read replicas for read scaling: routing reads, handling replication lag, read-your-writes, failover roles, cross-region replicas and limits."
sources: ["https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_ReadRepl.html", "https://learn.microsoft.com/azure/azure-sql/database/read-scale-out", "https://cloud.google.com/sql/docs/postgres/replication"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Read replicas and read scaling

## Steps
1. **Confirm reads are the bottleneck** (read/write ratio, top queries) before adding replicas; indexes and caching
   are other options. Replicas do not scale writes.
2. **Create replicas.** Amazon RDS takes a snapshot of the source and uses the engine's asynchronous replication.
   Replicas are billed like standard DB instances; RDS does not autoscale replicas, so create and delete them manually.
   Cloud SQL recommends 10 or fewer direct read replicas per primary, with cascading replicas (up to four levels
   including the primary) for more. Put Cloud SQL replicas in a different zone than an HA primary.
3. **Route reads.** Applications connect to an RDS replica like any DB instance. Azure SQL Database (Premium, Business
   Critical, Hyperscale with at least one secondary) routes connections with `ApplicationIntent=ReadOnly` to a
   read-only replica; the default `ReadWrite` goes to the primary. Cloud SQL does not provide load balancing between
   replicas; implement it yourself (for example with connection pooling).
4. **Handle lag.** Replication is asynchronous. Azure documents typical propagation latency from tens of milliseconds
   to single-digit seconds with no fixed upper bound, and says applications needing committed data readable
   immediately should use the primary. Route read-your-writes paths to the primary. In Azure SQL, `redo_queue_size`
   and `redo_rate` in `sys.dm_database_replica_states` indicate latency. Cloud SQL page: replication lag metrics are
   linked from its replication docs.
5. **Failover and promotion.**
   - RDS: promote a replica to a standalone instance for disaster recovery. In a Multi-AZ deployment the standby
     replicates synchronously and cannot serve reads, unlike a read replica.
   - Cloud SQL: read replicas cannot fail over; only a DR replica can be a failover target. A replica can be promoted
     for disaster recovery or corruption.
6. **Cross-region.** RDS and Cloud SQL both support cross-region replicas, for DR and for reads closer to users; Cloud
   SQL adds cross-region data transfer charges.

## Gotchas
- Azure SQL: long-running queries on a read-only replica can block redo or cleanup and may be terminated (errors 1219,
  3947, 3948 are retryable); transactions on read-only replicas always use snapshot isolation.
- RDS: a deleted source promotes its in-Region replicas to standalone instances.
- Azure SQL: only one read-only replica is accessible at a time in Premium and Business Critical; geo-replicas give
  additional read-only replicas.
- Cloud SQL: replicas have no backups of their own, cannot be stopped, and share the primary's maintenance windows.
  Do not use a replica as the source for Datastream or Kafka.

## Verify
- [ ] Lag alarm configured with a threshold matched to staleness tolerance.
- [ ] Read-after-write paths tested.

## Checked
Method: docs-only read of cited pages, 2026-11-08

Confirmed against the RDS read replica overview, Azure SQL read scale-out and Cloud SQL replication pages. Removed:
Aurora replica figures (lag under 100 ms, 15 replicas), ProxySQL/pgpool/RDS Proxy routing, `ReplicaLag` metric name,
PostgreSQL `hot_standby_feedback` and read-your-writes token techniques (not in these pages).
