---
id: computing-software.cloud-infrastructure-engineering.aws.aws-backup-restoring-from-recovery-points
name: aws-backup-restoring-from-recovery-points
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, aws-backup, recovery-point-restore, restore-job, restore-metadata, item-level-restore, cross-account-restore]
level: practitioner
status: docs-checked
description: "Restore resources from AWS Backup recovery points: restore metadata per resource type, the restore role, item-level S3/EFS restores, cross-account copies and post-restore work."
sources: ["https://docs.aws.amazon.com/aws-backup/latest/devguide/restoring-a-backup.html", "https://docs.aws.amazon.com/aws-backup/latest/devguide/restoring-s3.html", "https://docs.aws.amazon.com/aws-backup/latest/devguide/restoring-efs.html", "https://docs.aws.amazon.com/aws-backup/latest/devguide/restoring-ec2.html", "https://docs.aws.amazon.com/aws-backup/latest/devguide/restoring-ebs.html", "https://docs.aws.amazon.com/aws-backup/latest/devguide/restoring-rds.html", "https://docs.aws.amazon.com/cli/latest/reference/backup/start-restore-job.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Restoring from AWS Backup recovery points

## 1. Find the recovery point
```bash
aws backup list-recovery-points-by-resource --resource-arn arn:aws:rds:eu-west-1:<ACCOUNT_ID>:db:orders \
  --query 'RecoveryPoints[].{arn:RecoveryPointArn,created:CreationDate,status:Status,vault:BackupVaultName}'
aws backup list-recovery-points-by-backup-vault --backup-vault-name prod-vault --by-resource-type EFS
```

## 2. Get and edit restore metadata
Each resource type needs its own parameters. Start from what Backup recorded:
```bash
aws backup get-recovery-point-restore-metadata --backup-vault-name prod-vault \
  --recovery-point-arn <rp-arn> --query RestoreMetadata > meta.json
```
`get-recovery-point-restore-metadata` may not return everything needed (for example a new resource name when the
original exists). Edit for the target. Documented metadata keys per type:
- **EC2**: `InstanceType`, `SubnetId`, `SecurityGroupIds`, `IamInstanceProfileName` (and others on the EC2 restore page).
- **EBS**: `availabilityZone`, `volumeType`, `volumeSize`, `iops`, `encrypted`.
- **DynamoDB**: `targetTableName` (not case-sensitive), plus encryption keys.
- **EFS**: `file-system-id`, `newFileSystem`, `Encrypted`, `KmsKeyId`, `PerformanceMode` (`generalPurpose` or `maxIO`),
  `CreationToken`, `ItemsToRestore` (up to five file paths).
- **S3**: `DestinationBucketName` (mandatory), `ItemsToRestore` (up to five object paths), `RestoreTime`
  (continuous recovery points).
- **RDS**: the parameters of RDS `RestoreDBInstanceFromDBSnapshot` / `RestoreDBInstanceToPointInTime`; `EngineVersion`,
  `KmsKeyId`, `Encrypted` and `vpcId` are accepted but have no effect.

## 3. Start and monitor
```bash
aws backup start-restore-job --recovery-point-arn <rp-arn> \
  --iam-role-arn arn:aws:iam::<ACCOUNT_ID>:role/service-role/AWSBackupDefaultServiceRole \
  --metadata file://meta.json --resource-type RDS
aws backup describe-restore-job --restore-job-id <id> \
  --query '{s:Status,pct:PercentDone,created:CreatedResourceArn,msg:StatusMessage}'
```
Restore job statuses: `PENDING`, `RUNNING`, `COMPLETED`, `ABORTED`, `FAILED`. `--metadata` and `--recovery-point-arn`
are required; `--iam-role-arn` and `--resource-type` are optional on the API.
Managed policies for the restore role include `AWSBackupServiceRolePolicyForRestores` and, for S3,
`AWSBackupServiceRolePolicyForS3Restore`. The role needs KMS access to the recovery point key and the target key.
AWS Backup restores are non-destructive: for S3, an existing object with the same name or version is skipped, and
nothing in the destination bucket is deleted; EFS restores land in a recovery directory.

## 4. Item-level restores
- **S3**: restore the whole bucket or up to five objects or folders (`ItemsToRestore`), to an existing or new bucket,
  into S3 Standard; from continuous (up to 35 days, `RestoreTime`) or snapshot backups. By default only the latest
  version is restored.
- **EFS**: restore specific files or directories to the original file system or a new one. Restored files appear in a
  recovery directory named `aws-backup-restore_<datetime>` off the root, and you move them into place.
- Other types, including RDS and Aurora point-in-time restores, follow their own restore pages.

## 5. Cross-account and cross-region
Restore from a **copy** in the destination account or Region vault, in the same Region as the copy. S3 cross-Region
copies cannot reuse the original encryption method, so choose another one at restore. The copy's KMS key must be
usable in the destination. Logically air-gapped vaults can be shared through AWS RAM so a recovery account restores
from them.

## 6. After the restore
- Tags: `StartRestoreJob` has `CopySourceTagsToRestoredResource`, default false (the console copies by default);
  it is unsupported for DynamoDB, S3, SAP HANA, Timestream and VM restores.
- Check what the restored resource does and does not carry from the original (DNS records, load balancer target
  registration, resource policies, Elastic IPs, parameter groups), and add the new resource to the backup plan tags.
- Validate data integrity before switching traffic.

## Verify
- [ ] Restore job `COMPLETED` with a `CreatedResourceArn`; resource reachable with the intended network settings.
- [ ] Data check (row counts, checksums) passes against expectations for the restore point time.
- [ ] Restore duration recorded against RTO; a restore testing plan covers this resource type.

## Checked
Date: 2026-10-27. Documentation release: AWS Backup Developer Guide (latest) and botocore backup 2018-11-15 model.
Confirmed: `StartRestoreJob` required and optional parameters, restore job statuses, managed policy names,
per-type metadata keys (EC2, EBS, DynamoDB, EFS, S3, RDS), S3 and EFS item-level limits and the EFS recovery
directory, same-Region restore of copies, S3 cross-Region encryption note, tag-copy default and exclusions.
Removed the claims that restores always create new resources, that the role needs `iam:PassRole`, and the FSx,
VMware and Aurora `RestoreToTime` item-level claims, none of which the restore pages confirm.
Method: documentation only; no commands were run.
