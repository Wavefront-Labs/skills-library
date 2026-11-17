---
id: computing-software.cloud-infrastructure-engineering.azure.blob-versioning-vs-snapshots
name: blob-versioning-vs-snapshots
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, versioning, blob-versioning, blob-snapshots, previous-versions, lifecycle-management, blob-data-protection]
level: practitioner
status: docs-checked
description: "Choose between blob versioning and manual snapshots, enable versioning, restore a previous version, and cap version cost with lifecycle rules."
sources: ["https://learn.microsoft.com/azure/storage/blobs/versioning-overview", "https://learn.microsoft.com/azure/storage/blobs/versioning-enable", "https://learn.microsoft.com/azure/storage/blobs/snapshots-overview", "https://learn.microsoft.com/azure/storage/blobs/data-protection-overview"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Blob versioning vs snapshots

**Goal:** every overwrite and delete is reversible, without version sprawl doubling storage cost.

## Comparison
| | Versioning | Snapshots |
|---|---|---|
| Created | Automatically on every write/delete | Explicitly by app/script |
| Granularity | Account-wide (all containers) | Per blob, when you choose |
| Read-only point-in-time | Yes (`versionid`) | Yes (`snapshot`) |
| Required for | Point-in-time restore (a prerequisite) | Nothing |
| HNS (ADLS Gen2) | Not supported (versioning is unavailable on accounts with a hierarchical namespace) | Snapshots are Microsoft's alternative on HNS accounts |
Microsoft recommends versioning for continuous protection of overwrites and deletes; use snapshots for deliberate, application-driven checkpoints ("before migration run").

## Enable versioning
```bash
az storage account blob-service-properties update -g rg --account-name stdata --enable-versioning true
```
With versioning on, a delete makes the current version a previous version (no base blob) — the
blob "disappears" but is recoverable.

## Restore a previous version
```bash
# list versions with `az storage blob list --include v`, then promote one by copying it over the base blob (Copy Blob with the versionid)
```
Promoting a previous version by copying it over the base blob makes it the current version (history preserved); see the versioning documentation for the portal, PowerShell and SDK steps.

## Snapshots
```bash
az storage blob snapshot --account-name stdata -c data -n db.bak --auth-mode login
```
A blob that has snapshots cannot be deleted unless its snapshots are deleted with it. List Blobs returns snapshots only when asked to include them.

## Control cost with lifecycle
```json
{ "rules": [{ "name": "versions", "enabled": true, "type": "Lifecycle",
  "definition": { "filters": { "blobTypes": ["blockBlob"] },
    "actions": { "version": { "tierToCool": { "daysAfterCreationGreaterThan": 30 },
                              "delete": { "daysAfterCreationGreaterThan": 90 } },
                 "snapshot": { "delete": { "daysAfterCreationGreaterThan": 90 } } } } }] }
```
Billing: see the Pricing and billing section of the versioning and snapshot documentation; every write operation (except Put Block) on a block blob creates a new version.

## Gotchas
- Workloads that rewrite large files frequently (logs appended via full upload, Delta tables) explode version counts — exclude them via separate account or aggressive lifecycle.
- Microsoft recommends fewer than 1,000 versions per blob (and fewer than 1,000 snapshots per blob) because more increases list latency.
- Versioning doesn't protect against account deletion or a privileged user deleting versions — use immutability/legal hold or vaulted backup for that.

## Verify
- [ ] `az storage account blob-service-properties show --account-name stdata --query isVersioningEnabled`.
- [ ] Lifecycle policy includes `version` actions and version counts per blob stay under 1,000.

## Checked

2026-10-24, against MicrosoftDocs/azure-docs (storage/blobs/versioning-overview, snapshots-overview, versioning-enable, data-protection-overview, point-in-time-restore-overview): versioning not available on hierarchical-namespace accounts, snapshots as the alternative, versioning prerequisite for point-in-time restore, which write operations create versions (all except Put Block), fewer than 1,000 versions or snapshots per blob, `--enable-versioning`, lifecycle `version` and `snapshot` action keys with `daysAfterCreationGreaterThan`. Removed the wrong HNS 'Supported' entry, the object-replication claim, unconfirmed CLI listing and delete-snapshots syntax, and the block-deduplication billing statement.

Method: documentation only; no commands were run.
