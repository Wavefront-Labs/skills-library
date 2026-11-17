---
id: computing-software.systems-network-administration.backup-and-recovery.veeam-scale-out-backup-repository
name: veeam-scale-out-backup-repository
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [sobr, scale-out-backup-repository, veeam, capacity-tier, archive-tier, performance-tier, object-storage]
level: advanced
status: docs-checked
description: "Run a Veeam Scale-Out Backup Repository: performance extents, placement policy, capacity tier copy and move policies, archive tier, immutability and extent maintenance."
sources:
  - https://helpcenter.veeam.com/docs/backup/vsphere/sobr_add.html
  - https://helpcenter.veeam.com/docs/backup/vsphere/capacity_tier.html
  - https://helpcenter.veeam.com/docs/backup/vsphere/archive_tier.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Veeam Scale-Out Backup Repository

**Goal:** one logical repository made of tiers, so jobs target a single object while data moves between storage types.

## Tiers
- **Performance tier:** extents where jobs write. Object storage repositories can be used here too (File backup job backups cannot be kept on object storage used as a performance extent).
- **Capacity tier:** an extra tier for long-term storage; extents are cloud or on-premises object storage (Veeam Data Cloud Vault, S3 compatible, Amazon S3, AWS Snowball Edge, Azure Blob, Azure Data Box, IBM Cloud, Google Cloud, Wasabi, 11:11 Cloud Object Storage). The object storage repository must be added to Veeam before it can be a capacity extent.
- **Archive tier:** moves infrequently accessed data from the capacity tier to archive storage.

## Capacity tier operations
- **Move** inactive backup chains to capacity extents (also manually).
- **Copy** new backup files as soon as they are created.
- **Download** moved data back to performance extents.
- **Restore** from the capacity tier; after a disaster you can restore from it without recreating the scale-out repository, by importing object storage backups.
Useful when you are running out of space, when policy limits what you keep on extents, or to keep data on several sites.

## Adding one
Available through the console or the web UI; capacity extents appear in the wizard on the Capacity Tier step.

## Checked
Date: 2026-11-03. Confirmed against the Veeam Help Center pages "Capacity Tier", "Object Storage Repositories" and "Adding Scale-Out Backup Repositories".
Removed (not on those pages): placement policy descriptions, maintenance/evacuate/seal operations, the PowerShell example (cmdlets not verified), Glacier/Archive specifics, forever-incremental gotcha, Verify section.
Method: documentation only; no commands were run.
