---
id: computing-software.cloud-infrastructure-engineering.azure.storage-account-migration-gpv1-upgrade-and-region-move
name: storage-account-migration-gpv1-upgrade-and-region-move
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, storage-account, storage-account-migration, gpv1-upgrade, region-move, classic-storage-migration, azcopy]
level: practitioner
status: docs-checked
description: "Upgrade GPv1 and Blob storage accounts to GPv2 (retirement date, billing impact) and plan a move to another region with AzCopy and a cutover."
sources: ["https://learn.microsoft.com/azure/storage/common/storage-account-upgrade", "https://github.com/Azure/azure-storage-azcopy", "https://learn.microsoft.com/azure/storage/common/general-purpose-version-1-account-migration-overview"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Storage account migration: GPv1 upgrade, classic, region move

**Goal:** legacy storage accounts become GPv2 ARM accounts, and accounts that must change region
move without data loss.

## GPv1 / BlobStorage → GPv2 (in place, one-way)
```bash
az storage account update -g rg -n stlegacy --set kind=StorageV2 --access-tier Hot
```
- No downtime and no data loss; existing applications and tools keep working. A general-purpose v1 or Blob Storage account can be upgraded to GPv2 but not downgraded.
- Cost changes: GPv2 can have higher transactional costs, especially for workloads with many reads and writes. Estimate with your current usage patterns (Azure Pricing Calculator) before upgrading high-transaction accounts.
- Setting default tier `Cool` on upgrade re-tiers blobs without explicit tier → write charges for every blob.
- Microsoft scheduled general-purpose v1 retirement for October 13, 2026 (new GPv1 account creation was blocked from Q1 2026) and says remaining GPv1 accounts will be migrated to GPv2 automatically, which might raise billing. Check the GPv1 retirement overview for the current state of any account you still have.

## Region move (redeploy + copy)
A new account in the target region is created and the data copied across (account names are globally unique, so the new account needs a new name).
1. Deploy the target account from your IaC or an exported template with the new location and name.
2. Recreate the same settings (redundancy, network rules, CMK, lifecycle, versioning, private endpoints in the new region).
3. Copy data server-side:
```bash
azcopy copy "https://stsrc.blob.core.windows.net/?<sas>" "https://stdst.blob.core.windows.net/?<sas>" --recursive --s2s-preserve-access-tier
azcopy sync "https://stsrc.blob.core.windows.net/data?<sas>" "https://stdst.blob.core.windows.net/data?<sas>" --delete-destination=false   # delta pass before cutover
```
   Other services (file shares, queues, tables) need their own copy tooling; check each service's documentation.
4. Cutover: stop writers → final `azcopy sync` → switch connection strings / DNS CNAMEs (custom domains) → verify → keep source read-only for a rollback window → delete.

## Gotchas
- Blob index tags are copied only with `--s2s-preserve-blob-tags` (default false); `--s2s-preserve-access-tier` defaults to true.
- Archive-tier blobs can't be read until rehydrated to an online tier.
- SAS tokens and private endpoint DNS change with the new account name; plan app config changes.

## Verify
- [ ] `az storage account show --query kind` is `StorageV2`.
- [ ] After a region move: object counts and total bytes match (blob inventory reports on both).
- [ ] Apps read/write the new account; source has no transactions for a week before deletion.

## Checked

2026-10-24, against MicrosoftDocs/azure-docs (storage/common/storage-account-upgrade) and the Azure/azure-storage-azcopy source (release v10.34.1, 2026-10-22, cmd/copy.go and cmd/sync.go): GPv1 and Blob Storage upgrade (no downtime, no downgrade, possible transactional cost increase), retirement date October 13, 2026 with automatic migration, upgrade command `az storage account update --set kind=StorageV2 --access-tier`, AzCopy flags `--s2s-preserve-access-tier` (default true), `--s2s-preserve-blob-tags` (default false), `--recursive`, `--delete-destination`. Removed the classic-to-ARM section and the in-place region-move statement, which could not be confirmed against a current article, plus unconfirmed AzCopy scope claims.

Method: documentation only; no commands were run.
