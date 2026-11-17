---
id: computing-software.cloud-infrastructure-engineering.aws.aws-backup-plans-and-vaults
name: aws-backup-plans-and-vaults
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, aws-backup, backup-plan, backup-vault, vault-lock, recovery-point, backup-selection, tag-based-backup, cross-region-backup, cross-account-backup, logically-air-gapped-vault, restore-testing, backup-audit-manager, continuous-backup, point-in-time-recovery, backup-policy, organizations, ransomware, immutable-backup, retention, backup-policies, org-backup-policy]
level: practitioner
status: docs-checked
description: "Centralise backups with AWS Backup: tag-driven plans, Vault Lock, cross-account and cross-Region copies, air-gapped vaults, restore testing and org-wide backup policies."
sources: ["https://docs.aws.amazon.com/aws-backup/latest/devguide/whatisbackup.html", "https://docs.aws.amazon.com/aws-backup/latest/devguide/creating-a-backup-plan.html", "https://docs.aws.amazon.com/aws-backup/latest/devguide/plan-options-and-configuration.html", "https://docs.aws.amazon.com/aws-backup/latest/devguide/vault-lock.html", "https://docs.aws.amazon.com/aws-backup/latest/devguide/logicallyairgappedvault.html", "https://docs.aws.amazon.com/aws-backup/latest/devguide/point-in-time-recovery.html", "https://docs.aws.amazon.com/aws-backup/latest/devguide/restore-testing.html", "https://docs.aws.amazon.com/aws-backup/latest/devguide/aws-backup-audit-manager.html", "https://docs.aws.amazon.com/aws-backup/latest/devguide/manage-cross-account.html", "https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_policies_backup.html"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# AWS Backup: plans, vaults and proving restores

**Goal:** one policy that backs up every tagged resource (EBS, RDS/Aurora, DynamoDB,
EFS, FSx, S3, EC2, VMs...) on a schedule, keeps copies an attacker with admin
credentials cannot delete, and proves regularly that the copies restore.

## 1. Model
- **Vault**: a container for recovery points with its own KMS key and access policy.
- **Plan**: rules (schedule, start window, completion window, lifecycle to cold storage,
  retention, copy actions to other vaults/regions/accounts).
- **Selection**: which resources the plan covers: by tag (`backup=daily`), by ARN, or
  "all resources" with `Conditions` (`StringEquals`, `StringNotEquals`, `StringLike`, `StringNotLike`) or `NotResources`.
- **Recovery point**: the backup (an EBS snapshot, RDS snapshot, EFS backup...).
Per-region service opt-in per resource type is set with
`aws backup update-region-settings --resource-type-opt-in-preference EBS=true,RDS=true` (a map of resource type to boolean).

## 2. A production plan
```json
{"BackupPlanName": "prod-daily",
 "Rules": [
  {"RuleName": "daily", "TargetBackupVaultName": "prod",
   "ScheduleExpression": "cron(0 2 * * ? *)", "ScheduleExpressionTimezone": "Europe/London",
   "StartWindowMinutes": 60, "CompletionWindowMinutes": 480,
   "Lifecycle": {"MoveToColdStorageAfterDays": 30, "DeleteAfterDays": 365},
   "CopyActions": [{"DestinationBackupVaultArn": "arn:aws:backup:eu-central-1:<DR_ACCOUNT_ID>:backup-vault:prod-dr",
                    "Lifecycle": {"DeleteAfterDays": 365}}],
   "RecoveryPointTags": {"plan": "prod-daily"}},
  {"RuleName": "pitr", "TargetBackupVaultName": "prod",
   "ScheduleExpression": "cron(0 3 * * ? *)", "EnableContinuousBackup": true,
   "Lifecycle": {"DeleteAfterDays": 35}},
  {"RuleName": "monthly-7y", "TargetBackupVaultName": "prod-compliance",
   "ScheduleExpression": "cron(0 3 1 * ? *)", "Lifecycle": {"MoveToColdStorageAfterDays": 90, "DeleteAfterDays": 2555}}
 ]}
```
```bash
aws backup create-backup-plan --backup-plan file://plan.json
aws backup create-backup-selection --backup-plan-id <ID> --backup-selection \
  '{"SelectionName":"tagged","IamRoleArn":"arn:aws:iam::<ACCOUNT_ID>:role/service-role/AWSBackupDefaultServiceRole",
    "Resources":["*"],"Conditions":{"StringEquals":[{"ConditionKey":"aws:ResourceTag/backup","ConditionValue":"daily"}]}}'
```
- Cold storage applies only to some resource types (CloudFormation, DynamoDB with advanced features, EBS via
  Snapshot Archive for monthly-or-less-frequent backups, EFS, SAP HANA, Timestream, VMware); `DeleteAfterDays` must
  be at least 90 days after `MoveToColdStorageAfterDays`. Other types ignore the transition.
- **Continuous backup** (PITR) is a separate rule: restore to within 1 second of precision, maximum 35 days,
  no cold storage. Supported: S3, RDS (not Multi-AZ DB clusters), Aurora and SAP HANA on EC2. Only one continuous backup per
  resource is kept; a duplicate rule creates snapshot backups instead.
- `StartWindowMinutes`: the job stays `CREATED` and is retried at least every 10 minutes until it starts or the
  start window ends; it then becomes `EXPIRED`. Alarm on `EXPIRED`.
- Tag discipline is the whole mechanism: a resource without the tag is not backed up. The AWS Config managed rule
  `backup-plan-min-frequency-and-min-retention-check` (defaults: 1 day, 35 days retention) and Backup Audit Manager
  controls such as `BACKUP_RESOURCES_PROTECTED_BY_BACKUP_PLAN` catch the stragglers.

## 3. Vaults that resist deletion
```bash
aws backup create-backup-vault --backup-vault-name prod-compliance --encryption-key-arn arn:aws:kms:<REGION>:<ACCOUNT_ID>:key/<KEY_ID>
aws backup put-backup-vault-lock-configuration --backup-vault-name prod-compliance \
  --min-retention-days 2555 --max-retention-days 2600 --changeable-for-days 3
```
- **Vault Lock, compliance mode**: include `--changeable-for-days` (3 to 36,500). After that grace time the vault
  and its lock are immutable for any user and for AWS while it holds recovery points. Omit it for governance mode
  (removable by users with permissions). Test in governance mode first.
- Min and max retention (1 to 36,500 days) apply to new backup and copy jobs, which fail if they do not conform;
  recovery points already in the vault are unaffected. Recovery points saved with "Always" retention in a locked
  vault are kept forever, so check retention before the grace time ends.
- Vault Lock and access policies govern AWS Backup actions only; EBS snapshots can still be shared with
  `ec2:ModifySnapshotAttribute` and tiered with `ec2:ModifySnapshotTier`. Deny those in IAM or SCPs, exempting the
  backup roles.
- Vault **access policy**: no wildcards in `Action`; deny `backup:DeleteRecoveryPoint` and
  `backup:UpdateRecoveryPointLifecycle` to everyone but a break-glass role. Cross-account access is rejected for
  every action except `backup:CopyIntoBackupVault`.
- **Logically air-gapped vault**: always has a compliance-mode vault lock; encrypted with an AWS owned key by
  default or optionally a customer managed key; minimum retention at least 7 days; can be shared through AWS RAM
  so a recovery account can restore from it; recovery points in it cannot be indexed for backup search.
- Cross-account copies: both accounts must be in the same organization, the destination vault access policy must
  allow `backup:CopyIntoBackupVault`, and cross-account backup is enabled from the management account. For resource
  types not fully managed by AWS Backup (EBS, RDS and others) a customer managed key is needed, because the key
  policy of an AWS managed key (`aws/rds`, `aws/ebs`) cannot be shared across accounts.

## 4. Organisation-wide
From the management (or delegated admin) account, turn on AWS Backup cross-account management, then **backup
policies** (`aws organizations create-policy --type BACKUP_POLICY`) apply plans to accounts and OUs; the effective
plan appears in each member account as an immutable plan. The management account can then see backup job status
for all accounts. The effective policy must be complete (all required elements) or the affected resources are not
backed up.

## 5. Restore and restore testing
```bash
aws backup list-recovery-points-by-backup-vault --backup-vault-name prod --by-resource-arn <ARN>
aws backup get-recovery-point-restore-metadata --backup-vault-name prod --recovery-point-arn <RP>
aws backup start-restore-job --recovery-point-arn <RP> --iam-role-arn <ROLE> --metadata file://meta.json   # metadata differs per resource type
```
**Restore testing plans** (`create-restore-testing-plan` plus `create-restore-testing-selection` per resource type)
restore latest or random recovery points on a schedule (`StartWindowHours`, selection window days), optionally
retain the restored resource for a validation window of 1 to 168 hours so validation can run (validation is
programmatic, not console), then delete it. Make it frequent for Tier-1 data.

## 6. Monitoring and audit
- EventBridge: `aws.backup` `Backup Job State Change` with `state` of `FAILED`, `EXPIRED` or `ABORTED` to SNS or a ticket.
- Backup Audit Manager controls include `BACKUP_RECOVERY_POINT_ENCRYPTED`,
  `BACKUP_RECOVERY_POINT_MINIMUM_RETENTION_CHECK`, `BACKUP_RESOURCES_PROTECTED_BY_BACKUP_VAULT_LOCK`; resource
  tracking through AWS Config must be on.

## Gotchas
- The default service role does not cover everything; managed policies such as `AWSBackupServiceRolePolicyForS3Backup`,
  `AWSBackupServiceRolePolicyForRestores` and `AWSBackupServiceRolePolicyForS3Restore` exist for those cases.
- S3 backups need S3 Versioning enabled on the bucket.
- DynamoDB cold storage and full AWS Backup management require the advanced DynamoDB backup feature.
- Continuous backup resource types and air-gapped vault features grow; check the feature-availability table.

## Verify
- [ ] Every production resource with `backup=daily` has a recovery point newer than 24 hours (`list-recovery-points-by-resource`).
- [ ] Deleting a recovery point in the locked vault is denied.
- [ ] Cross-account copy job `COMPLETED` in the DR vault; its KMS key is a customer managed key.
- [ ] Last restore-testing run `COMPLETED` with validation successful for RDS, EBS and EFS.
- [ ] No jobs in `EXPIRED` state in the last 30 days; alarm wired to on-call.

## Checked
Date: 2026-10-27. Documentation release: AWS Backup Developer Guide (latest), AWS Organizations User Guide,
AWS Config managed rule page and botocore backup and organizations models. Confirmed: lifecycle 90-day rule and
cold-eligible types, continuous backup limits and supported services, start-window EXPIRED behaviour, Vault Lock
parameters, grace time and immutability, EC2 API gaps, access-policy rules, air-gapped vault properties, KMS rules
for cross-account copies, `BACKUP_POLICY` type, restore testing parameters, Audit Manager control names, Config
rule defaults and managed policy names. Fixed the example plan (a continuous-backup rule cannot carry a cold
transition or 365-day retention) and the claim that EBS/RDS have retention-only lifecycles. Removed the price
figures, the "silently skipped" claim, and the unconfirmed claims about air-gapped restore speed and Aurora/RDS
snapshot separation. Prices were not checked.
Method: documentation only; no commands were run.
