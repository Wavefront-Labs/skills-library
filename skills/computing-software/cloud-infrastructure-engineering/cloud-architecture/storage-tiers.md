---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.storage-tiers
name: storage-tiers
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, storage-selection, storage-tiers, access-tiers, storage-classes, intelligent-tiering]
level: practitioner
status: docs-checked
description: "Pick storage classes and access tiers: hot, cool, cold and archive trade-offs, minimum durations, retrieval charges, early deletion and automatic tiering."
sources: ["https://aws.amazon.com/s3/storage-classes/", "https://learn.microsoft.com/azure/storage/blobs/access-tiers-overview", "https://cloud.google.com/storage/docs/storage-classes"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Storage classes and access tiers

## The trade-off
Lower storage price buys higher retrieval or access cost, a minimum storage duration and, for some archive tiers, slower
retrieval. All three vendors document the same shape; the names and durations differ.
| Tier | AWS S3 | Azure Blob | GCS | Min duration |
|---|---|---|---|---|
| hot | Standard | Hot | Standard | none |
| infrequent | Standard-IA / One Zone-IA | Cool | Nearline | 30 days (all) |
| cold | Glacier Instant Retrieval | Cold | Coldline | 90 days (all) |
| archive | Glacier Flexible Retrieval (90 days) / Deep Archive (180 days) | Archive (offline, 180 days) | Archive (online, 365 days) | see cells |

Notes from the vendor pages:
- S3 Glacier Instant Retrieval returns data in milliseconds; Flexible Retrieval takes minutes to hours and Deep Archive
  hours (the S3 page gives both "within 12 hours" and "12-48 hours" for Deep Archive, so read the current retrieval
  options before promising a restore time).
- Azure Archive is offline: a blob cannot be read or modified until it is rehydrated to Hot, Cool or Cold, which can
  take up to 15 hours depending on priority. Archive is only available on LRS, GRS and RA-GRS accounts, cannot be the
  account default tier, and tiering applies to block blobs only.
- GCS Archive is not offline: the page states data is available within milliseconds, with a 365-day minimum.
- S3 One Zone-IA keeps data in one Availability Zone, so it can be lost if that zone is lost; use it for re-creatable
  data or secondary copies.

## Steps
1. **Measure access** before choosing: how often and how recently objects are read, and how long they must be kept.
2. **Unknown or changing patterns**: S3 Intelligent-Tiering (small monthly monitoring and automation charge, no
  retrieval charge; moves objects to Infrequent after 30 days and Archive Instant Access after 90 days without access;
  objects under 128 KB are never auto-tiered and are always charged at Frequent Access rates), Azure smart tier, or GCS
  Autoclass.
3. **Known patterns**: lifecycle rules by age (S3 Lifecycle, Azure lifecycle management, GCS Object Lifecycle
  Management), with transitions timed after the minimum duration of the tier you leave.
4. **Small objects**: S3 Glacier Instant Retrieval has a 128 KB minimum object size, and Glacier Flexible Retrieval and
  Deep Archive add about 40 KB of metadata per archived object. Aggregate tiny objects before archiving them.
5. **Archive retrieval**: plan restore times for DR or legal requests. In Azure, lifecycle policies cannot rehydrate an
  archived blob; use Copy Blob (recommended) or Set Blob Tier.

## Gotchas
- Early deletion charges: moving, overwriting or deleting before the minimum duration is billed for the remaining days
  (Azure: prorated, for example a Cool blob deleted at 21 days is charged 9 days). Azure soft delete defers the penalty
  until the retention period ends.
- Azure bills a move to a cooler tier as a write operation per 10,000 and a move to a warmer tier as read operations
  plus data retrieval from the source tier, so mass tier changes of small blobs cost money.
- Changing a bucket's default GCS storage class does not change existing objects.
- Prices change: use each vendor's pricing page rather than copying figures.

## Verify
- [ ] Lifecycle or auto-tiering on every large bucket/container.
- [ ] Retrieval time for archive data meets the restore requirement.

## Checked
2026-11-08. Confirmed against the S3 storage classes page, the Azure blob access tiers overview and the GCS storage
classes page (all read in full): tier names, 30/90/180/365-day minimums, Intelligent-Tiering behaviour and 128 KB rule,
Glacier IR 128 KB minimum, 40 KB archive metadata, One Zone loss note, Azure 15-hour rehydration and archive
restrictions, early-deletion proration, GCS Autoclass and archive latency. Removed: S3 Standard-IA 128 KB minimum (not
on the page; the page ties 128 KB to Glacier IR and Intelligent-Tiering), "Deep Archive standard up to 12 hours"
(page contradicts itself), Storage Lens/Class Analysis/blob inventory/usage-log tooling (not on these pages), and the
lifecycle example numbers.
Method: documentation only; no commands were run.
