---
id: computing-software.database-administration.database-backup-recovery.managed-cloud-database-backups
name: managed-cloud-database-backups
category: computing-software
field: database-administration
product: database-backup-recovery
tags: [database-administration, database-backup-recovery, backup-strategy, point-in-time-recovery, rds-snapshots, managed-database-backup, cross-region-backup, aws-backup]
level: practitioner
status: draft
description: "Get managed database backups right on RDS/Aurora, Cloud SQL and Azure: automated PITR vs manual snapshots, retention, cross-region and cross-account copies, and restore tests."
sources:
  - https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_WorkingWithAutomatedBackups.html
  - https://cloud.google.com/sql/docs/postgres/backup-recovery/backups
  - https://learn.microsoft.com/en-us/azure/postgresql/flexible-server/concepts-backup-restore
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Managed cloud database backups

## What you get by default
| Service | Automated backups / PITR | Max retention | Restore creates |
|---|---|---|---|
| Amazon RDS / Aurora | daily snapshot + transaction logs, PITR to ~5 min ago | 35 days | a **new** instance/cluster |
| Google Cloud SQL | daily backups + PITR (binary logs / WAL) | 365 backups (Enterprise Plus: longer PITR) | new or same instance |
| Azure Database for PostgreSQL/MySQL Flexible | snapshots + logs, PITR | 35 days | a new server |
| Azure SQL Database | full/diff/log, PITR | 35 days (+ LTR up to 10 years) | a new database |

## Gaps to close
1. **Deletion**: deleting an RDS instance can delete its automated backups (unless "retain
   automated backups" is set); Cloud SQL deletes backups with the instance (retained backups
   option in newer releases); Azure servers likewise. Enable deletion protection and keep
   **manual/long-term** copies.
2. **Retention beyond 35 days** (compliance): manual snapshots (kept until deleted), AWS Backup
   plans with vault lock, Azure LTR, Cloud SQL on-demand backups or exports.
3. **Region loss**: cross-region automated backup replication (RDS), cross-region snapshot copy,
   Aurora Global Database, Cloud SQL cross-region replicas, Azure geo-redundant backup storage.
4. **Account compromise**: copy snapshots to a separate backup account with vault lock
   (AWS Backup cross-account copy) so a compromised production account cannot delete them.
5. **Logical exports**: `pg_dump`/`mysqldump` to object storage occasionally, for portability
   and single-table restores (managed snapshots restore whole instances only).

## Restores
```bash
aws rds restore-db-instance-to-point-in-time --source-db-instance-identifier prod \
  --target-db-instance-identifier prod-pitr-0915 --restore-time 2026-10-18T09:15:00Z
gcloud sql backups list --instance=prod
gcloud sql instances clone prod prod-pitr --point-in-time '2026-10-18T09:15:00Z'
az postgres flexible-server restore -g rg -n prod-pitr --source-server prod --restore-time "2026-10-18T09:15:00Z"
```
Restored instances get **new endpoints**, default parameter/option groups unless specified,
and need security groups, users and monitoring reattached. Script that.

## Encryption
Snapshots inherit the KMS key; copying cross-account/region needs key grants or re-encryption.
If the key is deleted, backups are unrecoverable: protect keys with deletion windows and backups.

## Test
Quarterly: PITR restore to a scratch instance, run integrity and row-count checks, measure the
time (large instances take hours; Aurora restores are faster but still minutes+), then delete it.

## Verify
Inventory shows for each production database: PITR window, long-term copies, cross-region and
cross-account copies, deletion protection on, and a dated successful restore test.
