---
id: computing-software.cloud-infrastructure-engineering.aws.rds-cross-region-read-replicas-and-promotion
name: rds-cross-region-read-replicas-and-promotion
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, rds, cross-region-read-replica, replica-promotion, disaster-recovery, replica-lag, kms]
level: practitioner
status: docs-checked
description: "Create RDS cross-region read replicas (KMS, lag monitoring) and promote one to a standalone primary during a regional DR event, then rebuild the reverse path."
sources: ["https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_ReadRepl.XRgn.html", "https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_ReadRepl.Promote.html", "https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_ReadRepl.Monitoring.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# RDS cross-region read replicas and promotion

Applies to RDS for Db2, MariaDB, MySQL, Oracle, PostgreSQL and SQL Server (engine and Region
availability varies). Aurora uses Global Database instead.

## 1. Create
Run in the **destination** region, referencing the source ARN:
```bash
aws rds create-db-instance-read-replica --region eu-west-1 \
  --db-instance-identifier orders-dr --source-db-instance-identifier arn:aws:rds:us-east-1:<ACCOUNT_ID>:db:orders \
  --db-instance-class db.r7g.xlarge --kms-key-id arn:aws:kms:eu-west-1:<ACCOUNT_ID>:key/... \
  --db-subnet-group-name dr-db-subnets --vpc-security-group-ids sg-dr-db --multi-az
```
- Encrypted source → you must give a KMS key **in the destination region**.
- Source needs automated backups enabled (retention > 0).
- Replication is asynchronous; cross-region transfer charges apply.
- Replica can be Multi-AZ so the promoted primary is immediately HA.

## 2. Monitor
`ReplicaLag` (seconds) on the replica; alarm well below your RPO. Also watch source
`TransactionLogsDiskUsage`/`OldestReplicationSlotLag` (PostgreSQL): a broken replica holds WAL
on the source and fills its disk.

## 3. Promote (DR)
```bash
aws rds promote-read-replica --region eu-west-1 --db-instance-identifier orders-dr \
  --backup-retention-period 7
aws rds wait db-instance-available --region eu-west-1 --db-instance-identifier orders-dr
```
- Promotion is **one-way**: the replica becomes a standalone writable instance (reboot
  before it becomes available). Replication from the old source stops for good.
- Point applications at it (Route 53 CNAME with low TTL, or config/secret update).
- Data written to the old primary but not yet replicated is lost (RPO = lag at failure).

## 4. After the event
Old region recovers → create a new cross-region replica **from the promoted instance** back
to the original region; fail back later with the same promotion process during a maintenance window.

## Gotchas
- RDS cannot guarantee more than five cross-Region replicas per source (VPC ACL entry limit); up to 20 concurrent
  create requests per destination Region per account.
- Db2, SQL Server, Oracle and PostgreSQL below 14.1 cannot create a cross-Region replica from a source that is itself a replica.
- If the source of a cross-Region PostgreSQL replica is deleted, the replica is not promoted (status `terminated`);
  for Db2, MariaDB, SQL Server, MySQL and Oracle it is promoted automatically.
- By default the replica uses the default security group (pass `--vpc-security-group-ids` to override); a custom subnet group must be in the same VPC. For
  Db2 a custom parameter group is required on the replica.
- The requesting IAM policy needs access to both Regions and both instances (conditions such as `aws:RequestedRegion` limited to one Region fail).
- Parameter/option groups are regional — pre-create equivalents in the DR region.
- Secrets Manager secret for the DB should be replicated to the DR region, with the promoted endpoint.

## Verify
- [ ] `ReplicaLag` alarm exists and lag is consistently seconds at peak.
- [ ] DR drill on a test copy: promote, app connects, write succeeds, time recorded vs RTO.
- [ ] DR-region parameter groups, subnet group, SGs and secrets exist in IaC.

## Checked
Date: 2026-10-27. Sources: RDS User Guide pages USER_ReadRepl.XRgn, USER_ReadRepl.Create, USER_ReadRepl.Promote,
USER_ReadRepl.Monitoring and rds-metrics; botocore `rds` model (CreateDBInstanceReadReplica: `MultiAZ`,
`DBSubnetGroupName`, `VpcSecurityGroupIds`, `KmsKeyId`; PromoteReadReplica `BackupRetentionPeriod`). Confirmed the
destination-Region invocation, encrypted-source requirement, backup retention prerequisite, promotion reboot, the
`ReplicaLag`, `OldestReplicationSlotLag` and `TransactionLogsDiskUsage` metric names, and the replica limits listed.
Method: documentation only; no commands were run.
