---
id: computing-software.cloud-infrastructure-engineering.azure.azure-storage-lifecycle
name: azure-storage-lifecycle
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, azure-storage, blob-storage, lifecycle-management, access-tiers, hot-tier, cool-tier, cold-tier, archive-tier, smart-tier, last-access-time-tracking, daysaftermodificationgreaterthan, blob-versioning, snapshots, soft-delete, immutability, worm, legal-hold, rehydration, early-deletion-fee, blob-inventory, data-retention, adls-gen2]
level: practitioner
status: docs-checked
description: "Manage Azure Blob lifecycle: Hot/Cool/Cold/Archive tiers, lifecycle policy rules on modification or last-access time, versions and snapshots cleanup, early-deletion fees and archive rehydration."
sources: ["https://learn.microsoft.com/azure/storage/blobs/access-tiers-overview", "https://learn.microsoft.com/azure/storage/blobs/lifecycle-management-overview", "https://learn.microsoft.com/azure/storage/blobs/lifecycle-management-policy-structure", "https://learn.microsoft.com/azure/storage/blobs/archive-rehydrate-overview", "https://learn.microsoft.com/azure/storage/common/storage-redundancy"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Azure Storage lifecycle — tier, expire and clean versions on purpose

**Goal:** blob data moves to the cheapest tier its reads allow, is deleted when
retention says, and versions/snapshots don't silently double the bill — without paying
early-deletion penalties or stranding data in Archive when someone needs it.

## 1. Tiers and their costs
| Tier | Min. retention (early-deletion charge) | Read |
|---|---|---|
| Hot | — | online |
| Cool | 30 days | online, per-GB read fee |
| Cold | 90 days | online, higher read fee |
| Archive | 180 days | **offline**: rehydrate first |
- Tier is per blob (block blobs only); the account's default access tier can be Hot, Cool or Cold.
- The archive tier is not supported for ZRS, GZRS or RA-GZRS accounts.
- **Smart tier** moves data between hot, cool and cold automatically based on usage; see the Microsoft smart tier article for its current status and limits before choosing it over hand-written rules.

## 2. Write the policy
Lifecycle management is one JSON policy per storage account, written in full (partial updates are not supported):
```json
{"rules": [
 {"name": "logs-tiering", "enabled": true, "type": "Lifecycle",
  "definition": {
   "filters": {"blobTypes": ["blockBlob"], "prefixMatch": ["logs/"]},
   "actions": {
    "baseBlob": {
     "tierToCool":    {"daysAfterModificationGreaterThan": 30},
     "tierToCold":    {"daysAfterModificationGreaterThan": 90},
     "tierToArchive": {"daysAfterModificationGreaterThan": 180, "daysAfterLastTierChangeGreaterThan": 7},
     "delete":        {"daysAfterModificationGreaterThan": 2555}},
    "version":  {"tierToCold": {"daysAfterCreationGreaterThan": 30}, "delete": {"daysAfterCreationGreaterThan": 90}},
    "snapshot": {"delete": {"daysAfterCreationGreaterThan": 90}}}}}
]}
```
Apply: `az storage account management-policy create --account-name <ACCOUNT> -g <RG> --policy @policy.json`
(the policy is written in full, so manage the whole document in IaC).
- `prefixMatch` starts with the **container name** (`logs/` matches container `logs`).
- `blobIndexMatch` filters on blob index tags — useful for per-object retention classes.
- `daysAfterLastTierChangeGreaterThan` prevents bouncing a just-rehydrated blob straight back to Archive.

## 3. Access-time based rules
Enable **last access time tracking** on the account, then use
`daysAfterLastAccessTimeGreaterThan` with `enableAutoTierToHotFromCool: true` to move
blobs back to Hot when read. That action moves a blob from Cool to Hot only once in 30 days, to protect against repeated early-deletion charges, and has no effect on blobs set to Cool before the rule was added.

## 4. Versions, snapshots and soft delete
- **Blob versioning** keeps every overwrite; without a `version` delete action, a
  frequently rewritten blob accumulates unbounded versions.
- **Soft delete** (blobs and containers, 1-365 days) is a safety net, not retention:
  soft-deleted data is billed at its tier's rate.
- Point-in-time restore depends on versioning + change feed + soft delete; lifecycle
  deletes inside the restore window weaken it — keep version-deletion ≥ restore window.

## 5. Retention that must hold
- **Immutability policies** (time-based WORM or legal hold) at container or version
  level. Locked time-based policies cannot be shortened. The lifecycle delete action does not work on blobs in an immutable container.
- Version-level immutability is not supported on hierarchical-namespace (ADLS Gen2) accounts, and blob versioning is unavailable there; check the feature support table for lifecycle on HNS accounts.

## 6. Rehydration
`az storage blob set-tier --tier Hot --rehydrate-priority Standard` (may take up to 15 h for objects under 10 GB) or
`High` (may complete in under an hour for objects under 10 GB, at higher cost). Or **copy** the archived blob to an online tier. Plan restore drills — Archive
reads are never instant.

## Gotchas
- An early-deletion penalty applies if a blob is deleted, overwritten or moved to another tier before the tier's minimum number of days.
- A new or changed policy can take up to 24 h to start acting; the policy then processes objects periodically.
- Per-blob transaction costs make tiering millions of tiny blobs uneconomic; aggregate first.
- Access tiers cannot be set on append or page blobs; lifecycle supports `blockBlob` and `appendBlob` blob types and page blobs are not supported by lifecycle delete.

## Verify
- [ ] Blob inventory report shows bytes by tier, version and snapshot counts trending as intended.
- [ ] Every account with versioning has a `version` delete action consistent with the restore window.
- [ ] Archive rules include `daysAfterLastTierChangeGreaterThan`; a rehydration drill met the RTO.
- [ ] Modelled early-deletion and transaction costs < tiering savings.
- [ ] `az storage account management-policy show` matches IaC exactly.

## Checked

2026-10-24, against MicrosoftDocs/azure-docs (storage/blobs access-tiers-overview, lifecycle-management-overview, lifecycle-management-policy-structure, archive-rehydrate-overview, storage/common/storage-redundancy, immutable-storage-overview): minimum retention days for cool (30), cold (90) and archive (180), early-deletion penalty rule, default access tier options, archive not supported on ZRS, GZRS or RA-GZRS, tiering limited to block blobs, up-to-24-hour policy delay, `enableAutoTierToHotFromCool` behaviour (once in 30 days), `daysAfterLastTierChangeGreaterThan`, rehydration priorities (15 h and under one hour for objects under 10 GB), immutable-container delete limit. Removed the unconfirmed 100-rule maximum, the per-24-hour access-time batching claim, and the preview-date and Cool-to-Archive worked example. The soft-delete 1-365 day range is confirmed in the soft delete articles.

Method: documentation only; no commands were run.
