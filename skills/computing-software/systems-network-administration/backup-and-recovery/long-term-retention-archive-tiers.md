---
id: computing-software.systems-network-administration.backup-and-recovery.long-term-retention-archive-tiers
name: long-term-retention-archive-tiers
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [long-term-retention, glacier-deep-archive, archive-tier, retention-policy, s3-lifecycle, azure-archive]
level: practitioner
status: docs-checked
description: "Keep long-term backup retention in cold cloud tiers (S3 Glacier, Deep Archive, Azure Archive): minimum durations, retrieval behaviour and planning."
sources:
  - https://docs.aws.amazon.com/AmazonS3/latest/userguide/storage-class-intro.html
  - https://learn.microsoft.com/en-us/azure/storage/blobs/access-tiers-overview
  - https://helpcenter.veeam.com/docs/backup/vsphere/archive_tier.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Long-term retention in archive tiers

**Goal:** monthly/yearly restore points kept for years in cold storage, with known retrieval time and cost. For prices, see each vendor's pricing page.

## Tier facts (from the vendor docs)
| Tier | Minimum storage duration | Retrieval |
|---|---|---|
| S3 Glacier Instant Retrieval | 90 days | millisecond access; per-GB retrieval fees |
| S3 Glacier Flexible Retrieval | 90 days | minutes to hours; restore the object first |
| S3 Glacier Deep Archive | 180 days | hours; restore the object first |
| Azure Blob Archive | 180 days recommended | offline; rehydrate to hot, cool or cold first, up to 15 hours depending on priority |

- Glacier Flexible Retrieval and Deep Archive each add 40 KB of metadata per archived object (32 KB at the archive rate, 8 KB at the S3 Standard rate), so many tiny objects are inefficient.
- Azure charges an early deletion fee if a blob leaves the archive tier before 180 days (the docs' example: removed at day 45, charged for the remaining 135 days). Soft delete delays the "deleted" moment until its retention expires. Copy Blob can rehydrate without the early deletion penalty but you pay capacity for both blobs. The archive tier is supported only for LRS, GRS and RA-GRS accounts, and lifecycle management policies cannot rehydrate a blob.
- S3: these storage classes have minimum storage durations and retrieval fees, so they suit rarely accessed data.

## Patterns
- **S3 lifecycle rule**: transition a prefix such as `backups/monthly/` to `DEEP_ARCHIVE` after a delay you choose and expire it after your retention period. Scope with prefixes or tags.
- **Veeam archive tier** (scale-out backup repository): an object storage repository added as a single archive extent; supported types listed are Amazon S3 Glacier, S3-compatible storage with data archiving, Microsoft Azure Archive Storage and Veeam Data Cloud Vault Archive. Veeam describes it as useful for data accessed no more than once a quarter.
- Pair with immutability (for example S3 Object Lock) where required over the retention period.

## Plan retrieval
- Test a restore from archive once a year and time it.
- Budget retrieval and egress cost per TB from the vendor's pricing page.
- Keep the catalogue/index (backup server configuration) outside the archive so you know what to fetch.

## Gotchas
- Check how your backup product handles chains before archiving; archive only restore points that can be restored independently of unarchived data (product-specific, read its archive tier documentation).
- Format longevity: keep a backup software version able to read old archives.

## Verify
Bucket inventory shows expected storage classes, and an annual timed restore from the archive tier succeeds.

## Checked

2026-11-09. Confirmed against the Amazon S3 storage classes page (Glacier IR/Flexible/Deep Archive minimum durations 90/90/180 days, 40 KB metadata, retrieval fees), the Azure access tiers overview (180-day archive minimum, early deletion example, up to 15 hours rehydration, Copy Blob, LRS/GRS/RA-GRS only) and the Veeam Archive Tier page (supported repository types, quarterly-access use case). Partial read of the Veeam page (first part only). Removed: GCS Archive row and 365 days, specific S3 retrieval hour ranges, "high priority under 1 h for under 10 GB", the 2555-day example, Azure Backup vault-archive claim, SOBR proxy-appliance and non-incremental statements.

Method: documentation only; no commands were run.
