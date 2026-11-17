---
id: computing-software.cloud-infrastructure-engineering.azure.blob-and-container-soft-delete-and-undelete
name: blob-and-container-soft-delete-and-undelete
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, soft-delete, blob-soft-delete, container-soft-delete, undelete, blob-data-protection, recovery]
level: practitioner
status: docs-checked
description: "Enable blob and container soft delete with sensible retention, and recover deleted or overwritten blobs and containers, including on HNS accounts."
sources: ["https://learn.microsoft.com/azure/storage/blobs/soft-delete-blob-overview", "https://learn.microsoft.com/azure/storage/blobs/soft-delete-container-overview", "https://learn.microsoft.com/azure/storage/blobs/soft-delete-blob-enable", "https://learn.microsoft.com/azure/storage/blobs/soft-delete-container-enable", "https://learn.microsoft.com/azure/storage/blobs/data-protection-overview"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Blob and container soft delete and undelete

**Goal:** an accidental delete (by a person or a buggy job) is recoverable for N days without a
backup restore.

## Enable
```bash
az storage account blob-service-properties update -g rg --account-name stdata \
  --enable-delete-retention true --delete-retention-days 14 \
  --enable-container-delete-retention true --container-delete-retention-days 14
```
Retention 1–365 days for both blob and container soft delete. Microsoft's basic baseline: an Azure Resource
Manager lock on the account, container soft delete and blob soft delete, each with a minimum retention of seven days.

## What it protects
| Event | Protected by |
|---|---|
| Delete Blob | Blob soft delete (or versioning) |
| Overwrite (Put Blob) | Blob soft delete creates a soft-deleted *snapshot* (non-versioned accounts); versioning creates a version |
| Delete Container | Container soft delete |
| Delete storage account | Not protected — use a resource lock |

## Recover a blob
```bash
az storage blob list --account-name stdata -c data --include d --prefix reports/ \
  --query "[?deleted].{name:name, deletedOn:properties.deletedTime}" -o table --auth-mode login
az storage blob undelete --account-name stdata -c data -n reports/q3.xlsx --auth-mode login
```
Undelete restores the blob **and all its soft-deleted snapshots**. With versioning on, restoring a
previous version (promoting it to the current version) is the recovery path; see the blob versioning documentation.

## Recover a container
```bash
az storage container list --account-name stdata --include-deleted --query "[?deleted].{n:name,v:version}" -o table
az storage container restore --account-name stdata -n data --deleted-version <version>
```
A container can be restored only to its original name: if a container with the same name was created after the delete, rename or delete the conflicting container first.

## HNS (ADLS Gen2) specifics
Blob soft delete and container soft delete are both available on accounts with a hierarchical namespace. Deleting a directory
soft-deletes the directory and all its contents, and the ACL of a restored blob remains intact. The soft-deleted overwrite snapshots described above do not apply to HNS accounts.

## Gotchas
- Soft-deleted data is billed at the same rate as active data, in the same tier.
- Bulk delete jobs plus long retention mean large hidden capacity; choose a retention that matches recovery needs.
- Soft delete alone is not a defence against a principal who can change retention settings; for ransomware-style scenarios Microsoft suggests adding Azure Backup.

## Verify
- [ ] `az storage account blob-service-properties show --account-name stdata --query "{blob:deleteRetentionPolicy, container:containerDeleteRetentionPolicy}"`.
- [ ] Test: delete a canary blob, list with `--include d`, undelete, compare MD5.

## Checked

2026-10-24, against the MicrosoftDocs/azure-docs repository (storage/blobs articles, main branch as of that date): retention range 1-365 days for blob and container soft delete; Microsoft's basic baseline (lock, container and blob soft delete, 7-day minimum); overwrite behaviour with soft delete (soft-deleted snapshot, not on HNS); container restore only to its original name; billing at the same rate and tier as active data; CLI parameters `--enable-delete-retention`, `--delete-retention-days`, `--enable-container-delete-retention`. Removed unconfirmed HNS path-level CLI commands, version copy syntax, lifecycle and metric remarks.

Method: documentation only; no commands were run.
