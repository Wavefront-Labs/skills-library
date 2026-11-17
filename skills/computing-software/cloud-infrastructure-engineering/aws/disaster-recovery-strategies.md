---
id: computing-software.cloud-infrastructure-engineering.aws.disaster-recovery-strategies
name: disaster-recovery-strategies
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, disaster-recovery, dr, pilot-light, warm-standby, backup-and-restore, multi-site-active-active, rto, rpo, route53-failover, aurora-global-database, dynamodb-global-tables, s3-cross-region-replication, aws-backup, cross-region, dr-runbook, dr-testing, failover, failback, multi-region-data, data-replication-strategy]
level: practitioner
status: docs-checked
description: "Pick and build an AWS DR tier against RTO/RPO: backup-and-restore, pilot light, warm standby or active-active, with matching data replication, DNS failover and tested runbooks."
sources: ["https://docs.aws.amazon.com/whitepapers/latest/disaster-recovery-workloads-on-aws/disaster-recovery-options-in-the-cloud.html", "https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/aurora-global-database.html", "https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/dns-failover.html", "https://docs.aws.amazon.com/r53recovery/latest/dg/routing-control.html"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Disaster recovery strategies on AWS — match the tier to the RTO/RPO, then prove it

**Goal:** a DR design whose cost matches the business's actual recovery objectives, whose
data replication meets the RPO, and whose failover has been executed — not just documented.
(Business-side objectives: `computing-software.cloud-infrastructure-engineering.cloud-architecture.disaster-recovery-planning`.)

## 1. The four tiers
| Strategy | Recovery point is set by | What runs in DR region |
|---|---|---|
| **Backup & restore** | backup frequency | Nothing; backups copied cross-region; IaC redeploys |
| **Pilot light** | continuous replication plus point-in-time backups | Data layer live (replicas), app layer defined but scaled to 0 |
| **Warm standby** | continuous replication | Full stack at reduced capacity, takes traffic after scale-up |
| **Multi-site active-active** | continuous replication | Full capacity in both; traffic split; needs data conflict strategy |
RTO and RPO targets, and cost, rise with the tier: take the numbers from your own game-day measurements.
Pick per *workload*, not per company; most estates have one or two tier-1 systems and many
backup-and-restore ones. A region-level DR is rarely justified before multi-AZ is solid
(`computing-software.cloud-infrastructure-engineering.cloud-architecture.multi-region-high-availability-design`).

## 2. Data layer per tier
- The whitepaper lists these as continuous, cross-Region, asynchronous replication: **S3 Replication**
  (monitor with S3 Replication Time Control), **RDS read replicas**, **Aurora global databases**,
  **DynamoDB global tables**, **DocumentDB global clusters** and **ElastiCache (Redis OSS) Global Datastore**.
- **RDS**: a **cross-region read replica** is asynchronous; promote it on failover and plan how to
  re-establish replication for failback.
- **Aurora Global Database**: use **switchover** (previously "managed planned failover", no data
  loss) for planned moves of the primary Region, and **failover** to recover after an outage of
  the primary Region (`failover-global-cluster`, with `--allow-data-loss` for an unplanned one).
  **Write forwarding** lets secondary clusters send writes to the primary.
- **AWS Backup** and snapshot copies are the backbone of backup & restore; AMIs are copied with `copy-image`.
  Back up code and configuration too, including AMIs.

## 3. Traffic layer
- **Route 53 failover records** with health checks on the primary. A health check can monitor a
  resource, the status of other health checks (calculated), or the status of a CloudWatch alarm:
  use the latter two so a partial failure (DB down, app up) fails over too.
- **Application Recovery Controller** (ARC) *routing controls* are grouped on control panels in an ARC
  cluster, which is a data plane of endpoints in five Regions; ARC recommends updating routing
  control states with the CLI or API. Routing control health checks plug into DNS failover records.
- **Global Accelerator** with endpoint groups in both regions for non-DNS failover.
- Prefer **failing over to a region that is already live** (active-active) over cold starts of control-plane-heavy stacks.

## 4. App layer by tier
- Backup & restore: IaC (CloudFormation/CDK) that can deploy the whole stack to
  any region with region-agnostic parameters; AMIs/images replicated (ECR replication);
  secrets and parameters copied.
- Pilot light: everything above *deployed* — ASGs at 0, ECS services desired 0, Lambda already
  there; failover = scale up + promote data + flip DNS.
- Warm standby: same, with min capacity > 0 and continuous synthetic traffic to prove it works.
- Active-active: stateless services behind global routing; data via global tables / Global
  Database write forwarding; idempotent writes; per-region queues.

## 5. Runbook and testing
1. Declare (who, criteria, agreed in advance).
2. Promote data (Aurora `failover-global-cluster`; RDS `promote-read-replica`; DynamoDB nothing).
3. Scale app (`set-desired-capacity`, `update-service --desired-count`).
4. Flip traffic (ARC routing control `update-routing-control-state` or Route 53 record).
5. Verify with synthetic transactions; announce.
6. **Failback** plan: re-establish replication in the opposite direction before switching back; most data stores need a rebuild.
- Test quarterly with a **game day**: at minimum a read-only region failover for a tier-1 app;
  measure actual RTO/RPO and record the delta vs target. Use AWS FIS to inject the failure.
- Control-plane dependency check: your runbook must not require IAM/Route 53/S3 control
  plane calls in the failed region. Pre-create everything; use ARC for the switch.

## Gotchas
- "Multi-AZ" is not DR; AZ failure is handled by AZ redundancy, region failure needs this.
- Service quotas are per region — the DR region often cannot scale to production size until
  quotas are raised (ARC readiness checks catch this).
- KMS keys are regional: use **multi-Region keys** or re-encrypt; snapshots encrypted with a
  single-region key cannot be used elsewhere.
- Aurora Global DB unplanned failover is a *detach-and-promote*: the old primary must be re-added as secondary afterwards.
- DNS TTLs honoured by clients/ISPs vary; some resolvers ignore low TTLs — keep ARC/Global Accelerator in mind.
- Aurora Global Database switchover has minimum engine versions (for example Aurora MySQL 5.7-compatible needs 2.09.1 or higher); check the docs for yours.
- Costs: see the pricing pages; size the DR region from measured need.

## Verify
- [ ] Documented RTO/RPO per workload and the chosen tier written next to it.
- [ ] Replication lag metrics for each data store are alarmed below the RPO.
- [ ] A game day in the last quarter achieved RTO within target; the report lists gaps.
- [ ] Quotas in the DR region match production (ARC readiness or a quota diff script).
- [ ] DNS/ARC failover executed from an account that does not depend on the failed region's control plane.

## Checked
2026-10-31. Confirmed in the AWS DR whitepaper (DR options), the Aurora global database page, the Route 53 health checks page, the ARC routing control page and the botocore rds model: tier definitions and the list of cross-Region asynchronous replication services, S3 RTC for monitoring, Aurora switchover (formerly managed planned failover) versus failover, write forwarding, `FailoverGlobalCluster` `AllowDataLoss`, Route 53 health check types, ARC routing control structure. Removed as unconfirmed: the numeric RTO/RPO/cost columns and the 20-40 percent cost figure, the 15-minute RTC SLA, sub-second Aurora lag, DynamoDB conflict-resolution and lag figures, AWS Backup service coverage list, TTL advice, S3 delete-marker advice, and the 15-minute declaration criteria.
Method: documentation only; no commands were run.
