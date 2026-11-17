---
id: computing-software.cloud-infrastructure-engineering.aws.neptune-serverless-and-read-replicas
name: neptune-serverless-and-read-replicas
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, neptune, neptune-serverless, read-replicas, graph-database, ncu]
level: advanced
status: docs-checked
description: "Run Amazon Neptune with serverless instances that scale in NCUs, mix provisioned and serverless replicas, and tune min/max capacity and failover tiers."
sources: ["https://docs.aws.amazon.com/neptune/latest/userguide/neptune-serverless.html", "https://docs.aws.amazon.com/neptune/latest/userguide/neptune-serverless-using.html", "https://docs.aws.amazon.com/neptune/latest/userguide/feature-overview-db-clusters.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Neptune Serverless and read replicas

## 1. Enable serverless capacity
```bash
aws neptune create-db-cluster --db-cluster-identifier graph --engine neptune \
  --serverless-v2-scaling-configuration MinCapacity=1.0,MaxCapacity=64 \
  --db-subnet-group-name graph-subnets --vpc-security-group-ids sg-neptune --enable-iam-database-authentication
aws neptune create-db-instance --db-instance-identifier graph-w --db-cluster-identifier graph \
  --engine neptune --db-instance-class db.serverless
```
- Capacity is in Neptune Capacity Units (NCUs, about 2 GiB of memory plus matching CPU each); each serverless instance
  scales between the cluster min and max. Lowest minimum is 1.0 NCU; highest maximum is 128 NCUs (256 GB of memory).
- A higher minimum lets instances scale up faster for a sudden jump (Neptune starts with a larger scaling increment);
  a low minimum saves money but scales up slowly from low capacity.
- Constraints on the Serverless page: engine release 1.2.0.1 or later, not compatible with the lookup cache, and available in the
  Regions it lists (check the page for your Region). An existing provisioned cluster can be converted (with some downtime).

## 2. Read replicas
- Up to 15 read-replica instances share the cluster volume; replication lag is usually well under 100 ms
  according to the Neptune User Guide.
- Mix provisioned and serverless instances in one cluster.
- Promotion tier (priority, 0 to 15) decides failover order. Serverless readers in tiers 0 and 1 scale together with the writer so
  they can take over its workload; readers in tiers 2 to 15 scale independently of the writer and each other. Keep a
  tier 0 or 1 reader in a second AZ.

## 3. Monitor
`ServerlessDatabaseCapacity`, `NCUUtilization` (current capacity divided by the cluster maximum), `BufferCacheHitRatio`,
`MainRequestQueuePendingRequests`. If `NCUUtilization` stays near 100% the instance has scaled as high as it can: raise
the maximum, or add reader instances to spread read load.

## 4. Cost
Serverless instances are charged for the resources used; pricing is not checked here (see the Neptune pricing page).
For development clusters set a low minimum.

## Verify
- [ ] Load test shows capacity rising and falling; failover to a tier-0 replica completes and the writer endpoint follows.

## Checked
Date: 2026-10-27. Sources: Neptune User Guide pages neptune-serverless (constraints), neptune-serverless-capacity-scaling
(1.0 min, 128 max, promotion tier behaviour), neptune-serverless-using (CLI example, metrics, conversion),
feature-overview-db-clusters (15 replicas, lag), cw-metrics (metric names); botocore `neptune` model
(`EnableIAMDatabaseAuthentication`, `ServerlessV2ScalingConfiguration`, `PromotionTier`). Corrected the IAM flag name
(`--enable-iam-database-authentication`), the minimum capacity (1.0, not 2.5 as an example), and the buffer cache claim;
removed the `AWS/Neptune` namespace, billing and stop-cluster claims.
Method: documentation only; no commands were run.
