---
id: computing-software.cloud-infrastructure-engineering.aws.aws-backup-vault-access-policies-and-kms
name: aws-backup-vault-access-policies-and-kms
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, aws-backup, vault-access-policy, backup-vault-kms, vault-lock, ransomware-protection]
level: advanced
status: docs-checked
description: "Protect AWS Backup vaults with access policies that deny deletion, choose vault KMS keys for cross-account copies, and add Vault Lock for immutability."
sources: ["https://docs.aws.amazon.com/aws-backup/latest/devguide/create-a-vault-access-policy.html", "https://docs.aws.amazon.com/aws-backup/latest/devguide/encryption.html", "https://docs.aws.amazon.com/aws-backup/latest/devguide/vault-lock.html", "https://docs.aws.amazon.com/aws-backup/latest/devguide/create-a-vault.html", "https://docs.aws.amazon.com/aws-backup/latest/devguide/logicallyairgappedvault.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Vault access policies and vault KMS keys

## 1. Deny destructive actions
```json
{"Version":"2012-10-17","Statement":[{"Effect":"Deny","Principal":"*",
  "Action":["backup:DeleteRecoveryPoint","backup:UpdateRecoveryPointLifecycle","backup:PutBackupVaultAccessPolicy","backup:DeleteBackupVault"],
  "Resource":"*",
  "Condition":{"ArnNotLike":{"aws:PrincipalArn":"arn:aws:iam::<ACCOUNT_ID>:role/BackupAdmin"}}}]}
```
```bash
aws backup put-backup-vault-access-policy --backup-vault-name prod --policy file://vault-policy.json
```
- AWS Backup vault access policies do not support a wildcard in `Action`; list each action.
- They control access through AWS Backup APIs only. EBS and RDS snapshots can also be reached through those
  services' own APIs, so add IAM policies for them.
- Regardless of the policy, cross-account access for any action other than `backup:CopyIntoBackupVault` is rejected.
  Add an allow for `backup:CopyIntoBackupVault` from source accounts when the vault is a cross-account copy target.- To limit a deny to one type, set `Resource` to the recovery point ARN pattern, for example `arn:aws:ec2:*:*:snapshot/*`.

## 2. Encryption keys
- The vault key is chosen at vault creation and cannot be changed afterwards; the default is the `aws/backup` key.
- Independent encryption: resource types fully managed by AWS Backup (S3, VMware, DynamoDB with advanced backup,
  EFS, Timestream, CloudFormation, SAP HANA) use the vault key. EBS, RDS, Aurora, FSx, DocumentDB, Neptune, Redshift,
  Storage Gateway and standard DynamoDB keep the source resource's key (or stay unencrypted).
- Cross-account copy of a recovery point from a resource type not fully managed by AWS Backup cannot use AWS
  managed keys (`aws/ebs`, `aws/rds`): their key policy is immutable and cannot be shared. Use a customer managed
  key shared with the destination account.
- A copy is encrypted with the destination vault's key. For a fully managed type choose a customer managed key or
  `aws/backup`; for others the destination key must be a customer managed key or the owning service's managed key
  (for EC2, `aws/ebs`, not `aws/backup`).
- The key policy needs at least `kms:CreateGrant`, `kms:GenerateDataKey` and `kms:Decrypt` for AWS Backup;
  Deny statements or a revoked grant cause failed jobs.

## 3. Vault Lock
```bash
aws backup put-backup-vault-lock-configuration --backup-vault-name prod \
  --min-retention-days 7 --max-retention-days 3650 --changeable-for-days 3
```
`--changeable-for-days` (3 to 36,500) puts the lock in compliance mode: after the grace time the vault and its
lock cannot be changed or deleted by any user or AWS while the vault holds recovery points. Omit it for governance
mode, where users with permissions can remove the lock. Min and max retention apply to new backup and copy jobs.

## 4. Logically air-gapped vaults
A separate vault type that always has a compliance-mode vault lock, uses an AWS owned key by default (a customer
managed key is optional), and can be shared through AWS RAM for restore from another account. Minimum retention is
7 days.

## Verify
- [ ] A non-admin role gets `AccessDenied` on `delete-recovery-point`.
- [ ] Cross-account copy job completes into the backup account vault.

## Checked
Date: 2026-10-27. Documentation release: AWS Backup Developer Guide (latest). Confirmed: no wildcard in policy
`Action`, API-only scope, `CopyIntoBackupVault` cross-account rule, vault key immutability and default key,
independent-encryption resource table, managed-key limits for cross-account copy, minimum KMS permissions, Vault
Lock parameter ranges, and air-gapped vault key and retention rules. Removed the unconfirmed claim that the
destination key policy must allow "AWS Backup in that account".
Method: documentation only; no commands were run.
