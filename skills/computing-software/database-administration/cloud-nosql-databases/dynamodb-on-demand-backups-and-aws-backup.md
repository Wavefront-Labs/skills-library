---
id: computing-software.database-administration.cloud-nosql-databases.dynamodb-on-demand-backups-and-aws-backup
name: dynamodb-on-demand-backups-and-aws-backup
category: computing-software
field: database-administration
product: cloud-nosql-databases
tags: [dynamodb-on-demand-backups-and-aws-backup, dynamodb-backup-pitr, dynamodb, amazon-dynamodb, cloud-nosql-databases, database-administration]
level: practitioner
status: docs-checked
description: "Take full backups with no throughput impact and manage them by policy."
sources:
  - https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Backup-and-Restore.html
  - https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Introduction.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# On-demand backups and AWS Backup

**Goal:** Take full backups with no throughput impact and manage them by policy.

## Steps
- aws dynamodb create-backup --table-name Orders --backup-name pre-migration
- Each on-demand backup is a full copy of the table, consumes no provisioned throughput and there is no limit on how many you take; AWS Backup adds schedules, retention lifecycle, Vault Lock and cross-Region or cross-account copy.
- Restore with aws dynamodb restore-table-from-backup.
- Test restores on a schedule.

## Gotcha
A restore does not bring back auto scaling policies, IAM policies, CloudWatch alarms, tags, stream, TTL, deletion protection or PITR settings; script them. Backups made by AWS Backup cannot be deleted from the DynamoDB console.

## Verify
- [ ] Backup status is AVAILABLE and a scheduled restore test succeeds into a scratch table.

## Checked
Checked 2026-11-03 against the backup and restore how-it-works page and botocore (CreateBackup TableName/BackupName, RestoreTableFromBackup TargetTableName/BackupArn): full backups without throughput use, no backup count limit, AWS Backup schedules and retention, the list of settings to recreate after restore and the AWS_BACKUP console restriction match. AWS Backup Vault Lock and cross-Region/account copy are AWS Backup features and were not re-read on a DynamoDB page. Replaced "kept until deleted" and resolved the "(confirm)" marker.
Method: documentation only; no commands were run.
