---
id: computing-software.cloud-infrastructure-engineering.aws.aws-backup-cold-storage-lifecycle-and-retention
name: aws-backup-cold-storage-lifecycle-and-retention
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, aws-backup, cold-storage-transition, backup-retention, lifecycle, backup-plans]
level: practitioner
status: docs-checked
description: "Set AWS Backup lifecycles that move recovery points to cold storage and expire them: the 90-day cold minimum, supported resources and changing existing points."
sources: ["https://docs.aws.amazon.com/aws-backup/latest/devguide/plan-options-and-configuration.html", "https://docs.aws.amazon.com/aws-backup/latest/devguide/backup-feature-availability.html", "https://docs.aws.amazon.com/aws-backup/latest/devguide/API_Lifecycle.html", "https://docs.aws.amazon.com/aws-backup/latest/devguide/API_UpdateRecoveryPointLifecycle.html", "https://docs.aws.amazon.com/aws-backup/latest/devguide/point-in-time-recovery.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Lifecycle to cold storage and retention

## 1. Rule lifecycle
```json
{"RuleName":"monthly","TargetBackupVaultName":"prod","ScheduleExpression":"cron(0 5 1 * ? *)",
 "Lifecycle":{"MoveToColdStorageAfterDays":30,"DeleteAfterDays":365,"OptInToArchiveForSupportedResources":true}}
```
- `DeleteAfterDays` must be at least `MoveToColdStorageAfterDays + 90`: a backup moved to cold storage must stay
  there for a minimum of 90 days.
- `MoveToColdStorageAfterDays` cannot be changed once a backup has transitioned to cold.
- AWS Backup recommends at least 8 days in warm storage before the transition for resource types with incremental
  backups; if the full backup moves too soon, Backup creates another warm full backup.
- Only some resource types can transition to cold storage; the others ignore the setting. The plan-options page
  lists CloudFormation, DynamoDB with advanced features, EBS (using EBS Snapshot Archive), EFS, SAP HANA on EC2,
  Timestream and VMware virtual machines. Check the feature-availability table for the current list.
- EBS archive applies when the backup frequency is monthly or less frequent; set
  `OptInToArchiveForSupportedResources` for EBS. For EBS an incremental backup becomes a full backup after it moves.
- Snapshot retention can range from 1 day to 100 years (or indefinite when no value is set); to remove an existing
  lifecycle and keep a recovery point indefinitely, pass `-1` for both `MoveToColdStorageAfterDays` and
  `DeleteAfterDays`.

## 2. What fits where
| Backup | Retention idea |
|---|---|
| Daily | 35 days warm |
| Monthly | 30 days warm, cold to 1-7 years |
| Continuous (PITR) | 1 to 35 days, never cold |
Continuous backups cannot transition to cold storage and have a maximum retention of 35 days; pair them with
snapshot rules for long retention.

## 3. Changing retention
Editing the plan affects **new** recovery points only. For existing ones:
```bash
aws backup update-recovery-point-lifecycle --backup-vault-name prod --recovery-point-arn <RP_ARN> \
  --lifecycle MoveToColdStorageAfterDays=30,DeleteAfterDays=730
```
- Include both `DeleteAfterDays` and `MoveToColdStorageAfterDays` when the point already has them; omitting them
  can set them to null.
- The operation does not support continuous backups.
- Vault Lock minimum and maximum retention applies to new backup and copy jobs in the vault; recovery points that
  were already in the vault keep their existing lifecycle.

## Verify
- [ ] `list-recovery-points-by-backup-vault --query 'RecoveryPoints[].{arn:RecoveryPointArn,calc:CalculatedLifecycle}'` shows expected cold (`MoveToColdStorageAt`) and delete (`DeleteAt`) dates.
- [ ] Test restore from a cold recovery point completed and timed.

## Checked
Date: 2026-10-27. Documentation release: AWS Backup Developer Guide (latest) and botocore backup 2018-11-15 model.
Confirmed: 90-day cold minimum and `DeleteAfterDays` rule, no change to the cold transition after it happens,
cold-eligible resource list, 8-day recommendation, continuous backups 1-35 days with no cold tier, `-1` to keep
indefinitely, `update-recovery-point-lifecycle` null-value warning and continuous-backup exclusion, and the
`CalculatedLifecycle` response field. Removed unconfirmed price and early-deletion billing claims and the claim
that a point cannot move from cold to warm. Prices were not checked.
Method: documentation only; no commands were run.
