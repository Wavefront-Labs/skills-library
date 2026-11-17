---
id: computing-software.database-administration.cloud-nosql-databases.dynamodb-point-in-time-recovery
name: dynamodb-point-in-time-recovery
category: computing-software
field: database-administration
product: cloud-nosql-databases
tags: [dynamodb-point-in-time-recovery, dynamodb-backup-pitr, dynamodb, amazon-dynamodb, cloud-nosql-databases, database-administration]
level: practitioner
status: docs-checked
description: "Enable continuous backups to restore to any second in the recovery window (up to 35 days)."
sources:
  - https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Backup-and-Restore.html
  - https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/pointintimerecovery_restores.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Point in time recovery

**Goal:** Enable continuous backups to restore to any second in the recovery window (up to 35 days).

## Steps
- aws dynamodb update-continuous-backups --table-name Orders --point-in-time-recovery-specification PointInTimeRecoveryEnabled=true,RecoveryPeriodInDays=35
- Restore: aws dynamodb restore-table-to-point-in-time --source-table-name Orders --target-table-name Orders-restore --restore-date-time 2026-11-01T10:00:00Z
- A restore always creates a new table; auto scaling policies, IAM policies, CloudWatch alarms, Contributor Insights, tags, stream settings, TTL, deletion protection and PITR settings must be set again on it.
- Restore time varies with several factors and is not always correlated with table size; record real restore times for recovery planning.

## Gotcha
Disabling and re-enabling PITR resets the recoverable window, so only the latest restorable time is available at first.

## Verify
- [ ] describe-continuous-backups shows ENABLED with an EarliestRestorableDateTime and a test restore matches expected data.

## Checked
Checked 2026-11-03 against the restore page and botocore shapes (UpdateContinuousBackups, RestoreTableToPointInTime): restore to a new table, the list of settings to recreate, RecoveryPeriodInDays 1-35 and the restore-time wording. Fixed "restore time depends on table size" (docs say not always correlated). Replaced the "off by default" gotcha with the documented re-enable reset; resolved the "(confirm)" with the docs list.
Method: documentation only; no commands were run.
