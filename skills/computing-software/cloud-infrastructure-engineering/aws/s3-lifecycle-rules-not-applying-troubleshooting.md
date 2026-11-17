---
id: computing-software.cloud-infrastructure-engineering.aws.s3-lifecycle-rules-not-applying-troubleshooting
name: s3-lifecycle-rules-not-applying-troubleshooting
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, s3, lifecycle-troubleshooting, lifecycle-rule-conflicts, noncurrent-versions, delete-markers, s3-lifecycle]
level: practitioner
status: docs-checked
description: "Find out why an S3 lifecycle rule seems to do nothing: timing, filters, versioned buckets, small-object transition rules, conflicting rules, Object Lock and replication."
sources: ["https://docs.aws.amazon.com/AmazonS3/latest/userguide/intro-lifecycle-rules.html", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/lifecycle-transition-general-considerations.html", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/lifecycle-expire-general-considerations.html", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/how-to-set-lifecycle-configuration-intro.html", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/troubleshoot-lifecycle.html", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/lifecycle-configuration-examples.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# S3 lifecycle rules not applying

## 1. Timing expectations
- Lifecycle queues actions asynchronously with no guaranteed completion time; an action can run days or
  even weeks after the rule is satisfied. Billing changes when the rule is satisfied (expiration billing
  stops then), even if the object is still listed; transitions to Intelligent-Tiering are billed after they complete.
- A new or changed configuration takes a few minutes to propagate. Rules apply to existing objects too.

## 2. Check the rule matches
```bash
aws s3api get-bucket-lifecycle-configuration --bucket b
aws s3api head-object --bucket b --key logs/2026/01/x.gz \
  --query '{class:StorageClass,exp:Expiration,mod:LastModified}'
```
`Expiration` in head-object output shows which rule (`rule-id`) will expire the object and
when; if empty, no expiration rule matches. Common mismatches:
- **Prefix** typo or leading slash (`/logs/` never matches; keys do not start with `/`).
- **Tag filter** requires exact key and value; objects uploaded without the tag never match.
- **Object size filters** (`ObjectSizeGreaterThan`/`LessThan`) exclude objects.
- `Status: Disabled`.

## 3. Versioned buckets
- `Expiration` on current versions only adds a **delete marker**; the data remains as a
  noncurrent version and keeps costing money. Add `NoncurrentVersionExpiration` (with
  optional `NewerNoncurrentVersions` to keep N versions).
- Remove **expired object delete markers** (`ExpiredObjectDeleteMarker: true`) so lists
  stay clean.
- `AbortIncompleteMultipartUpload` (e.g. 7 days) cleans orphaned parts that are invisible
  to `ls` but billed.
```json
{"Rules": [{"ID": "logs", "Status": "Enabled", "Filter": {"Prefix": "logs/"},
  "Transitions": [{"Days": 30, "StorageClass": "STANDARD_IA"}, {"Days": 180, "StorageClass": "DEEP_ARCHIVE"}],
  "Expiration": {"Days": 2555},
  "NoncurrentVersionExpiration": {"NoncurrentDays": 30, "NewerNoncurrentVersions": 3},
  "AbortIncompleteMultipartUpload": {"DaysAfterInitiation": 7}},
 {"ID": "markers", "Status": "Enabled", "Filter": {},
  "Expiration": {"ExpiredObjectDeleteMarker": true}}]}
```

## 4. Transitions that do not happen
- Since September 2024, by default S3 does **not transition objects smaller than 128 KB** to any
  class (`TransitionDefaultMinimumObjectSize` is `all_storage_classes_128K`; configurations created
  earlier keep the old behaviour, small objects only to Glacier Flexible/Deep Archive, until you
  create, edit or delete a rule). Use `varies_by_storage_class` (the
  `x-amz-transition-default-minimum-object-size` header on `PutBucketLifecycleConfiguration`) or an
  `ObjectSizeGreaterThan`/`ObjectSizeLessThan` filter to allow small objects.
- A single rule cannot move an object onward before the previous class's minimum storage duration has
  passed (for example Glacier Instant Retrieval then Deep Archive needs at least 94 days if the first
  transition is at day 4).
- The waterfall only goes "down" (see the supported-transitions list); you cannot transition back up via
  lifecycle, and Glacier Flexible Retrieval can only move to Deep Archive.
- Objects with a `Pending` or `Failed` replication status are not transitioned or expired.

## 5. Conflicts and blockers
- Overlapping rules: an object gets at most one lifecycle action per day, the least costly one.
  Permanent deletion beats transition, transition beats delete-marker creation, and Glacier Flexible
  Retrieval beats Standard-IA/One Zone-IA. Two rules on the same prefix confuse people; consolidate.
- Tag filters are re-evaluated when the action runs: removing the tag before then cancels the action.
- **Object Lock**: lifecycle takes no action on noncurrent versions that have Object Lock configured.
- Replication: lifecycle actions on the source are not replicated; set rules on the
  destination too.
- Bucket policies cannot block lifecycle: even a policy that denies all actions for all principals does not stop it.

## Verify
- [ ] `head-object` on a sample key shows the expected `Expiration` rule id and date.
- [ ] Storage Lens or S3 metrics show bytes moving between classes over the following days.
- [ ] Noncurrent versions and incomplete multipart uploads trend to zero for the prefix.

## Checked

2026-10-24 against the AWS documentation (docs.aws.amazon.com, current Amazon S3 User Guide) and the botocore API models. Confirmed: asynchronous timing and billing at eligibility, configuration propagation, September 2024 128 KB default and the header name (botocore enum values `varies_by_storage_class`, `all_storage_classes_128K`), minimum-duration example, waterfall restrictions, conflict-resolution rules, bucket policy cannot block lifecycle, Object Lock behaviour, `Expiration` header on head-object. Removed unconfirmed once-a-day evaluation, 30-days-before-IA and MFA-delete claims.

Method: documentation only; no commands were run.
