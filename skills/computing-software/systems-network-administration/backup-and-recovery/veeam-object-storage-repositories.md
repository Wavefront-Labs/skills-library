---
id: computing-software.systems-network-administration.backup-and-recovery.veeam-object-storage-repositories
name: veeam-object-storage-repositories
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [veeam, veeam-object-storage, s3, azure-blob, object-lock, capacity-tier, direct-to-object]
level: advanced
status: docs-checked
description: "Add S3, S3-compatible and Azure Blob object storage repositories to Veeam, direct or as SOBR capacity/archive tiers, with object lock immutability and cost traps."
sources:
  - https://helpcenter.veeam.com/docs/backup/vsphere/object_storage_repository.html
  - https://helpcenter.veeam.com/docs/backup/vsphere/capacity_tier.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Veeam object storage repositories

## Supported types
Veeam Data Cloud Vault, Amazon S3 / S3 Glacier / AWS Snowball Edge, S3 compatible (including with data archiving), Google Cloud, IBM Cloud, Wasabi, Microsoft Azure Blob / Azure Archive / Azure Data Box, and 11:11 Cloud Object Storage.

## Uses
- Target for backup jobs and backup copy jobs (also a source location for backup copy jobs), file backup jobs, VMware Cloud Director VM backups, Veeam Agent backups, configuration database backups and several plug-in backups.
- Part of a scale-out backup repository as performance tier, capacity tier (offloads existing backup data to object storage) or archive tier (infrequently accessed data moved from the capacity tier).
- File backup job backups cannot be kept in object storage that is a performance extent of a scale-out repository.

## Connection modes
For vSphere, a VMware backup proxy transfers data (Hyper-V: on-host or off-host proxy); a mount server processes guest OS applications and item recovery. A proxy connects either **direct** (the default) or **through gateway servers**; choose on the Account step of the Object Storage Repository wizard.

## Other documented features
- **Block reuse:** synthetic full backups, file merges and clustered-disk backups from Veeam Agent for Windows reuse existing blocks, so stored size can be smaller than logical size. Active fulls and incrementals do not reuse blocks.
- **Multiple buckets (S3 compatible):** child buckets are provisioned automatically, with mapping metadata kept in a master bucket under a prefix; the number of per-machine chains per child bucket is set in the repository settings.
- **Read-only access:** the "Add repository as a read-only option" lets a second backup server restore from a repository owned by another; nothing is written or locked.

## Checked
Date: 2026-11-03. Confirmed against the Veeam Help Center pages "Object Storage Repositories" and "Capacity Tier" (build 13.x).
Removed (not on those pages): Object Lock-at-creation and default-retention advice, IAM policy and Veeam Ready claims, menu path, "direct-to-object v12+", 1 MB/4 MB block size and PUT request claims, the "up to 10 days" padding, egress and lifecycle-rule warnings, Verify section. Immutability details live on the separate "Immutability for Object Storage Repositories" page, which was not read.
Method: documentation only; no commands were run.
