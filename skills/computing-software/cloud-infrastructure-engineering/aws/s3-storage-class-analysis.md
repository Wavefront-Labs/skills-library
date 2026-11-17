---
id: computing-software.cloud-infrastructure-engineering.aws.s3-storage-class-analysis
name: s3-storage-class-analysis
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, s3, storage-class-analysis-export, storage-class-analysis, s3-analytics, cost-optimization]
level: practitioner
status: docs-checked
description: "Configure S3 storage class analysis with daily CSV export to find when data becomes infrequently accessed, then turn the results into lifecycle transitions."
sources: ["https://docs.aws.amazon.com/AmazonS3/latest/userguide/analytics-storage-class.html", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/storage-class-intro.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# S3 storage class analysis

## 1. Configure with export
```bash
aws s3api put-bucket-analytics-configuration --bucket data-lake --id logs-prefix \
  --analytics-configuration '{"Id":"logs-prefix","Filter":{"Prefix":"logs/"},
   "StorageClassAnalysis":{"DataExport":{"OutputSchemaVersion":"V_1",
     "Destination":{"S3BucketDestination":{"Format":"CSV","Bucket":"arn:aws:s3:::analytics-exports","Prefix":"sca/data-lake/"}}}}}'
```
- Filter by prefix and/or tags; up to 1,000 configurations per bucket.
- The destination bucket needs a policy that lets S3 write the export (see the S3 docs example "Grant permissions for S3 Inventory and S3 analytics").

## 2. Reading results
- Data first appears in the console after 24 to 48 hours; it usually takes about 30 days (sometimes longer) of observation before a result.
- The export is a daily CSV with storage and retrieval by object age group (less than 15 days, 15-29, ... up to 730 days and older);
  the console shows "infrequently accessed" age.
- It only analyses Standard to Standard-IA transitions; it does not recommend Glacier tiers or One Zone-IA.

## 3. Act
If objects older than 45 days are rarely read:
```json
{"Rules":[{"ID":"logs-to-ia","Status":"Enabled","Filter":{"Prefix":"logs/"},
  "Transitions":[{"Days":45,"StorageClass":"STANDARD_IA"}]}]}
```
Account for Standard-IA's 30-day minimum storage duration, 128 KB minimum billable object size and
retrieval fees. Objects under 128 KB are not monitored by Intelligent-Tiering, so tiny-object buckets
need a separate look.

## 4. Alternatives
Unknown or changing patterns: S3 Intelligent-Tiering. Fleet-wide view: S3 Storage Lens.

## Verify
- [ ] Export files appear daily under the destination prefix.
- [ ] Lifecycle rule created from the observed age, with cost estimate recorded.

## Checked

Checked 2026-10-27 against the S3 User Guide pages Amazon S3 analytics - Storage Class Analysis and Understanding and managing Amazon S3 storage classes, and the botocore s3 model.
Confirmed: analysis only recommends STANDARD to STANDARD_IA transitions; filters by prefix or tags, up to 1,000 per bucket; daily CSV export; console data after 24 to 48 hours and about 30 days of observation; predefined object age groups (less than 15 days, 15-29 days, up to 730 days and older); Standard-IA 30-day minimum storage duration and 128 KB minimum billable size; Intelligent-Tiering does not monitor objects under 128 KB; PutBucketAnalyticsConfiguration filter and StorageClassAnalysis shape.

Method: documentation only; no commands were run.
