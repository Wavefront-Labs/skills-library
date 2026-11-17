---
id: computing-software.cloud-infrastructure-engineering.azure.blob-lifecycle-policy-run-timing-and-troubleshooting
name: blob-lifecycle-policy-run-timing-and-troubleshooting
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, blob-storage, lifecycle-run, lifecycle-troubleshooting, lifecyclepolicycompleted, lifecycle-management]
level: practitioner
status: docs-checked
description: "Debug blob lifecycle management: run frequency and first-run delay, LifecyclePolicyCompleted events, prefix and filter mistakes, versions/snapshots and blocked actions."
sources: ["https://learn.microsoft.com/azure/storage/blobs/lifecycle-management-overview", "https://learn.microsoft.com/azure/storage/blobs/lifecycle-management-policy-structure", "https://learn.microsoft.com/azure/storage/blobs/lifecycle-management-policy-configure", "https://learn.microsoft.com/azure/event-grid/event-schema-blob-storage"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Lifecycle policy timing and troubleshooting

**Goal:** know when lifecycle rules actually run and why blobs weren't tiered or deleted.

## Timing
- An active policy processes objects periodically. After you add or edit rules, it can take up to **24 hours** for the change to take effect and
  for the first run to start. A run is interrupted if you change the policy.
- Track completion with the Event Grid event **Microsoft.Storage.LifecyclePolicyCompleted** (a summary report with the policy run's results):
```bash
az eventgrid system-topic event-subscription create -g rg --system-topic-name st-events -n lifecycle-done \
  --endpoint <webhook-or-function> --included-event-types Microsoft.Storage.LifecyclePolicyCompleted
```

## Common rule mistakes
```json
{ "rules": [ { "name": "logs-to-cool", "enabled": true, "type": "Lifecycle",
  "definition": {
    "filters": { "blobTypes": ["blockBlob"], "prefixMatch": ["logs/app1/"] },
    "actions": { "baseBlob": { "tierToCool": { "daysAfterModificationGreaterThan": 30 },
                               "delete": { "daysAfterModificationGreaterThan": 365 } },
                 "version":  { "delete": { "daysAfterCreationGreaterThan": 90 } },
                 "snapshot": { "delete": { "daysAfterCreationGreaterThan": 90 } } } } } ] }
```
- `prefixMatch` must start with the **container name** (`logs/app1/`), not just the folder.
- `blobTypes` is required and takes `blockBlob` or `appendBlob`; page blobs aren't supported. Tiering actions are not supported on append blobs.
- `daysAfterLastAccessTimeGreaterThan` needs **last access time tracking** enabled on the account first.
- With versioning on, deleting the base blob creates a previous version - add `version` actions or capacity never drops.
- The delete action does not work on blobs in an immutable container.
- Rehydrating a blob does not update its last-modified or last-access time, so a tier-to-archive rule can move it straight back; add `daysAfterLastTierChangeGreaterThan` to that action.
- `blobIndexMatch` filters need blob index tags; each rule allows up to 10 prefixes and up to 10 index tag conditions. Index tags are not integrated with lifecycle management on HNS accounts.

## Check what happened
- Blob properties (`az storage blob show --query properties.blobTier`) and `accessTierChangeTime`.
- Policy JSON currently applied: `az storage account management-policy show -g rg --account-name st`.

## Verify
- [ ] LifecyclePolicyCompleted events arrive after runs with the expected results; capacity by tier trends as designed.

## Checked

2026-10-24, against MicrosoftDocs/azure-docs (lifecycle-management-overview, lifecycle-management-policy-structure, lifecycle-management-policy-configure, event-grid/event-schema-blob-storage): up-to-24-hour delay for new or edited rules, periodic execution, LifecyclePolicyCompleted event name and `BlobDataManagement/LifeCycleManagement/SummaryReport` subject, blobTypes values, append and page blob limits, immutable-container delete limit, prefix and tag-condition limits, `daysAfterLastTierChangeGreaterThan` guidance, `az storage account management-policy create --policy @file`. Removed the unconfirmed once-a-day cadence, the claim that archive-to-other-tier is not possible, per-action counts in the event, and the StorageBlobLogs remark.

Method: documentation only; no commands were run.
