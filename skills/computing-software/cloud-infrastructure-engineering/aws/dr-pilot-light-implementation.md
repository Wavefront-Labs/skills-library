---
id: computing-software.cloud-infrastructure-engineering.aws.dr-pilot-light-implementation
name: dr-pilot-light-implementation
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, disaster-recovery, pilot-light, pilot-light-implementation, pilot-light-design, aurora-global-database, ami-copy, ecr-replication, asg-zero, cross-region, rto, rpo]
level: advanced
status: docs-checked
description: "Build a pilot-light DR Region on AWS: continuously replicated data, deployed but switched-off compute, replicated images, and a scripted activation that fits the RTO."
sources:
  - https://docs.aws.amazon.com/whitepapers/latest/disaster-recovery-workloads-on-aws/disaster-recovery-options-in-the-cloud.html
  - https://aws.amazon.com/blogs/architecture/disaster-recovery-dr-architecture-on-aws-part-iii-pilot-light-and-warm-standby/
  - https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/aurora-global-database.html
  - https://docs.aws.amazon.com/AmazonECR/latest/userguide/replication.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Pilot light DR — implementation

**Goal:** replicate data to the DR Region continuously, provision a copy of the core infrastructure there, keep application servers loaded with code and configuration but switched off, and make switching on a scripted, tested operation. Unlike backup and restore, the core infrastructure is always available.

## 1. What is on and what is off
| Layer | In the DR Region |
|---|---|
| Relational DB | Aurora global database secondary cluster, or an RDS cross-Region read replica |
| NoSQL | DynamoDB global table replica |
| Objects | S3 replication (S3 Replication Time Control to monitor replication times) |
| Images | ECR private replication rules; golden AMIs built by an Image Builder pipeline and copied to both Regions |
| Network | VPC with subnets and routing, Elastic Load Balancing, Auto Scaling groups deployed |
| Compute | Auto Scaling group configured but with no instances; the scale-out is scripted |
| Traffic | Route 53 records and health checks, or Application Recovery Controller (ARC) routing controls, set up before the event |

- Deploy with infrastructure as code: full infrastructure in the primary Region and a scaled-down or switched-off version in the DR Region, using CloudFormation conditions on pseudo parameters (or equivalent). Workload changes must reach both Regions simultaneously.
- The whitepaper recommends a different account per Region for the highest resource and security isolation.
- Replication does not protect against corruption or deletion on its own: also keep point-in-time backups (and S3 versioning) in the DR Region.
- Best practice for "switched off" is to not deploy the resource and keep the configuration to deploy it when needed; the blog's example keeps the Auto Scaling group but sets `MinSize` and `DesiredCapacity` to 0 through a CloudFormation `ActiveOrPassive` parameter and flips it to active on failover.

## 2. Aurora global database
An Aurora global database has one primary Region for writes and up to 10 read-only secondary Regions. Replication uses the cluster storage volume, typically under a second of latency. The writer endpoint keeps pointing at the primary cluster after a switchover or failover. You can add reader instances to a secondary cluster.
```bash
aws rds create-global-cluster --global-cluster-identifier app-global --source-db-cluster-identifier <PRIMARY_ARN>
aws rds create-db-cluster --region <DR_REGION> --db-cluster-identifier app-dr \
  --global-cluster-identifier app-global --engine aurora-postgresql --engine-version <SAME_AS_PRIMARY> \
  --db-subnet-group-name <DR_SUBNET_GROUP> --vpc-security-group-ids <SG_ID> --kms-key-id <DR_KEY>
```
- Use switchover for planned moves of a healthy global database (no data loss) and failover to recover after a primary-Region outage; the whitepaper says a secondary can be promoted in under a minute. Commands: `aws rds switchover-global-cluster` and `aws rds failover-global-cluster --global-cluster-identifier app-global --target-db-cluster-identifier <DR_CLUSTER_ARN>`.
- Managed switchover and failover need the same major and minor engine version in primary and secondary (patch levels may also need to match; otherwise fail over manually). Create secondaries with the same engine version as the primary.
- For RDS read replicas other than Aurora, promotion takes a few minutes and includes a reboot.

## 3. Activation runbook (script it)
1. Decide to fail over. Automatic failover on health checks should be used with caution (false alarms cost availability and data); manual initiation with the steps automated "like the push of a button" is common.
2. Data: promote the replica or fail over the global database.
3. Compute: script scale-up of desired counts (Auto Scaling group capacity, ECS tasks, Lambda concurrency) from the CLI or SDK.
4. Traffic: ARC routing controls (Route 53 health checks used as on/off switches, driven through a data plane API) or Route 53 health-check failover; weighted-record changes are a control plane operation and less resilient. Global Accelerator traffic dials are also control plane.
5. Verify with synthetic transactions.
Prefer data plane operations for failover; Auto Scaling is a control plane activity, so scaling from zero adds a dependency. Measure each step in drills; the sum must fit the RTO.

## 4. Gotchas
- Raise service quotas in the DR Region so scale-out is not limited.
- ECR replication: only content pushed or restored after replication is configured is replicated (use replication backfill for older images); the repository name is unchanged; repository policies and lifecycle policies are not replicated (repository creation templates can carry settings); cross-account replication needs a registry permissions policy on the destination.
- If pilot light's scale-out and provisioning time misses the RTO, move to warm standby (`computing-software.cloud-infrastructure-engineering.aws.dr-warm-standby-implementation`).

## Verify
- [ ] Replication monitoring in place: S3 RTC, and Aurora RPO lag monitoring for secondary clusters.
- [ ] Deployed DR infrastructure matches the primary's template versions.
- [ ] Regular activation drill completes within RTO, with timings recorded per step.
- [ ] DR Region service quotas allow production capacity.

## Checked

Method: docs-only read of cited pages, 2026-11-08

Confirmed against the AWS DR whitepaper (pilot light, services, traffic management, Auto Scaling sections), the Architecture Blog pilot light and warm standby post, the Aurora Global Database overview page and the ECR private image replication page. CLI commands checked against the botocore model. Removed as not stated by the pages: headless (instance-less) secondary clusters and the `--allow-data-loss` recipe, Secrets Manager replica secrets, Parameter Store copying, KMS multi-Region key advice, ECS/Lambda zero-cost claims, RPO/RTO figures, On-Demand Capacity Reservation and SSM alias advice, and the DynamoDB ReplicationLatency alarm.
