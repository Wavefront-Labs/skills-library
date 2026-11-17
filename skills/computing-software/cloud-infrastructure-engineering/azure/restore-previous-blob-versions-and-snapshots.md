---
id: computing-software.cloud-infrastructure-engineering.azure.restore-previous-blob-versions-and-snapshots
name: restore-previous-blob-versions-and-snapshots
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, blob-storage, promote-version, restore-previous-version, blob-versioning, blob-snapshots, data-recovery]
level: practitioner
status: docs-checked
description: "Recover overwritten or deleted blobs: undelete soft-deleted versions and snapshots, promote a previous version or snapshot over the base blob."
sources: ["https://learn.microsoft.com/azure/storage/blobs/soft-delete-blob-manage", "https://learn.microsoft.com/azure/storage/blobs/snapshots-manage-dotnet"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Restore previous blob versions and snapshots

**Goal:** get yesterday's file back after an overwrite or delete, without making things worse.

## Soft-deleted blob with versioning enabled
In the portal, select the soft-deleted blob, open the **Versions** tab, pick the version to promote and select
**Make current version**. Undelete restores any soft-deleted versions or snapshots but does **not** restore the base
blob: to restore the base blob you must promote a previous version.
```bash
az storage blob undelete --account-name <account> -c docs -n reports/q3.xlsx --auth-mode login
```

## Snapshots
- To promote a soft-deleted snapshot, first restore the blob's soft-deleted snapshots (Undelete, even if the base blob
  isn't deleted), then select the snapshot and use **Promote snapshot** to overwrite the base blob.
- A copy operation can also promote a snapshot over its base blob, as long as the base blob is in an online tier (hot or
  cool). The snapshot remains; the destination is overwritten with a writable copy.

## Gotchas
- Archived blobs can't be read or modified; rehydrate first. Snapshots aren't supported for archived blobs.
- Seeing soft-deleted items needs the account owner or a Storage Blob Data Owner, Contributor or Reader role.
- Pick the version to promote by the incident time, not by position in the list.

## Verify
- [ ] Users confirm the restored file; incident notes record the version or snapshot used.

## Checked
2026-10-31. Confirmed against Learn "Manage and restore soft-deleted blobs" and "Create and manage blob snapshots with
.NET": Versions tab and Make current version, Undelete behaviour, Promote snapshot, copy-promote rule for online tiers,
roles, archived blob restrictions. Removed: the `copy start` with `?versionId=` and `?snapshot=` URLs (the syntax is not
on the pages read), the point-in-time restore prerequisites, the version-promote capacity-billing note.
Method: documentation only; no commands were run.
