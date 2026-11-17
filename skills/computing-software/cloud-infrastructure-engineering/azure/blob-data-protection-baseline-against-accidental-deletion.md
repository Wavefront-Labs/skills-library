---
id: computing-software.cloud-infrastructure-engineering.azure.blob-data-protection-baseline-against-accidental-deletion
name: blob-data-protection-baseline-against-accidental-deletion
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, blob-storage, data-protection-baseline, accidental-deletion, recover-deleted-storage-account, soft-delete, versioning]
level: practitioner
status: docs-checked
description: "Apply Microsoft's recommended Blob Storage data protection baseline in one pass: soft delete, versioning, change feed, PITR, locks, backup, and deleted-account recovery."
sources: ["https://learn.microsoft.com/azure/storage/blobs/data-protection-overview", "https://learn.microsoft.com/azure/storage/common/storage-account-recover", "https://learn.microsoft.com/azure/storage/blobs/point-in-time-restore-overview"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Blob data protection baseline

**Goal:** any account holding real data survives a deleted container, an overwritten blob, a malicious delete
script and a deleted storage account.

## Baseline (general-purpose v2)
```bash
az storage account blob-service-properties update -g rg --account-name st \
  --enable-delete-retention true --delete-retention-days 14 \
  --enable-container-delete-retention true --container-delete-retention-days 14 \
  --enable-versioning true --enable-change-feed true \
  --enable-restore-policy true --restore-days 7
az lock create -g rg -n lock-st --lock-type CanNotDelete --resource st --resource-type Microsoft.Storage/storageAccounts
```
| Layer | Protects against |
|---|---|
| Container soft delete | Deleted container |
| Blob soft delete | Deleted blob/version/snapshot |
| Versioning | Overwrites, deletes |
| Change feed + PITR | Bulk corruption: restore block blobs in a range to a point in time |
| CanNotDelete lock | Account deletion via ARM |
| Azure Backup | Broader loss such as account deletion or ransomware, in addition to in-account features |
| Immutability (where required) | Regulatory WORM |
The point-in-time restore retention must be at least one day less than the blob soft delete retention (and the change feed retention).
Microsoft's own basic baseline is the lock plus container soft delete plus blob soft delete; the other layers are optional additions.

## Deleted storage account
A deleted account can be recovered (portal) if it was deleted within the past 14 days, was created with the Azure Resource
Manager deployment model, the resource group still exists and no new account with the same name has been created. A lock prevents most of this scenario.

## At scale
Enforce the settings with Azure Policy or infrastructure-as-code modules so every new account gets the same baseline.

## Costs and trade-offs
- Versions and soft-deleted data are billed capacity; high-churn workloads (frequent overwrites) grow capacity -
  add lifecycle rules for old versions.
- HNS (ADLS Gen2) accounts: Microsoft lists blob versioning and point-in-time restore as not available there; soft delete and container-level immutability are available. Snapshots are the alternative to versioning.

## Verify
- [ ] Delete a test container and blob in non-prod; recover both; PITR test restore of a prefix succeeds.

## Checked

2026-10-24, against MicrosoftDocs/azure-docs (data-protection-overview, storage-account-recover, point-in-time-restore-overview): basic baseline recommendation; 7-day minimum retention advice; deleted-account recovery conditions (14 days, Resource Manager model, resource group exists, name unused); PITR retention at least one day below soft delete; HNS availability (versioning and PITR not available). Removed unconfirmed Resource Graph and shared-key remarks and the claim that Azure Backup is the only vaulted option.

Method: documentation only; no commands were run.
