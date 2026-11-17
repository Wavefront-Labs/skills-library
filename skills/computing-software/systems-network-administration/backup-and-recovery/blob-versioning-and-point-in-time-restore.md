---
id: computing-software.systems-network-administration.backup-and-recovery.blob-versioning-and-point-in-time-restore
name: blob-versioning-and-point-in-time-restore
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [blob-versioning, saas-cloud-backup, azure-blob-point-in-time-restore, s3-versioning, soft-delete, object-storage]
level: practitioner
status: docs-checked
description: "Protect object storage data with versioning, soft delete and point-in-time restore in Azure Blob, Amazon S3 and Google Cloud Storage, and restore overwritten or deleted objects."
sources:
  - https://learn.microsoft.com/en-us/azure/storage/blobs/point-in-time-restore-overview
  - https://learn.microsoft.com/en-us/azure/storage/blobs/versioning-overview
  - https://docs.aws.amazon.com/AmazonS3/latest/userguide/Versioning.html
  - https://cloud.google.com/storage/docs/soft-delete
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Blob versioning and point-in-time restore

**Goal:** recover objects that were overwritten, deleted or encrypted by a compromised client, without a separate backup copy for short windows.

## Azure Blob
- **Versioning**: each overwrite keeps the previous version.
- **Soft delete** for blobs (retention 1 to 365 days; it cannot be extended once the period has elapsed) and for containers.
- **Point-in-time restore** (block blobs in standard general-purpose v2 accounts, hot and cool tiers, no hierarchical namespace): requires blob soft delete, blob versioning and change feed; the PITR retention must be at least one day less than the soft delete retention. It cannot restore container deletions, append or page blobs, or archived blobs.
```powershell
# -TimeToRestore is a UTC value
Restore-AzStorageBlobRange -ResourceGroupName rg -StorageAccountName acct -TimeToRestore (Get-Date).ToUniversalTime().AddHours(-6)
# Ranges are container/prefix, start inclusive and end exclusive
$range = New-AzStorageBlobRangeToRestore -StartRange "data/2026/" -EndRange "data/2027/"
Restore-AzStorageBlobRange -ResourceGroupName rg -StorageAccountName acct -BlobRestoreRange $range -TimeToRestore (Get-Date).ToUniversalTime().AddHours(-6)
```
- Azure Backup operational backup keeps data local to the storage account and manages point-in-time restore and its prerequisites for you; vaulted backup copies data to a Backup vault on a schedule.

## Amazon S3
- S3 Versioning keeps prior versions and Object Lock can protect them; restoring an older version means copying it over the current object (`aws s3api copy-object` with a version-qualified `--copy-source`). The AWS user guide is not readable from the documentation repositories used for this check, so confirm version-ID syntax, delete-marker behaviour and AWS Backup continuous-backup limits for S3 in the current AWS documentation.

## Google Cloud Storage
- Object versioning keeps noncurrent versions and soft delete keeps deleted objects recoverable for a retention period. Confirm the default retention period and the restore command in the current Cloud Storage documentation.

## Gotchas
- Versioning without lifecycle rules quietly multiplies storage costs; Azure PITR retention does not affect how long versions are kept, so use a lifecycle policy to remove old versions.
- An attacker with account-level rights can delete versions or the account; versioning is not a backup. Add immutable storage policies or a copy in another account.
- Azure PITR restores ranges of block blobs and reverts writes and deletes within them; it does not restore a deleted container.

## Verify
Overwrite and delete test objects, then restore them via the version/PITR path; confirm content and timestamps.

## Checked

Checked 2026-10-27 against the Azure Storage articles in MicrosoftDocs/azure-docs (point-in-time restore overview, point-in-time restore manage, blob soft delete overview) and the Azure Backup blob backup overview. Confirmed: PITR account type, tier and hierarchical-namespace limits, the three prerequisite features, the retention rule against soft delete, blob soft delete retention of 1 to 365 days, `Restore-AzStorageBlobRange` with a UTC `-TimeToRestore`, container/prefix ranges with an exclusive end, and the operational versus vaulted backup distinction. The Amazon S3 and Google Cloud Storage details were removed because those documents are not readable from the repositories used here; the skill now points to the vendor documentation for them.

Method: documentation only; no commands were run.
