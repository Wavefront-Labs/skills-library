---
id: computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.storage-lifecycle-policies
name: storage-lifecycle-policies
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-cost-optimisation
tags: [cloud-cost-optimisation, finops, workload-optimisation, storage-lifecycle-policies, s3-lifecycle, intelligent-tiering, blob-lifecycle-management, gcs-autoclass, glacier, archive-tier, minimum-storage-duration]
level: practitioner
status: docs-checked
description: "Write object storage lifecycle policies that save money: tiering by age/access, minimum-duration and retrieval charges, small objects, auto-tiering, expiry."
sources: ["https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lifecycle-mgmt.html", "https://learn.microsoft.com/azure/storage/blobs/lifecycle-management-overview", "https://cloud.google.com/storage/docs/autoclass", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/storage-class-intro.html", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/lifecycle-transition-general-considerations.html", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/intelligent-tiering-overview.html", "https://learn.microsoft.com/en-us/azure/storage/blobs/access-tiers-overview", "https://docs.cloud.google.com/storage/docs/storage-classes"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Storage lifecycle policies

## Steps
1. **Know the access pattern**: S3 Storage Class Analysis, Azure last access time tracking, or
   each cloud's own access metrics. Data read rarely after 30-90 days is the target.
2. **Unknown or changing patterns** → automatic tiering: S3 Intelligent-Tiering (per-object
   monitoring and automation charge; objects < 128 KB aren't tiered), GCS **Autoclass**, Azure
   lifecycle rules on last access time with access tracking enabled.
3. **Known patterns** → explicit rules, e.g. S3:
```json
{"Rules":[{"ID":"logs","Filter":{"Prefix":"logs/"},"Status":"Enabled",
  "Transitions":[{"Days":30,"StorageClass":"STANDARD_IA"},{"Days":90,"StorageClass":"GLACIER_IR"},{"Days":365,"StorageClass":"DEEP_ARCHIVE"}],
  "Expiration":{"Days":2555},
  "NoncurrentVersionExpiration":{"NoncurrentDays":30},
  "AbortIncompleteMultipartUpload":{"DaysAfterInitiation":7}}]}
```
4. **Expire** data you don't need — the cheapest tier is deletion. Align with retention policy.

## Cost traps
- **Minimum storage duration** charges: S3 Standard-IA/One Zone-IA 30 days, Glacier IR/Flexible
  90 days, Deep Archive 180 days; Azure Cool 30, Cold 90, Archive 180 days; GCS Nearline 30,
  Coldline 90, Archive 365 days. Deleting early still bills the minimum.
- **Small objects**: IA classes bill a minimum object size (128 KB on S3 IA); transition requests
  cost per object — millions of tiny objects can cost more to transition than they save.
- **Retrieval** fees and latency for archive tiers (hours for Deep Archive/Archive rehydration).

## Verify
- [ ] Each large bucket has a lifecycle rule or an explicit reason not to.
- [ ] Modelled savings net of transition and retrieval costs.

## Checked
2026-11-01. Confirmed in the S3 storage class comparison table (minimum durations 30/90/180 days, 128 KB minimum size,
retrieval fees), the S3 lifecycle considerations page (early-transition charge, objects under 128 KB not transitioned by
default), Intelligent-Tiering overview (monitoring and automation charge, 128 KB), Azure access tiers (30/90/180 days,
general-purpose v2) and Cloud Storage classes (30/90/365 days, Autoclass). Removed: Storage Lens, blob inventory, Storage
Insights and the Azure last-access rule property name (not in the pages read). Lifecycle JSON field names match the S3
examples page.
Method: documentation only; no commands were run.
