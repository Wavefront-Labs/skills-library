---
id: computing-software.cloud-infrastructure-engineering.azure.set-blob-tier-manually-and-in-bulk
name: set-blob-tier-manually-and-in-bulk
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, access-tiers, set-blob-tier, batch-tier-change, tier-change, blob-batch, default-access-tier]
level: practitioner
status: docs-checked
description: "Change blob access tiers individually and at scale: Set Blob Tier, Blob Batch, AzCopy and lifecycle policies, with early-deletion and rehydration side effects."
sources: ["https://learn.microsoft.com/azure/storage/blobs/access-tiers-online-manage", "https://learn.microsoft.com/rest/api/storageservices/blob-batch", "https://learn.microsoft.com/azure/storage/blobs/access-tiers-overview"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Set blob tier manually and in bulk

**Goal:** move existing data to the right tier without early-deletion fees or a long rehydrate.

## Single blob
```bash
az storage blob set-tier --account-name <account> -c logs -n 2025/01/app.log --tier Cool --auth-mode login
```
Moving from a warmer tier to a cooler one is instantaneous, as is cold or cool to hot. Rehydrating from Archive to an
online tier (hot, cool or cold) can take up to 15 hours depending on the rehydration priority. You can't read or
modify an archived blob until it is rehydrated. Check a blob's tier with `properties.blobTier` and
`properties.blobTierInferred`.

## Bulk options
| Method | Best for |
|---|---|
| Lifecycle management policy | Large numbers of blobs, server-side |
| Blob Batch (SDK batch client) | Up to 256 subrequests per batch, request body max 4 MB |
| `azcopy set-properties` | Ad-hoc prefixes from a workstation |
| Loop over blobs calling Set Blob Tier | Small sets only |
```bash
azcopy set-properties "https://<account>.blob.core.windows.net/logs/2024/?<sas>" --block-blob-tier=Cool --recursive
```
- Blob Batch supports Set Blob Tier (block blobs) and Delete Blob only; subrequests are not atomic and each runs independently.
- For moving a large number of blobs the docs recommend a batch operation. The least privileged built-in role for Blob Batch is Storage Blob Data Contributor.

## Cost side effects (see the vendor's pricing page for amounts)
- Recommended minimum retention: Cool 30 days, Cold 90 days, Archive 180 days (general-purpose v2 accounts). Moving or
  deleting a blob earlier is charged an early deletion fee for the remaining days.
- Moving a blob to a warmer tier is billed as a read from the source tier; Copy Blob avoids the early-deletion
  penalty but incurs capacity charges for two blobs.
- Set Blob Tier can't archive a blob that uses an encryption scope.
- Metadata of archived blobs is charged at cool rates; snapshots aren't supported for archived blobs.

## Gotchas
- Access tiers apply to block blobs only, not append or page blobs.
- Soft-deleted blobs are not subject to the early deletion penalty until the retention period expires.

## Verify
- [ ] `az storage blob show ... --query "[properties.blobTier, properties.blobTierInferred]"` shows the intended tier.

## Checked
2026-10-31. Confirmed against Learn "Access tiers for blob data", "Set a blob's access tier" and the Blob Batch REST
reference: instant tier changes, 15-hour rehydration, minimum retention 30/90/180 days, block blobs only, 256-subrequest
and 4 MB limits, supported subrequests, non-atomic batches, role, billing notes, encryption scope restriction.
Removed: account default tier advice, lifecycle `daysAfterModificationGreaterThan: 0` timing, the Python/PowerShell
snippets, the `--rehydrate-priority` example and High-priority timing, and premium account statements.
Method: documentation only; no commands were run.
