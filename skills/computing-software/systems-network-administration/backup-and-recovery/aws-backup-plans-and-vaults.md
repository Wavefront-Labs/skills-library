---
id: computing-software.systems-network-administration.backup-and-recovery.aws-backup-plans-and-vaults
name: aws-backup-plans-and-vaults
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [aws-backup, backup-plan, backup-vault, vault-lock, cross-account-backup, restore-testing, cloud-backup]
level: advanced
status: docs-checked
description: "Protect AWS workloads with AWS Backup: plans and rules, tag-based selections, vault policies and Vault Lock, cross-region and cross-account copies, restore testing."
sources:
  - https://docs.aws.amazon.com/aws-backup/latest/devguide/whatisbackup.html
  - https://docs.aws.amazon.com/aws-backup/latest/devguide/vault-lock.html
  - https://docs.aws.amazon.com/aws-backup/latest/devguide/restore-testing.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AWS Backup plans and vaults

**Goal:** policy-driven backups of AWS resources (EC2/EBS, RDS, Aurora, DynamoDB, EFS, FSx, S3 and more) that an attacker in the workload account cannot delete.

## Plans and rules
```json
{
  "BackupPlanName": "prod-daily",
  "Rules": [{
    "RuleName": "daily-35d",
    "TargetBackupVaultName": "prod-vault",
    "ScheduleExpression": "cron(0 3 * * ? *)",
    "StartWindowMinutes": 60,
    "Lifecycle": { "DeleteAfterDays": 35 },
    "CopyActions": [{ "DestinationBackupVaultArn": "arn:aws:backup:eu-central-1:111122223333:backup-vault:dr-vault",
                      "Lifecycle": { "DeleteAfterDays": 90 } }]
  }]
}
```
```bash
aws backup create-backup-plan --backup-plan file://plan.json
aws backup create-backup-selection --backup-plan-id <id> --backup-selection '{
  "SelectionName":"tagged-prod","IamRoleArn":"arn:aws:iam::<acct>:role/AWSBackupDefaultServiceRole",
  "ListOfTags":[{"ConditionType":"STRINGEQUALS","ConditionKey":"backup","ConditionValue":"daily"}]}'
```
Tag-based selection protects new resources automatically when tagged.

## Protect the vault
- Vault access policy denying recovery point deletion except for a break-glass role (take the action names from the AWS Backup vault access policy docs).
- **Vault Lock** in compliance mode: once the grace time you choose (minimum 3 days) expires, the vault and its lock cannot be changed or deleted by any user or by AWS, and recovery points cannot be deleted before their lifecycle completes. In governance mode, users with sufficient IAM permissions can remove the lock. `PutBackupVaultLockConfiguration` with `ChangeableForDays` creates a compliance-mode lock; omit it for governance mode. Do not leave recovery points set to retain "Always" in a locked vault: they cannot be removed later.
- Copy to a vault in a separate **backup account** within AWS Organizations (cross-account backup), and ideally another region. Logically air-gapped vaults add further isolation.

## Governance
- Cross-account copy needs an existing AWS Organizations structure.
- Backup Audit Manager provides controls that track backup activity and generates daily compliance reports.

## Restore testing
AWS Backup restore testing plans periodically restore selected recovery points, run validation, and delete the test resources, giving restore evidence.

## Gotchas
- Continuous backup (point-in-time restore) is available only for some resource types; see Feature availability by resource.
- Read Lifecycle and storage tiers before setting `MoveToColdStorageAfterDays` and `DeleteAfterDays`, so deletion is not scheduled earlier than the tier allows.

## Verify
Backup Audit Manager report shows all tagged resources protected, and restore testing jobs succeed.

## Checked
2026-10-28. Confirmed against the AWS Backup botocore model (CreateBackupPlan and CreateBackupSelection members, Lifecycle, CopyAction, logically air-gapped vault field) and the AWS Backup Developer Guide pages What is AWS Backup, Vault Lock and Restore testing (grace time minimum, governance versus compliance, ChangeableForDays, test resources deleted after validation, Organizations requirement for cross-account copy). Removed: Organizations backup policy push, PITR 35-day figure, cold storage minimum durations, "even by root" wording and the vault policy action name, none confirmed in the fetched pages.
Method: documentation only; no commands were run.
