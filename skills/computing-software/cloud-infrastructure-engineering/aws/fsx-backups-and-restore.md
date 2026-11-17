---
id: computing-software.cloud-infrastructure-engineering.aws.fsx-backups-and-restore
name: fsx-backups-and-restore
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, fsx, fsx-backup, automatic-daily-backup, aws-backup, cross-region-backup-copy, file-restore]
level: practitioner
status: docs-checked
description: "Back up and restore FSx file systems: daily automatic backups, user and AWS Backup plans, cross-region copies, restore to a new file system, and file-level recovery."
sources: ["https://docs.aws.amazon.com/fsx/latest/WindowsGuide/using-backups.html", "https://docs.aws.amazon.com/fsx/latest/LustreGuide/using-backups-fsx.html", "https://docs.aws.amazon.com/fsx/latest/ONTAPGuide/using-backups.html", "https://docs.aws.amazon.com/aws-backup/latest/devguide/backup-fsx.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# FSx backups and restore

## 1. What each FSx type supports
| Type | Automatic daily backups | User backups | AWS Backup | Restore granularity |
|---|---|---|---|---|
| Windows File Server | yes (retention 0-90 days; console default 30, the API/CLI default differs) | yes | yes | whole file system, restored to a new file system; files via shadow copies |
| Lustre | persistent file systems not linked to an S3 bucket (no scratch, no S3-linked) | same limits | yes | whole file system; for S3-linked systems S3 is the primary copy |
| NetApp ONTAP | per volume (default on, retention 1-90 days, default 30) | per volume | yes | volume restored to a new volume |
| OpenZFS | supports backups and cross-Region copies | yes | yes | see the OpenZFS guide |
Backups are incremental and file-system-consistent (Windows uses VSS; ONTAP backups are built on volume snapshots).
User-initiated backups, including AWS Backup ones, are kept until you or AWS Backup delete them; automatic backups
are capped at 90 days.

## 2. Configure automatic backups
```bash
aws fsx update-file-system --file-system-id fs-0win \
  --windows-configuration 'AutomaticBackupRetentionDays=30,DailyAutomaticBackupStartTime=02:00,CopyTagsToBackups=true'
aws fsx create-backup --file-system-id fs-0win --tags Key=reason,Value=pre-upgrade
aws fsx describe-backups --filters Name=file-system-id,Values=fs-0win \
  --query 'Backups[].{id:BackupId,type:Type,state:Lifecycle,created:CreationTime}'
```
Deleting an ONTAP volume also deletes its automatic daily backups, with an option to take a final backup first.
User-initiated backups (including AWS Backup ones) persist until deleted.

## 3. AWS Backup for policy and copies
FSx can copy backups across Regions and accounts. Cross-account copies go through AWS Backup with AWS Organizations
support:
```bash
aws fsx copy-backup --source-backup-id backup-0abc --source-region eu-west-1 --region eu-central-1
```
Later copies to the same destination Region stay incremental only while you use the same KMS key.

## 4. Restore
Windows and Lustre restores create a **new file system**; Windows restores must use the same deployment type and
storage capacity as the original (you can grow it afterwards):
```bash
aws fsx create-file-system-from-backup --backup-id backup-0abc \
  --subnet-ids subnet-a subnet-b --security-group-ids sg-0fsx \
  --windows-configuration 'ThroughputCapacity=64,PreferredSubnetId=subnet-a,ActiveDirectoryId=d-0123'
```
Then repoint clients: DNS alias (FSx Windows supports DNS aliases you move to the new file
system), DFS namespace target swap, or update mount targets. Clients reach Windows shares by the file system DNS name
or DNS aliases associated with it.
ONTAP: restore a volume backup to a new volume on a file system in the same Region (copy the backup first for another Region).

## 5. File-level recovery without full restore
- Windows: enable **shadow copies** on the file system (see the FSx for Windows guide) so users can self-restore.
- ONTAP: volume snapshots and snapshot policies.
- Lustre linked to S3: S3 is the primary copy (FSx does not back these up); reload from the bucket.

## Gotchas
- Scratch Lustre file systems and S3-linked Lustre file systems have no FSx backups.
- ONTAP backup and restore are low-priority background processes, so heavy client I/O slows them.

## Verify
- [ ] `describe-backups` shows daily automatic backups at the expected time and retention.
- [ ] Quarterly test restore to a new file system with data checks and documented duration.
- [ ] Cross-region copies present for DR file systems; shadow copies/snapshots enabled for self-service restores.

## Checked

2026-10-28. Confirmed against the FSx for Windows, Lustre and ONTAP User Guide backup pages and the OpenZFS what-is page: retention ranges and defaults, VSS file-system-consistent incremental backups, Lustre scratch and S3-linked exclusion, same-deployment-type restore, cross-account copy through AWS Backup, ONTAP per-volume restore, and the CopyTagsToBackups option. The botocore model confirms the DeleteFileSystem shape.
Removed or corrected: "crash-consistent" (docs say file-system-consistent), the default of 7 days, the claim that Multi-AZ restores to a chosen deployment type (it must match the original), the customer-managed-KMS requirement, AWS Backup vault lock/long retention (page not readable), OpenZFS automatic-backup and `.zfs/snapshot` details, and the SkipFinalBackup delete example.
Method: documentation only; no commands were run.
