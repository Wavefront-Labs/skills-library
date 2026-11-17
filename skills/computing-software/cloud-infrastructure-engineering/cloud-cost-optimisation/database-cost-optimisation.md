---
id: computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.database-cost-optimisation
name: database-cost-optimisation
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-cost-optimisation
tags: [cloud-cost-optimisation, finops, cost-aware-architecture, database-cost-optimisation, rds-rightsizing, aurora-io-optimized, serverless-databases, dynamodb-capacity-modes, cosmos-db-ru, read-replica-costs, database-reserved-instances, database-rightsizing]
level: practitioner
status: draft
description: "Cut managed database cost: rightsizing, storage/IO pricing options, NoSQL capacity modes, replica and backup sprawl, serverless tiers, scheduling, reservations."
sources: ["https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/Aurora.Overview.StorageReliability.html#aurora-storage-type", "https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/capacity-mode.html", "https://learn.microsoft.com/azure/cosmos-db/optimize-cost-throughput", "https://www.finops.org/framework/capabilities/architecting-for-cloud/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Database cost optimisation

## Relational (RDS / Aurora / Azure SQL / Cloud SQL)
1. **Rightsize** on CPU, memory (freeable memory, buffer cache hit ratio) and connection
   metrics over 4+ weeks; move to Graviton/ARM instance classes where supported.
2. **Storage/IO pricing**: Aurora Standard vs **I/O-Optimized** (no per-I/O charges, higher
   instance/storage price; worth it when I/O > ~25% of the Aurora bill). RDS gp3 storage over gp2/io1.
3. **Replicas**: count read replicas vs actual read load; cross-region replicas only where DR needs them.
4. **Non-prod**: stop dev/test instances out of hours (RDS stops for up to 7 days, then auto-starts);
   Aurora Serverless v2 or Azure SQL serverless (auto-pause) for intermittent use.
5. **Backups**: retention aligned to policy; manual snapshots cleaned up.
6. **Reservations** for steady prod instances (RDS RIs / Azure reserved capacity / Cloud SQL CUDs).
7. Licensing: SQL Server/Oracle licence-included is expensive — edition downgrades, BYOL, or migrate engines.

## NoSQL
- DynamoDB: on-demand for spiky/unknown; provisioned + autoscaling (+ reserved capacity) for
  steady; Standard-IA table class for storage-heavy, rarely read tables; TTL to expire data.
- Cosmos DB: autoscale vs manual RU/s; serverless for low traffic; index only needed paths;
  partition key avoiding hot partitions (wasted RU).

## Verify
- [ ] Top 10 databases by cost reviewed with utilisation evidence.
- [ ] Non-prod databases have schedules or serverless tiers.
