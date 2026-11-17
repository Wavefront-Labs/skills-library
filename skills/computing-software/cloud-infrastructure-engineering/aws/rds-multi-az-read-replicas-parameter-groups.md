---
id: computing-software.cloud-infrastructure-engineering.aws.rds-multi-az-read-replicas-parameter-groups
name: rds-multi-az-read-replicas-parameter-groups
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, rds, multi-az, multi-az-cluster, read-replica, read-replicas, parameter-group, option-group, failover, postgresql, mysql, rds-snapshots, automated-backups, point-in-time-recovery, pitr, storage-autoscaling, performance-insights, enhanced-monitoring, blue-green-deployment, major-version-upgrade, maintenance-window, iam-database-authentication, rds-storage, gp3]
level: practitioner
status: docs-checked
description: "Operate Amazon RDS: Multi-AZ instance vs cluster, read replicas, parameter and option groups, backups and PITR, storage sizing, and blue/green upgrades."
sources: ["https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Concepts.MultiAZ.html", "https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_ReadRepl.html", "https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_WorkingWithParamGroups.html", "https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_PIT.html", "https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/blue-green-deployments.html", "https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_Storage.html", "https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_PerfInsights.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# RDS operations — Multi-AZ, read replicas, parameter groups

**Goal:** an RDS instance that survives an AZ failure, offloads reads
to replicas without lag surprises, has every engine setting under version control, and
can be restored to a point in time within the retention period or upgraded with a verified rollback.

## 1. Availability topologies
| | Multi-AZ DB **instance** | Multi-AZ DB **cluster** (MySQL/PostgreSQL) | Single-AZ + read replica |
|---|---|---|---|
| Standby | 1 synchronous standby, not readable | 2 readable replicas, semisynchronous, three AZs | Async replica, readable |
| Failover | Typically 60-120 s (can be longer after large transactions); DNS record of the same endpoint changes | Time depends on replica lag of the readers; writer/reader endpoints | Manual promote, new endpoint |
| Use | Default for production | Lower-RTO plus readable replicas | Dev, or read scaling on a budget |
```bash
aws rds create-db-instance --db-instance-identifier app-db --engine postgres --engine-version <ENGINE_VERSION> \
  --db-instance-class db.r6g.large --multi-az --storage-type gp3 --allocated-storage 200 --max-allocated-storage 1000 \
  --master-username admin --manage-master-user-password --db-subnet-group-name private --vpc-security-group-ids sg-db \
  --backup-retention-period 14 --preferred-backup-window 02:00-03:00 --preferred-maintenance-window sun:03:30-sun:04:30 \
  --enable-performance-insights --performance-insights-retention-period 7 --monitoring-interval 60 --monitoring-role-arn <ROLE> \
  --enable-iam-database-authentication --storage-encrypted --kms-key-id alias/rds-prod --deletion-protection \
  --db-parameter-group-name app-pg16 --copy-tags-to-snapshot --auto-minor-version-upgrade
```
- Multi-AZ instance failover changes the **DNS record** of the DB endpoint: clients must reconnect on error and
  re-resolve DNS. The User Guide recommends a JVM DNS TTL (`networkaddress.cache.ttl`) of no more than 60 seconds.
  Test with `reboot-db-instance --force-failover`.
- `--manage-master-user-password` stores the password in Secrets Manager with rotation (see
  `rds-managed-master-user-password` for limitations).
- Storage: **gp3** baseline is 3,000 IOPS and 125 MiB/s; for MySQL, MariaDB, PostgreSQL and Db2 volumes of 400 GiB or more
  (striped) the baseline is 12,000 IOPS and 500 MiB/s with provisioning up to 64,000 IOPS and 4,000 MiB/s (other
  engines differ: check the storage page). io2 Block Express goes up to 256,000 IOPS. Storage autoscaling
  (`--max-allocated-storage`) only grows; allocated storage cannot be reduced without migrating to a new instance.

## 2. Read replicas
```bash
aws rds create-db-instance-read-replica --db-instance-identifier app-db-ro1 --source-db-instance-identifier app-db \
  --db-instance-class db.r6g.large --multi-az   # replica can itself be Multi-AZ
aws rds create-db-instance-read-replica --db-instance-identifier app-db-eu --source-db-instance-identifier arn:aws:rds:us-east-1:<ACCOUNT_ID>:db:app-db --region eu-west-1 --kms-key-id <EU_KEY>   # cross-region
aws rds promote-read-replica --db-instance-identifier app-db-ro1   # becomes standalone, replication stops permanently
```
- Async; lag visible as `ReplicaLag` (seconds).
- Quota "Read replicas per primary": 15 per supported Region, adjustable except for Aurora (RDS quotas page, read
  2026-10-27); for RDS for Oracle the page recommends limiting replicas to 5 to minimise lag.
- Source needs a backup retention period above 0. Heavy writes + small replica class = runaway lag; the console
  guidance is to use the same or larger instance class and storage type for the replica.
- Cross-region replicas are the DR tier (see `rds-cross-region-read-replicas-and-promotion`); RPO is the lag.
- A replica gets its own parameter group (the default group unless you name one); manage replica groups
  deliberately so they stay aligned with the source.

## 3. Parameter and option groups
```bash
aws rds create-db-parameter-group --db-parameter-group-name app-pg16 --db-parameter-group-family postgres16 --description "app prod"
aws rds modify-db-parameter-group --db-parameter-group-name app-pg16 --parameters \
  "ParameterName=log_min_duration_statement,ParameterValue=500,ApplyMethod=immediate" \
  "ParameterName=shared_preload_libraries,ParameterValue=pg_stat_statements,ApplyMethod=pending-reboot" \
  "ParameterName=max_connections,ParameterValue=250,ApplyMethod=pending-reboot"   # example value, size for your workload
aws rds describe-db-instances --db-instance-identifier app-db --query 'DBInstances[0].DBParameterGroups'   # ParameterApplyStatus
```
- **You cannot change values in a default parameter group.** Create a custom group per
  engine-major and environment.
- **Dynamic** parameter changes apply to the instance immediately without a reboot; **static** ones are applied only
  after the instance is rebooted (status `pending-reboot`). In `modify-db-parameter-group` the `ApplyMethod` values are
  `immediate` and `pending-reboot`.
- Parameter values can be formulas (for example based on `DBInstanceClassMemory`) that scale with the instance
  class; keep engine-default formulas for sizing parameters unless you have measured.
- Worth setting: PostgreSQL `log_min_duration_statement`, `pg_stat_statements` in `shared_preload_libraries`,
  `rds.force_ssl` (default 1 from PostgreSQL 15, 0 for 14 and older); MySQL `slow_query_log=1`.
- **Option groups** add engine features (for example `MARIADB_AUDIT_PLUGIN` on MySQL). Check the engine page for the
  options available and whether a change applies immediately.
- A new engine major version needs a parameter group of the new family (blue/green takes
  `--target-db-parameter-group-name`).

## 4. Backups and PITR
- Automated backups: daily snapshot + transaction logs uploaded to S3 every five minutes → restore to a point in
  time within the retention period (0 to 35 days):
  `aws rds restore-db-instance-to-point-in-time --source-db-instance-identifier app-db --target-db-instance-identifier app-db-pitr --restore-time 2026-10-14T09:12:00Z --use-latest-restorable-time`
  (one or the other flag). A restore always creates a **new instance** with a new endpoint; by default it uses the
  default VPC security group, so pass `--vpc-security-group-ids` (and `--db-parameter-group-name`) explicitly.
- Share a manual snapshot cross-account with `modify-db-snapshot-attribute --values-to-add <ACCOUNT_ID>`; an
  encrypted snapshot must use a customer managed key (see `rds-encrypting-unencrypted-instances-and-sharing-snapshots`);
  copy cross-region for DR (`copy-db-snapshot --kms-key-id` with a key in the target region).
- During the backup window storage I/O may be suspended briefly; for MariaDB, MySQL, Oracle and PostgreSQL Multi-AZ
  the backup is taken from the standby, while SQL Server (and Db2) still suspend I/O briefly.
- Deleting an instance: `--final-db-snapshot-identifier` or `--skip-final-snapshot`; see
  `describe-db-instance-automated-backups` for backups kept after deletion.

## 5. Upgrades and schema changes without fear: blue/green
```bash
aws rds create-blue-green-deployment --blue-green-deployment-name pg16-to-17 --source arn:aws:rds:...:db:app-db \
  --target-engine-version <TARGET_VERSION> --target-db-parameter-group-name app-pg17 --target-db-instance-class db.r6g.xlarge
# green is a replicated copy; test it, then:
aws rds switchover-blue-green-deployment --blue-green-deployment-identifier <ID> --switchover-timeout 300
```
Switchover renames the environments, so the production hostname points at the former green; the old blue instance is
renamed with an `-old<n>` suffix and kept. The switchover timeout is 30 to 3,600 seconds (default 300); on timeout
changes are rolled back. Limitations differ by engine and replication method; for PostgreSQL with logical replication
the docs list: DDL is not replicated (RDS may break the green environment), large objects are not replicated, and
tables need a primary key (or `REPLICA IDENTITY FULL`). The new production instance's PITR window restarts, so keep
blue until your recovery window is covered. Check the "blue/green limitations" page for your engine.
Otherwise `modify-db-instance --engine-version <TARGET_VERSION> --allow-major-version-upgrade --apply-immediately`
upgrades in place and takes the instance offline during the upgrade; snapshot first.

## 6. Monitoring
Performance Insights (`DBLoad` vs vCPUs, top SQL/waits), Enhanced Monitoring (OS-level; `--monitoring-interval`),
CloudWatch `CPUUtilization`, `FreeableMemory`, `FreeStorageSpace`, `ReadIOPS`/`WriteIOPS` vs provisioned,
`DatabaseConnections` vs `max_connections`, `ReplicaLag`, `DiskQueueDepth`. RDS events (`create-event-subscription`)
for failover, low storage, maintenance (see `rds-event-notifications-and-log-export`).

## Gotchas
- `FreeStorageSpace` hitting zero stops writes. Storage autoscaling starts a modification when free space is at or
  below 10% of allocated storage for at least five minutes, the previous storage optimisation has completed, and
  fewer than four storage modifications happened in the past 24 hours (it can also trigger on predicted growth);
  it cannot fully prevent storage-full during large loads.
- Maintenance windows apply pending maintenance; subscribe to events and pick a window deliberately, and decide
  whether `--auto-minor-version-upgrade` suits the instance.
- IAM DB auth tokens are valid for 15 minutes.
- Changing instance class is applied with `--apply-immediately` or waits for the maintenance window.
- Encryption cannot be added to an existing unencrypted instance: snapshot, copy
  with `--kms-key-id`, restore.
- Multi-AZ DB cluster engine and version support is not checked here; read the User Guide before designing around it.

## Verify
- [ ] `reboot-db-instance --force-failover` completes with the app reconnecting within DNS TTL + retry, no manual intervention.
- [ ] `ReplicaLag` < 5 s under production write load; a replica promotion drill produces a writable standalone.
- [ ] No instance uses a `default.*` parameter group; `ParameterApplyStatus` is `in-sync` everywhere.
- [ ] A PITR restore to 10 minutes ago succeeds into the correct SG/parameter group and a known row is present.
- [ ] Blue/green switchover rehearsed on a staging copy with the production-size dataset; total app error window measured.

## Checked
Date: 2026-10-27. Sources: RDS User Guide pages Concepts.MultiAZ.Failover (60-120 s, DNS record change, JVM TTL),
multi-az-db-clusters-concepts, USER_PIT and USER_ManagingAutomatedBackups (5-minute log upload, I/O suspension),
CHAP_Storage (gp3 and io2 figures), USER_PIOPS.Autoscaling (trigger conditions), CHAP_Limits (read replicas per
primary 15), USER_WorkingWithParamGroups.Modifying (default group, dynamic vs static), blue-green-deployments
considerations and switching pages (timeout range, PK or REPLICA IDENTITY FULL, `-old<n>`, PITR reset); botocore `rds`
model (CreateDBInstance, CreateBlueGreenDeployment, SwitchoverBlueGreenDeployment, RestoreDBInstanceToPointInTime
parameters; retention 0 to 35). Corrected: autoscaling trigger (not "once per 6 h"), JVM TTL 60 s (not 30), blue/green
primary key rule, replica quota wording. Removed cost multiples, pinned engine versions, formula and default
parameter values, option names not confirmed, the IAM auth connection-rate figure and cluster failover seconds.
Method: documentation only; no commands were run.
