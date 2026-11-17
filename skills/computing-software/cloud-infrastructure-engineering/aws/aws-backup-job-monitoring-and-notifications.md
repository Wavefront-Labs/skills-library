---
id: computing-software.cloud-infrastructure-engineering.aws.aws-backup-job-monitoring-and-notifications
name: aws-backup-job-monitoring-and-notifications
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, aws-backup, backup-job-monitoring, backup-notifications, cross-account-monitoring, backup-job-failed, eventbridge]
level: practitioner
status: docs-checked
description: "Know when AWS Backup jobs fail: job states, vault SNS notifications, EventBridge rules, CloudWatch metrics, org-wide job monitoring and common failure causes."
sources: ["https://docs.aws.amazon.com/aws-backup/latest/devguide/monitoring.html", "https://docs.aws.amazon.com/aws-backup/latest/devguide/backup-notifications.html", "https://docs.aws.amazon.com/aws-backup/latest/devguide/eventbridge.html", "https://docs.aws.amazon.com/aws-backup/latest/devguide/cloudwatch.html", "https://docs.aws.amazon.com/aws-backup/latest/devguide/manage-cross-account.html", "https://docs.aws.amazon.com/aws-backup/latest/devguide/API_ListBackupJobs.html", "https://docs.aws.amazon.com/aws-backup/latest/devguide/troubleshooting.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AWS Backup job monitoring and notifications

## 1. Job states
Backup jobs move through `CREATED`, `PENDING`, `RUNNING`, then `COMPLETED`, `PARTIAL`, `FAILED`, `EXPIRED`,
`ABORTING` or `ABORTED` (the `ListBackupJobs` `ByState` values). Copy jobs use `CREATED`, `RUNNING`, `COMPLETED`,
`FAILED`, `PARTIAL`; restore jobs use `PENDING`, `RUNNING`, `COMPLETED`, `ABORTED`, `FAILED`. The console label
"Completed with issues" is a `COMPLETED` backup job that carries a status message, so monitor those too.
```bash
aws backup list-backup-jobs --by-state FAILED --by-created-after $(date -u -d '-1 day' +%FT%TZ) \
  --query 'BackupJobs[].{res:ResourceArn,msg:StatusMessage,plan:CreatedBy.BackupPlanId}'
aws backup list-copy-jobs --by-state FAILED
```
Org-wide from the management account (cross-account monitoring turned on in AWS Backup):
`aws backup list-backup-jobs --by-account-id '*' --by-state FAILED`. `ByAccountId` is otherwise a 12-digit account
ID; `*` works only from an Organizations management account.

## 2. Notifications
Vault-level SNS:
```bash
aws backup put-backup-vault-notifications --backup-vault-name prod-vault \
  --sns-topic-arn arn:aws:sns:eu-west-1:<ACCOUNT_ID>:backup-alerts \
  --backup-vault-events BACKUP_JOB_FAILED BACKUP_JOB_EXPIRED COPY_JOB_FAILED RESTORE_JOB_COMPLETED S3_BACKUP_OBJECT_FAILED
```
- The SNS topic access policy must name AWS Backup as a principal allowed to publish.
- Standard SNS topics work; FIFO topics are not supported. AWS Backup does not currently support cross-account SNS
  notifications even though SNS itself allows them.
- `S3_BACKUP_OBJECT_FAILED` is one of the extra S3 events; EKS has its own extra events.
- EventBridge tracks more changes than the SNS notification API (vaults, copy jobs, Region settings, cold and warm
  recovery point counts). Example rule:
```json
{"source": ["aws.backup"], "detail-type": ["Backup Job State Change", "Copy Job State Change"],
 "detail": {"state": ["FAILED", "EXPIRED", "ABORTED"]}}
```
Forward member-account events to a central bus to alert in one place.

## 3. Metrics
CloudWatch namespace `AWS/Backup`, updated every 5 minutes. Among the published names: `NumberOfBackupJobsFailed`,
`NumberOfBackupJobsExpired`, `NumberOfBackupJobsAborted`, `NumberOfBackupJobsCompleted`,
`NumberOfCopyJobsFailed`, `NumberOfRestoreJobsFailed`, `NumberOfRecoveryPointsCold`. Alarm on failed/expired > 0.
Backup Audit Manager controls catch unprotected resources, which job monitoring alone misses:
`BACKUP_RESOURCES_PROTECTED_BY_BACKUP_PLAN`, `BACKUP_PLAN_MIN_FREQUENCY_AND_MIN_RETENTION_CHECK`,
`BACKUP_RECOVERY_POINT_MINIMUM_RETENTION_CHECK`, `BACKUP_LAST_RECOVERY_POINT_CREATED`.
Resource tracking (AWS Config recording) must be on for the framework to evaluate resources.

## 4. Common failure causes
| StatusMessage (abridged) | Fix |
|---|---|
| `Insufficient privileges to perform this action` | The backup role lacks permission on the resource or its KMS key |
| `Given key ID not accessible` on a cross-account copy | The key policy does not allow the copy path; use a customer managed key shared with the destination |
| `Backup job expired before completion` | Seen when an RDS console backup collides with an Aurora backup job; configure a longer backup window |
| S3 backup failed | S3 Versioning must be enabled on the bucket; also check the role's S3 and KMS permissions |
| EC2 VSS failures (Windows) | See the Backup troubleshooting page for VSS |
| Copy failed cross-account | Destination vault access policy must allow `backup:CopyIntoBackupVault`; accounts must share an organization |

## Verify
- [ ] EventBridge/SNS alert fires for a deliberately failed job in a sandbox (e.g. revoke KMS access).
- [ ] Daily review or dashboard of failed/expired jobs across all accounts is zero or explained.
- [ ] Audit Manager report shows all tagged resources protected.

## Checked
Date: 2026-10-27. Documentation release: AWS Backup Developer Guide (latest) and botocore backup 2018-11-15 model.
Confirmed: job state enums, `BackupVaultEvent` values used above, `put-backup-vault-notifications` required
parameters, SNS policy and FIFO limits, EventBridge detail types, `AWS/Backup` metric names and 5-minute refresh,
Audit Manager control names, the `ByAccountId` `*` behaviour (the earlier `ANY` value is not valid on the API),
the S3 versioning requirement, and the RDS/Aurora expired-job message. Removed the `PARTIAL` state from the
EventBridge example (the event page lists FAILED, COMPLETED, RUNNING, ABORTED, EXPIRED, PENDING, CREATED) and
removed failure-cause rows that no documentation page confirmed.
Method: documentation only; no commands were run.
