---
id: computing-software.cloud-infrastructure-engineering.azure.blob-point-in-time-restore-for-block-blobs
name: blob-point-in-time-restore-for-block-blobs
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, point-in-time-restore, blob-pitr, blob-restore, change-feed, versioning, blob-data-protection]
level: advanced
status: docs-checked
description: "Enable and run point-in-time restore for block blobs: prerequisites (versioning, change feed, soft delete), restore ranges, duration, and what it can't undo."
sources: ["https://learn.microsoft.com/azure/storage/blobs/point-in-time-restore-overview", "https://learn.microsoft.com/azure/storage/blobs/point-in-time-restore-manage"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Point-in-time restore for block blobs

**Goal:** after ransomware-style overwrites or a bad bulk job, roll one or more containers back
to a timestamp in one operation.

## Prerequisites (all on the account)
- Blob **versioning**, **change feed**, **soft delete** enabled.
- The restore retention must be at least one day less than the soft delete (and change feed) retention (e.g. soft delete 14 d → restore up to 13 d).
- Standard general-purpose v2 accounts only; block blobs only (not append blobs, page blobs or premium block blobs); not supported on accounts with a hierarchical namespace. Only data in the hot and cool tiers can be restored.
```bash
az storage account blob-service-properties update -g rg --account-name stdata \
  --enable-versioning true --enable-change-feed true \
  --enable-delete-retention true --delete-retention-days 14 \
  --enable-restore-policy true --restore-days 13
```

## Run a restore
```bash
az storage blob restore -g rg --account-name stdata \
  --time-to-restore 2026-10-15T08:00:00Z \
  --blob-range data "" --blob-range finance "finance/z" --no-wait
az storage account show -g rg -n stdata --query blobRestoreStatus
```
- Ranges are lexicographic ranges of container and blob names; repeat `--blob-range` for each range (up to 10 ranges per restore); omit ranges to restore every container. Check the `az storage blob restore` reference for the exact range argument syntax.
- PowerShell: `Restore-AzStorageBlobRange` takes the restore point as a UTC date/time.

## During and after
- Restore time depends on the number of write and delete operations during the restore period. The operation is atomic: it either restores everything or fails, and reads and writes to the affected containers resume.

## Cannot restore
- Deleted containers (use container soft delete first, then PITR).
- Blobs in the archive tier (not restored).
- Append blobs, page blobs and premium block blobs.

## Gotchas
- The restore retention must be at least one day less than the change feed retention as well as the soft delete retention.
- Cost: versioning + change feed + soft delete storage; worth it only for high-value containers — consider vaulted blob backup for long retention.

## Verify
- [ ] `az storage account blob-service-properties show --query restorePolicy` shows enabled, days.
- [ ] Drill: in a test account, overwrite a set of blobs, restore to before the change, compare checksums.

## Checked

2026-10-24, against MicrosoftDocs/azure-docs (storage/blobs/point-in-time-restore-overview, point-in-time-restore-manage): prerequisites (soft delete, change feed, versioning), retention rule (at least one day below soft delete and change feed), supported account types and blob types, no HNS support, hot and cool tiers only, archive blobs not restored, deleted containers not restored, 10 ranges per restore, atomic restore, `az storage blob restore --time-to-restore` and `--blob-range`, `Restore-AzStorageBlobRange`. Removed the unconfirmed range syntax details, write-blocking and tag statements and the throughput remark.

Method: documentation only; no commands were run.
