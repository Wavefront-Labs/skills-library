---
id: computing-software.cloud-infrastructure-engineering.aws.aurora-clusters-serverless-global
name: aurora-clusters-serverless-global
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, aurora, aurora-postgresql, aurora-mysql, aurora-serverless, aurora-serverless-v2, global-database, cluster-endpoint, reader-endpoint, custom-endpoint, failover-priority, aurora-replicas, backtrack, fast-clone, aurora-io-optimized, acu, write-forwarding, cross-region-failover, switchover, database-activity-streams, parallel-query, rds-data-api, aurora-limitless]
level: advanced
status: docs-checked
description: "Run Aurora: endpoints, failover tiers, Serverless v2 ACU sizing, I/O-Optimized vs Standard, fast clones, backtrack, Global Database switchover and failover."
sources: ["https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/CHAP_AuroraOverview.html", "https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/Aurora.Overview.Endpoints.html", "https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/Concepts.AuroraHighAvailability.html", "https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/aurora-serverless-v2.html", "https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/aurora-global-database.html", "https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/aurora-global-database-disaster-recovery.html", "https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/Aurora.Managing.Clone.html", "https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/AuroraMySQL.Managing.Backtrack.html", "https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/Aurora.Overview.StorageReliability.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Aurora - clusters, Serverless v2 and Global Database

**Goal:** an Aurora cluster whose writer fails over to the right replica,
whose readers are used through the endpoints designed for it, whose capacity scales
with load (Serverless v2), and which can move its primary
Region when a Region fails.

## 1. What is different from RDS
Storage is a shared cluster volume with data copies across three AZs (six storage nodes) that grows automatically
(up to 256 TiB for specific engine versions; check your version). All instances in the cluster use the same volume,
so you can create up to 15 Aurora Replicas, and a replica is promoted to writer on failover (no data copy).
Billing has two storage configurations: **Aurora Standard** (instance and storage usage plus a per-million-requests I/O
charge) and **Aurora I/O-Optimized** (no read/write I/O charges). The User Guide says I/O-Optimized is the best
choice when I/O spending is 25% or more of total Aurora spending, and that you can switch from Standard to
I/O-Optimized once every 30 days (switching back is allowed at any time). Prices are not checked here.

## 2. Create a cluster
```bash
aws rds create-db-cluster --db-cluster-identifier app --engine aurora-postgresql --engine-version <ENGINE_VERSION> \
  --master-username admin --manage-master-user-password --db-subnet-group-name private --vpc-security-group-ids sg-db \
  --storage-type aurora-iopt1 --storage-encrypted --kms-key-id alias/rds-prod --backup-retention-period 14 \
  --db-cluster-parameter-group-name app-apg --deletion-protection --enable-cloudwatch-logs-exports postgresql \
  --serverless-v2-scaling-configuration MinCapacity=0.5,MaxCapacity=32
aws rds create-db-instance --db-cluster-identifier app --db-instance-identifier app-1 --engine aurora-postgresql \
  --db-instance-class db.serverless --promotion-tier 0 --enable-performance-insights
aws rds create-db-instance --db-cluster-identifier app --db-instance-identifier app-2 --engine aurora-postgresql \
  --db-instance-class db.r7g.xlarge --promotion-tier 1   # provisioned reader in another AZ
```
- Two parameter-group levels: **cluster** group (settings tied to physical layout and replication) and **instance**
  group (settings such as memory that can differ per instance); see `aurora-cluster-vs-instance-parameter-groups`.
- Put at least one reader in a **different AZ** from the writer. With one or more replicas, a replica is promoted;
  with none, the primary is recreated in the same AZ and the interruption is longer.

## 3. Endpoints and failover
| Endpoint | Points at | Use |
|---|---|---|
| Cluster (writer) | Current writer | All writes; follows failover |
| Reader | All readers; Aurora balances connections | Read-only traffic |
| Custom | A subset of instances you choose | Isolate analytics from OLTP readers |
| Instance | One instance | Diagnosis or tuning |
- **Promotion priority** 0 (highest) to 15 (lowest) decides which reader becomes the writer; replicas with the same
  priority form a tier and the largest in size is promoted, then an arbitrary one. After five unsuccessful failover
  attempts, tiers are no longer considered. Changing a priority does not trigger a failover.
- Failover: `aws rds failover-db-cluster --db-cluster-identifier app [--target-db-instance-identifier app-2]`.
  The User Guide says service is typically restored in under 60 seconds and often under 30 seconds when replicas exist;
  reads and writes fail with an exception meanwhile, so clients need retry. RDS Proxy can improve availability during failover.
- Reader endpoint balancing is per connection, so a pool that opens few long-lived connections can concentrate on one
  reader; recycle pooled connections periodically.
- **Local write forwarding** lets read/write transactions be issued on an Aurora Replica and forwarded to the writer
  (read-after-write consistency). The page read describes Aurora MySQL, version 3.04 or higher (including 8.4);
  create-db-cluster has `--enable-local-write-forwarding`. Check the Aurora PostgreSQL guide for its support.

## 4. Serverless v2
- Capacity is measured in **ACUs** (about 2 GiB of memory plus matching CPU and networking each). The range depends on the
  platform version: from 0.5 to 128 on older versions up to 0 to 256 (Aurora MySQL) or 0 to 384 (Aurora PostgreSQL) on
  recent ones (the table on the "how it works" page lists them). A minimum of 0 ACUs enables **auto-pause**
  (`SecondsUntilAutoPause`) on versions that support it. Scaling steps are as small as 0.5 ACU, larger at higher capacity,
  and can happen while connections and transactions are open.
- Choose `MinCapacity` so that your working set stays in the buffer cache after scale-down; `MaxCapacity` is the
  budget cap.
- `db.serverless` instances can mix with provisioned instances in one cluster (a serverless reader's minimum capacity
  is tied to the writer when the writer is provisioned: see the how-it-works page).
- `ServerlessDatabaseCapacity` and `ACUUtilization` are the metrics to watch; `ACUUtilization` at 100% means the
  instance is at its maximum capacity.

## 5. Clones and backtrack
- **Fast clone** (`restore-db-cluster-to-point-in-time --restore-type copy-on-write --use-latest-restorable-time --source-db-cluster-identifier app --db-cluster-identifier app-clone`):
  uses a copy-on-write protocol so a clone needs minimal additional storage until data diverges. Up to 15 copy-on-write
  clones; the next clone is a full copy. Cross-account cloning uses AWS RAM. Clones are useful for load tests and migration
  rehearsal. Add instances to the restored cluster; it has none.
- **Backtrack** (Aurora MySQL versions 2, 3 and 8.4 only; `--backtrack-window` in seconds at creation, maximum window
  72 hours): rewind the cluster in place without restoring from a backup. Aurora Global Database does not support
  backtracking.
- A PITR restore creates a new cluster and you add instances; pass parameter groups and security groups explicitly.

## 6. Global Database
```bash
aws rds create-global-cluster --global-cluster-identifier app-global --source-db-cluster-identifier arn:aws:rds:eu-west-1:<ACCOUNT_ID>:cluster:app
aws rds create-db-cluster --region us-east-1 --db-cluster-identifier app-us --engine aurora-postgresql --engine-version <ENGINE_VERSION> \
  --global-cluster-identifier app-global --db-subnet-group-name private --vpc-security-group-ids sg-db --kms-key-id <US_KEY>
aws rds create-db-instance --region us-east-1 --db-cluster-identifier app-us --db-instance-identifier app-us-1 --engine aurora-postgresql --db-instance-class db.r7g.xlarge
```
- Replication uses dedicated infrastructure with latency typically under a second; one primary Region plus up to 10
  read-only secondary Regions; each secondary cluster supports up to 16 read-only Aurora Replicas. Secondary clusters
  are read-only; writes can be forwarded with **global write forwarding**.
- **Switchover** (`switchover-global-cluster --global-cluster-identifier app-global --target-db-cluster-identifier <TARGET_CLUSTER_ARN>`):
  planned, no data loss; use for drills and Region moves. **Failover** (`failover-global-cluster
  --global-cluster-identifier app-global --target-db-cluster-identifier <TARGET_CLUSTER_ARN> --allow-data-loss`):
  unplanned; data not yet replicated can be lost, so watch the `AuroraGlobalDBRPOLag` metric (version-dependent).
  After a failover, the remaining clusters must be detached/recreated per the DR page.
- On Aurora PostgreSQL the `rds.global_db_rpo` parameter sets a recovery point objective for the global database; read
  the DR page for how it behaves before relying on it.
- Not supported on global databases: backtracking; automatic minor version upgrade has no effect; Aurora Auto Scaling
  for secondary clusters.
- Each Region has its own KMS key, parameter groups, subnet group and endpoints; applications must switch Region
  endpoints on failover (the User Guide does not describe a global DNS name for a global database; implement
  routing yourself, for example with Route 53).

## 7. Operate
- Watch cluster metrics for volume usage, I/O, `AuroraReplicaLag`, `DatabaseConnections` and
  `ServerlessDatabaseCapacity`.
- Major version upgrades can use blue/green deployments or an in-place upgrade with a snapshot first (check the
  limitations page for your engine and cluster type, including Global Database).
- Database Activity Streams for auditing; Performance Insights on each instance.

## Gotchas
- Readers are **not** a backup: a dropped table is replicated everywhere. Backups/PITR/clones are the recovery path.
- `MaxCapacity` too low on the writer leaves `ACUUtilization` at 100% and latency climbs; too low `MinCapacity` means a cold cache after scale-down.
- Auto-pause availability per engine version and Aurora Limitless Database scope are not checked here.

## Verify
- [ ] `failover-db-cluster` lands on the intended highest-priority reader and the app recovers with retries.
- [ ] Reader endpoint connections spread across readers (check `DatabaseConnections` per instance).
- [ ] Serverless v2: `ServerlessDatabaseCapacity` tracks load; `ACUUtilization` has headroom; buffer cache hit ratio is acceptable after scale-down.
- [ ] A fast clone of production completes and runs the migration rehearsal.
- [ ] Global Database switchover drill completes with no data loss; `AuroraGlobalDBRPOLag` is steady; app repointed via the documented mechanism.

## Checked
Date: 2026-10-27. Sources: Aurora User Guide pages Concepts.AuroraHighAvailability (60 s/30 s, promotion priorities),
Aurora.Overview.StorageReliability (256 TiB, three AZs), Aurora storage configuration text (25% rule, 30-day switch),
aurora-serverless-v2.how-it-works (ACU ranges, auto-pause), aurora-global-database and
aurora-global-database-disaster-recovery (10 secondary Regions, 16 readers, switchover and failover commands,
unsupported features), Aurora.Managing.Clone, AuroraMySQL.Managing.Backtrack (72 hours, supported versions),
aurora-mysql-write-forwarding; botocore `rds` model (create-db-cluster, ServerlessV2ScalingConfiguration,
FailoverGlobalCluster requires a target). Corrected: up to 10 secondary Regions (not 5); Aurora Auto Scaling is not
supported for global database secondaries; failover-global-cluster needs a target cluster; backtrack is not
supported with Global Database; promotion tier ties go to the largest instance. Removed pricing premiums, replica
lag and failover timings, DNS TTL and driver timing figures, cost claims and Serverless v1 statements.
Method: documentation only; no commands were run.
