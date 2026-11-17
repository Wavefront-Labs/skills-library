---
id: computing-software.cloud-infrastructure-engineering.aws.s3-glacier-storage-class-selection
name: s3-glacier-storage-class-selection
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, s3, glacier-instant-retrieval, glacier-flexible-retrieval, deep-archive, archive-strategy, retrieval-cost]
level: practitioner
status: docs-checked
description: "Choose between S3 Glacier Instant Retrieval, Flexible Retrieval and Deep Archive by access pattern, retrieval latency, minimum duration, per-object overhead and retrieval cost."
sources: ["https://docs.aws.amazon.com/AmazonS3/latest/userguide/glacier-storage-classes.html", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/storage-class-intro.html", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/restoring-objects-retrieval-options.html", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/lifecycle-transition-general-considerations.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Choosing a Glacier storage class

## 1. The three classes
| | Glacier Instant Retrieval | Glacier Flexible Retrieval | Glacier Deep Archive |
|---|---|---|---|
| Access | milliseconds, normal GET | restore first: expedited 1-5 min (typical, objects under 250 MB), standard 3-5 h, bulk 5-12 h | restore first: standard within 12 h, bulk within 48 h |
| Minimum storage duration | 90 days | 90 days | 180 days |
| Minimum billable object size | 128 KB | none, but 40 KB metadata added per object | none, but 40 KB metadata added per object |
| Retrieval cost | per-GB retrieval fee | per-GB retrieval fee by tier; Bulk retrievals are free | per-GB retrieval fee by tier |
| Typical use | rarely read but must be instant: medical images, old user uploads, compliance reads | backups, media archives with hours tolerance | regulatory retention 7-10 years, tape replacement |
Each archived object in Flexible/Deep Archive adds 32 KB of index data billed at
the archive class rate plus 8 KB billed at S3 Standard rates. Aggregate small files (tar/zip) before archiving.

## 2. Decision rules
- Accessed about once a quarter, needs instant access: **Glacier IR**.
- Accessed a few times a year or never, hours are fine: **Flexible**.
- Kept for compliance, almost never read, 12-48 h is fine: **Deep Archive**.
- Unknown pattern: **Intelligent-Tiering** (with optional archive tiers) instead of
  guessing; it charges a monthly monitoring and automation fee per object (objects under 128 KB are not monitored).
- Objects under 128 KB: keep in Standard or Standard-IA (IR and IA bill a 128 KB minimum).

## 3. Moving data
- Lifecycle transitions (see lifecycle skills) are the usual path:
  Standard to Glacier IR at 90 days, to Deep Archive at 365 days. Each transitioned object is one
  transition request charge; filter out small objects with a size filter (objects under 128 KB are not transitioned by default).
- Direct upload: `aws s3 cp file s3://b/k --storage-class DEEP_ARCHIVE` (or `GLACIER_IR`,
  `GLACIER`).
- Restore from Flexible/Deep Archive:
  `aws s3api restore-object --bucket b --key k --restore-request '{"Days":7,"GlacierJobParameters":{"Tier":"Bulk"}}'`;
  the restored copy is temporary (billed as Standard for those days). For many objects use
  S3 Batch Operations restore jobs.

## 4. Cost check before committing
Estimate with: objects count x per-object overhead, transition requests, storage per GB
by class, expected retrievals per year x retrieval price, early deletion fees if data is
deleted before the minimum duration (charged as if stored the full minimum). S3 Storage
Lens and storage class analysis show actual access patterns per prefix to base the
decision on data rather than guesses.

## Gotchas
- Deleting or overwriting an object in Glacier IR at day 30 incurs a pro-rated charge for the remaining 60 days of the 90-day minimum.
- Expedited retrievals might not be accepted during periods of high demand unless you buy provisioned capacity (Flexible Retrieval only).
- Restores of Deep Archive data do not support expedited.

## Verify
- [ ] Class chosen per dataset with access frequency, latency need and object size recorded.
- [ ] Average object size in archived prefixes well above 128 KB (or files aggregated).
- [ ] A test restore meets the documented RTO for that dataset.

## Checked

2026-10-24 against the AWS documentation (docs.aws.amazon.com, current Amazon S3 User Guide) and the botocore API models. Confirmed: class codes, minimum storage durations (90/90/180 days), 128 KB minimum billable size for Glacier Instant Retrieval, 40 KB archive metadata split (32 KB + 8 KB), restore tiers and times, Bulk free for Flexible Retrieval, provisioned capacity behaviour, early-deletion pro-rating, the 128 KB default transition behaviour. Removed unconfirmed storage-price ratio and relative retrieval-price claims.

Method: documentation only; no commands were run.
