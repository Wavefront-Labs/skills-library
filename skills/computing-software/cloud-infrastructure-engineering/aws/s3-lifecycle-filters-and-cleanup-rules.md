---
id: computing-software.cloud-infrastructure-engineering.aws.s3-lifecycle-filters-and-cleanup-rules
name: s3-lifecycle-filters-and-cleanup-rules
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, s3, lifecycle-filters, abort-incomplete-multipart, noncurrent-version-expiration, expired-delete-markers, object-size-filter, cost-optimization]
level: practitioner
status: docs-checked
description: "S3 lifecycle rules that save money: prefix, tag and size filters, aborting incomplete multipart uploads, noncurrent version expiry and delete marker cleanup."
sources: ["https://docs.aws.amazon.com/AmazonS3/latest/userguide/intro-lifecycle-rules.html", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/lifecycle-transition-general-considerations.html", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/lifecycle-expire-general-considerations.html", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/how-to-set-lifecycle-configuration-intro.html", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/mpu-abort-incomplete-mpu-lifecycle-config.html", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/storage_lens_metrics_glossary.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# S3 lifecycle filters and cleanup rules

Hidden S3 cost usually sits in three places lifecycle can fix: **incomplete multipart
uploads**, **noncurrent versions**, and **small objects transitioned** to classes where per-object
overhead exceeds savings.

## 1. A baseline configuration
```json
{"Rules": [
 {"ID": "abort-mpu", "Status": "Enabled", "Filter": {},
  "AbortIncompleteMultipartUpload": {"DaysAfterInitiation": 7}},
 {"ID": "noncurrent", "Status": "Enabled", "Filter": {},
  "NoncurrentVersionTransitions": [{"NoncurrentDays": 30, "StorageClass": "GLACIER_IR"}],
  "NoncurrentVersionExpiration": {"NoncurrentDays": 90, "NewerNoncurrentVersions": 3}},
 {"ID": "delete-markers", "Status": "Enabled", "Filter": {},
  "Expiration": {"ExpiredObjectDeleteMarker": true}},
 {"ID": "logs-archive", "Status": "Enabled",
  "Filter": {"And": {"Prefix": "logs/", "ObjectSizeGreaterThan": 131072}},
  "Transitions": [{"Days": 30, "StorageClass": "STANDARD_IA"}, {"Days": 180, "StorageClass": "DEEP_ARCHIVE"}],
  "Expiration": {"Days": 730}},
 {"ID": "temp-by-tag", "Status": "Enabled", "Filter": {"Tag": {"Key": "temp", "Value": "true"}},
  "Expiration": {"Days": 7}}
]}
```
```bash
aws s3api put-bucket-lifecycle-configuration --bucket b --lifecycle-configuration file://lc.json
```
`put` **replaces** the whole configuration — fetch, edit, put.

## 2. Filters
- `Prefix`, `Tag`, `ObjectSizeGreaterThan`/`ObjectSizeLessThan` (bytes, exclusive bounds: an object exactly at the value is not matched), combined with `And`.
- `NewerNoncurrentVersions` (1 to 100) keeps the N newest noncurrent versions; it requires a `Filter` element (otherwise `InvalidRequest`).
- `ExpiredObjectDeleteMarker` removes delete markers that have no versions behind them.
- Can't combine `ExpiredObjectDeleteMarker` with `Days` expiration in the same rule.

## 3. Find what to clean
- Incomplete MPUs: Storage Lens free metric "Incomplete multipart upload bytes" (`IncompleteMultipartUploadStorageBytes`);
  `aws s3api list-multipart-uploads --bucket b`.
- Noncurrent bytes: Storage Lens "Noncurrent version bytes" (`NonCurrentVersionStorageBytes`) or an S3 Inventory report with all object versions.

## Gotchas
- Since September 2024 the default is that objects smaller than 128 KB are not transitioned to any storage class (configurations created earlier keep the old behaviour until edited); a size filter overrides this. Minimum storage durations (30 days for Standard-IA/One Zone-IA, 90 for Glacier Flexible Retrieval and Instant Retrieval, 180 for Deep Archive) bill early deletes.
- Each transitioned object is one transition request charge, so very many tiny objects can cost more to transition than they save.
- Lifecycle actions are queued asynchronously with no guaranteed completion time; billing changes when the rule is satisfied (transitions to Intelligent-Tiering bill after the transition completes).
- Lifecycle takes no action on noncurrent versions that have S3 Object Lock configured.

## Verify
- [ ] `get-bucket-lifecycle-configuration` shows all rules; Storage Lens incomplete-MPU bytes trend to ~0 after a week.
- [ ] Noncurrent version bytes stop growing.
- [ ] Cost Explorer: transition request costs reviewed against storage savings for the first month.

## Checked

2026-10-24 against the AWS documentation (docs.aws.amazon.com, current Amazon S3 User Guide) and the botocore API models. Confirmed: put replaces the whole configuration, `ExpiredObjectDeleteMarker` cannot be combined with `Days` (botocore model), `NewerNoncurrentVersions` range and Filter requirement, size-filter bounds, the September 2024 128 KB default, minimum storage durations, billing timing, Object Lock interaction, Storage Lens metric names. Removed unconfirmed LIST-slowdown and 30-days-in-Standard claims.

Method: documentation only; no commands were run.
