---
id: computing-software.cloud-infrastructure-engineering.aws.s3-intelligent-tiering-archive-configuration
name: s3-intelligent-tiering-archive-configuration
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, s3, intelligent-tiering, intelligent-tiering-config, archive-access-tier, deep-archive-access, storage-classes, cost-optimization]
level: practitioner
status: docs-checked
description: "Use S3 Intelligent-Tiering well: automatic tiers, opting into Archive Access and Deep Archive Access with filters, the 128 KB and monitoring-fee math, and restore behaviour."
sources: ["https://docs.aws.amazon.com/AmazonS3/latest/userguide/intelligent-tiering-overview.html", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/restoring-objects.html", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/storage-class-intro.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# S3 Intelligent-Tiering and its archive tiers

## 1. Tiers
Automatic (no retrieval fees, ms access):
- Frequent Access → **Infrequent Access** after 30 days without access → **Archive Instant
  Access** after 90 days. Any access moves the object back to Frequent.
Optional (must be configured; need restore before access):
- **Archive Access**: after 90–730 days without access (you choose).
- **Deep Archive Access**: after 180–730 days. Activate Archive Access at 90 days only if you want to bypass Archive Instant Access.

## 2. Getting objects into Intelligent-Tiering
- Upload with `--storage-class INTELLIGENT_TIERING`, or
- Lifecycle transition (e.g. day 0) from Standard:
```json
{"Rules":[{"ID":"to-it","Status":"Enabled","Filter":{"Prefix":""},
  "Transitions":[{"Days":0,"StorageClass":"INTELLIGENT_TIERING"}]}]}
```

## 3. Enable archive tiers (opt-in, filterable)
```bash
aws s3api put-bucket-intelligent-tiering-configuration --bucket logs-archive --id archive-old \
  --intelligent-tiering-configuration '{"Id":"archive-old","Status":"Enabled",
   "Filter":{"Prefix":"raw/"},
   "Tierings":[{"Days":180,"AccessTier":"ARCHIVE_ACCESS"},{"Days":365,"AccessTier":"DEEP_ARCHIVE_ACCESS"}]}'
aws s3api list-bucket-intelligent-tiering-configurations --bucket logs-archive
```
Only enable for data whose readers can tolerate hours-long restores (`restore-object` without
`Days`; Standard retrieval typically 3–5 h for Archive Access and within 12 h for Deep Archive Access). `head-object` shows
`ArchiveStatus` (`ARCHIVE_ACCESS` or `DEEP_ARCHIVE_ACCESS`).

## 4. When it pays
- A monthly object monitoring and automation charge applies; **objects < 128 KB are not monitored or tiered**
  (they stay in the Frequent Access tier).
- No minimum storage duration for Intelligent-Tiering; no retrieval fees for the automatic tiers.
- Best for unknown/changing access patterns on objects ≥ 128 KB. For known patterns (logs
  never read after 30 days) explicit lifecycle to Glacier classes is cheaper.

## Gotchas
- Applications that suddenly get `InvalidObjectState` after enabling archive tiers — archive
  tiers are opt-in for a reason; scope them by prefix/tag.
- GET, PUT, copy and restore requests count as access and move IA/Archive Instant Access objects back to Frequent Access; HEAD, tagging and LIST calls do not. `SelectObjectContent` does not tier objects up but does reset the archive-tier timer.
  A job that GETs every object regularly keeps everything in Frequent Access.
- The S3 Inventory `IntelligentTieringAccessTier` optional field shows the tier distribution.

## Verify
- [ ] Inventory shows objects distributed across FA/IA/AIA after 90 days, as expected.
- [ ] Archive configuration filter covers only the intended prefix.
- [ ] Monthly cost (storage + monitoring) lower than the previous storage class, per Cost Explorer usage type.

## Checked

2026-10-24 against the AWS documentation (docs.aws.amazon.com, current Amazon S3 User Guide) and the botocore API models. Confirmed: automatic tiers and 30/90-day thresholds, optional archive tiers and the 90-730 / 180-730 day ranges (botocore `Tiering`), 128 KB rule, no retrieval fees for automatic tiers, what counts as access, restore request form for archive tiers, `ArchiveStatus` values, `put-bucket-intelligent-tiering-configuration` shape. Removed unconfirmed minimum-duration and per-1,000-object monitoring-fee statements.

Method: documentation only; no commands were run.
