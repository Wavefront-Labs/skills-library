---
id: computing-software.cloud-infrastructure-engineering.aws.s3-lifecycle-management
name: s3-lifecycle-management
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, s3, s3-lifecycle, lifecycle-rules, storage-classes, s3-standard-ia, s3-one-zone-ia, s3-intelligent-tiering, s3-glacier-instant-retrieval, glacier-flexible-retrieval, glacier-deep-archive, versioning, noncurrent-versions, delete-markers, incomplete-multipart-upload, object-lock, retention, storage-lens, storage-class-analysis, minimum-storage-duration, transition-cost, data-retention, archival]
level: practitioner
status: docs-checked
description: "Design S3 lifecycle rules: pick storage classes by access pattern, expire noncurrent versions and multipart debris, and avoid the minimum-duration and per-object transition traps."
sources: ["https://docs.aws.amazon.com/AmazonS3/latest/userguide/intro-lifecycle-rules.html", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/lifecycle-transition-general-considerations.html", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/lifecycle-expire-general-considerations.html", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/how-to-set-lifecycle-configuration-intro.html", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/storage-class-intro.html", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/intelligent-tiering-overview.html", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/storage_lens_metrics_glossary.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# S3 lifecycle management — tier, expire and clean up on purpose

**Goal:** every bucket has rules that move data to the cheapest class its access
pattern allows, delete what retention policy says to delete, and clear the invisible
debris (old versions, delete markers, abandoned multipart parts) that quietly
dominates many S3 bills.

## 1. Measure the access pattern first
- **Storage Lens** shows storage bytes, noncurrent-version bytes and incomplete-MPU bytes
  (free metrics; advanced metrics are a paid tier) — start here.
- **Storage class analysis** on a prefix or tag observes access patterns and helps
  choose when to move objects from Standard to Standard-IA.
- Rule of thumb: if you can't predict access, use **Intelligent-Tiering** and stop;
  if you can, use explicit transitions.

## 2. Storage classes and their traps
| Class | Min. duration | Min. billable size | Retrieval |
|---|---|---|---|
| Standard | — | — | ms |
| Intelligent-Tiering | none | none, but objects < 128 KB are not monitored or tiered | ms (optional archive tiers: minutes to hours) |
| Standard-IA / One Zone-IA | 30 days | 128 KB | ms, per-GB retrieval fee |
| Glacier Instant Retrieval | 90 days | 128 KB | ms, per-GB retrieval fee |
| Glacier Flexible Retrieval | 90 days | 40 KB metadata per object (32 KB Glacier rate + 8 KB Standard rate) | minutes to hours (restore first) |
| Glacier Deep Archive | 180 days | 40 KB metadata per object | within 12 h (standard) or 48 h (bulk), restore first |
Deleting or transitioning before the minimum duration bills the remainder anyway.
One Zone-IA loses data if the AZ is lost — only for reproducible data.

## 3. Write the rules
```json
{"Rules": [
 {"ID": "logs-tiering", "Status": "Enabled",
  "Filter": {"And": {"Prefix": "logs/", "ObjectSizeGreaterThan": 131072}},
  "Transitions": [{"Days": 30, "StorageClass": "STANDARD_IA"},
                  {"Days": 90, "StorageClass": "GLACIER_IR"},
                  {"Days": 365, "StorageClass": "DEEP_ARCHIVE"}],
  "Expiration": {"Days": 2555}},
 {"ID": "versions-and-debris", "Status": "Enabled", "Filter": {},
  "NoncurrentVersionTransitions": [{"NoncurrentDays": 30, "StorageClass": "GLACIER_IR"}],
  "NoncurrentVersionExpiration": {"NoncurrentDays": 90, "NewerNoncurrentVersions": 3},
  "AbortIncompleteMultipartUpload": {"DaysAfterInitiation": 7}},
 {"ID": "orphan-markers", "Status": "Enabled", "Filter": {},
  "Expiration": {"ExpiredObjectDeleteMarker": true}}
]}
```
Apply: `aws s3api put-bucket-lifecycle-configuration --bucket <BUCKET> --lifecycle-configuration file://lc.json`.
- **`put` replaces the whole configuration.** Always `get`, merge, `put`; IaC should own
  the entire config per bucket.
- Use `ObjectSizeGreaterThan` (bytes) to keep small objects out of IA/Glacier, where
  minimum size and per-object request charges exceed the saving.
- `ExpiredObjectDeleteMarker` cannot sit in the same rule as `Expiration.Days`; keep it separate.
- Tag filters let one bucket hold different retention classes (`retention=7y`).

## 4. Versioned buckets
With versioning on, `Expiration` only adds a delete marker; the bytes stay as a
noncurrent version until `NoncurrentVersionExpiration` removes them. A versioned bucket
with no noncurrent rule grows forever — the commonest lifecycle mistake.

## 5. Retention that must hold
- Legal or regulatory retention: use **Object Lock** plus lifecycle for what happens after.
  Lifecycle takes no action on noncurrent versions that have Object Lock configured.
- Replication (CRR/SRR) does not replicate lifecycle actions; configure rules on both buckets.

## Gotchas
- Each transitioned object is charged a transition request; for many small objects the cost can
  outweigh the saving, so aggregate small files first or filter them out with a size filter.
- Lifecycle queues actions asynchronously and does not guarantee a completion time (days or even weeks
  of lag is possible). Billing changes when the rule is satisfied, not when the action completes
  (transitions to Intelligent-Tiering bill after the transition completes).
- Days count from object creation (or from becoming noncurrent).
- Glacier Flexible/Deep Archive objects must be restored before read; a GET fails with `InvalidObjectState`.
- When rules overlap, permanent deletion beats transition, transition beats delete-marker creation, and
  Glacier Flexible Retrieval beats Standard-IA/One Zone-IA.
- Not all lifecycle waterfall moves are allowed (for example Glacier Flexible to Deep Archive only);
  check the supported-transitions list.

## Verify
- [ ] Storage Lens shows incomplete-MPU bytes near zero and noncurrent bytes bounded.
- [ ] Every versioned bucket has a `NoncurrentVersionExpiration` rule.
- [ ] No transition rule applies to objects < 128 KB (size filter or measured otherwise).
- [ ] Modelled transition request cost < 12 months of storage saving for the affected objects.
- [ ] `get-bucket-lifecycle-configuration` matches IaC exactly (no manual drift).

## Checked

2026-10-24 against the AWS documentation (docs.aws.amazon.com, current Amazon S3 User Guide) and the botocore API models. Confirmed: storage-class minimum durations, minimum billable sizes, 40 KB archive metadata split, availability of One Zone-IA, `put` replaces the configuration, versioned-bucket expiration behaviour, delete-marker rule restriction, overlapping-rule precedence, asynchronous action and billing timing, Storage Lens free metrics. Removed unconfirmed claims (Object Lock compliance wording, daily run, midnight rounding, ~30 day class-analysis window, paid-metric detail beyond the tier split).

Method: documentation only; no commands were run.
