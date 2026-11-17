---
id: computing-software.cloud-infrastructure-engineering.azure.blob-version-level-immutability-worm
name: blob-version-level-immutability-worm
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, blob-storage, version-level-immutability, container-level-worm, legal-hold, time-based-retention, compliance]
level: advanced
status: docs-checked
description: "Configure version-level WORM on Blob Storage: account/container defaults, per-blob retention and legal holds, locking, migration from container-level WORM and deletion limits."
sources: ["https://learn.microsoft.com/azure/storage/blobs/immutable-storage-overview", "https://learn.microsoft.com/azure/storage/blobs/immutable-policy-configure-version-scope", "https://learn.microsoft.com/azure/storage/blobs/data-protection-overview"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Version-level immutability (WORM)

**Goal:** compliance-grade write-once storage (for example broker-dealer record-keeping rules such as SEC 17a-4(f); confirm requirements with your compliance team) with per-blob retention, not one rule
for a whole container.

## Container-level vs version-level
- **Container-level WORM**: one time-based policy (and legal holds) for the whole container; supported on hierarchical-namespace accounts.
- **Version-level WORM**: policies can be set at account, container or version level; version-level WORM is not yet supported on hierarchical-namespace accounts.

## Enable
```bash
# account-level default (at creation)
az storage account create -g rg -n stworm -l westeurope --sku Standard_GRS --kind StorageV2 \
  --enable-alw true --immutability-period-in-days 2555 --immutability-state unlocked --allow-protected-append-writes true
# or container-level version-scoped immutability
az storage container-rm create -g rg --storage-account stworm -n records --enable-vlw true
```

## Per-blob retention and legal hold
```bash
az storage blob immutability-policy set --account-name stworm -c records -n trade-0001.json \
  --expiry-time 2033-10-18T00:00:00Z --policy-mode Unlocked --auth-mode login
az storage blob set-legal-hold --account-name stworm -c records -n trade-0001.json --legal-hold true --auth-mode login
```
- **Unlocked** policies can be shortened or removed - for testing only.
- **Locked** policies can't be shortened or removed (the retention period can only be extended) and are what make the policy compliant with SEC 17a-4(f) and similar regulations. Lock after validation.
- Legal holds have no expiry; remove explicitly when the matter closes.

## Migrate container-level to version-level
```bash
az storage container-rm migrate-vlw -g rg --storage-account stworm -n legacy-records
```
Migration can't be reversed, may take some time, and is limited to 10 containers at a time per storage account.

## Gotchas
- With a locked policy or legal hold in effect, the storage account is also protected from deletion, and containers with blobs can't be deleted - only
  plan this for data you truly must keep.
- `allowProtectedAppendWrites` (`--allow-protected-append-writes`) lets append blobs grow (logs) while existing blocks stay immutable.
- The lifecycle delete action does not work on blobs in an immutable container; capacity grows until retention expires - budget for it.
- Version-level WORM is not supported on hierarchical-namespace accounts; check the feature support table for other combinations.

## Verify
- [ ] Attempted overwrite/delete of a protected version is rejected; policy mode is Locked in prod.

## Checked

2026-10-24, against MicrosoftDocs/azure-docs (storage/blobs/immutable-storage-overview, immutable-policy-configure-version-scope, data-protection-overview): container-level vs version-level scope, HNS support (container-level only), locked and unlocked policy behaviour, `az storage account create --enable-alw --immutability-period-in-days --immutability-state --allow-protected-append-writes`, `az storage container-rm create --enable-vlw`, container migration limits (irreversible, 10 at a time), lifecycle delete limit, account deletion protection. Corrected the period flag name. The per-blob CLI commands (`az storage blob immutability-policy set`, `set-legal-hold`) and `migrate-vlw` follow the documented configure article; the 409 error code and the 'recommended model' claim were removed as unconfirmed.

Method: documentation only; no commands were run.
