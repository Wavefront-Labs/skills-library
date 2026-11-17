---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.archive-storage-planning
name: archive-storage-planning
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, storage-selection, archive-storage, glacier, archive-tier, retrieval-time, retention]
level: practitioner
status: docs-checked
description: "Plan archive storage and retrieval: archive class choice, minimum durations and early deletion fees, retrieval tiers and times, rehydration, object size effects and immutability."
sources: ["https://docs.aws.amazon.com/AmazonS3/latest/userguide/storage-class-intro.html", "https://learn.microsoft.com/azure/storage/blobs/access-tiers-overview", "https://cloud.google.com/storage/docs/storage-classes"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Archive storage and retrieval planning

## Steps
1. **Classify data**: retention period, how often and how fast it might be needed (legal
   discovery in days vs restore in hours), immutability requirement.
2. **Pick class by retrieval need**:
   - AWS S3: Glacier Instant Retrieval (millisecond access, 90-day minimum storage duration), Glacier Flexible
     Retrieval (minutes to hours, 90 days, objects must be restored first), Glacier Deep Archive (hours,
     180 days, objects must be restored first). Retrieval fees are per GB. Standard-IA and One Zone-IA have a
     30-day minimum.
   - Azure Blob: Cool (online, 30-day minimum), Cold (online, 90-day minimum) and Archive (offline,
     latency on the order of hours, 180-day minimum). Cool and Cold minimums apply to general-purpose v2
     accounts. Rehydration from Archive to an online tier can take up to 15 hours depending on the priority
     (standard or high) you choose; the blob cannot be read or modified while archived.
   - Google Cloud Storage: Nearline (30-day minimum), Coldline (90), Archive (365). Archive still gives
     millisecond access, but has higher data access and operation costs; retrieval fees apply to all three.
3. **Mind object size**: S3 Standard-IA, One Zone-IA and Glacier Instant Retrieval bill a minimum of 128 KB per
   object, and Glacier Flexible Retrieval and Deep Archive add 40 KB of metadata per archived object (32 KB at the
   archive rate, 8 KB at the S3 Standard rate). Many small objects therefore cost more; bundle (for example with
   tar) before archiving.
4. **Retrieval plan**: choose the restore priority per the vendor docs, budget the rehydration cost, and write a
   runbook for large restores. In Azure, Copy Blob is the recommended way to rehydrate and avoids the early
   deletion penalty, at the cost of capacity charges for two blobs; lifecycle policies cannot rehydrate.
5. **Lifecycle rules** to transition automatically by age. For unknown access patterns, S3 Intelligent-Tiering
   (objects under 128 KB are not auto-tiered; optional archive tiers need asynchronous access and a restore) or
   Cloud Storage Autoclass.
6. **Immutability**: check the vendor's object lock or immutable storage feature if retention must be enforced
   (not covered by the pages cited here).

## Gotchas
- Early deletion: AWS charges a pro-rated amount for the rest of the minimum duration if you delete, overwrite or
  transition early; Azure charges early deletion for the remaining days (for example 135 days if an archived
  blob is deleted after 45 of 180).
- Azure soft delete: a soft-deleted blob is not subject to the early deletion penalty until retention expires.
- Rehydration and retrieval are billed; estimate the cost before a bulk restore (see each vendor's pricing page).

## Verify
- [ ] Retrieval time objectives met by the chosen tier (test restore timed).
- [ ] Small objects bundled; lifecycle rules in place.

## Checked
2026-11-08. Confirmed against the S3 storage classes page (read in full: minimum durations, 128 KB, 40 KB metadata,
Glacier restore requirement, Intelligent-Tiering), the Azure access tiers overview (searched for tier minimums,
15-hour rehydration, early deletion example, Copy Blob, soft delete; not read end to end) and the Cloud Storage
storage classes page (searched for minimums, Archive millisecond access, Autoclass). Removed unsupported claims:
the 12-48 h Deep Archive figure, S3 Batch Operations restore, the Object Lock / immutable blob / bucket lock claim
(replaced by a pointer) and the unsourced "expedited costs more than years of storage" claim.
Method: documentation only; no commands were run.
