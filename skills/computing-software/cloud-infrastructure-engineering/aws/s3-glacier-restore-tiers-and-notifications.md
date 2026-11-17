---
id: computing-software.cloud-infrastructure-engineering.aws.s3-glacier-restore-tiers-and-notifications
name: s3-glacier-restore-tiers-and-notifications
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, s3, glacier, glacier-restore, restore-object, restore-tiers, batch-operations, event-notifications]
level: practitioner
status: docs-checked
description: "Restore archived S3 objects: Glacier Flexible and Deep Archive tiers and timings, restore-object days, bulk restores with Batch Operations, completion events, costs."
sources: ["https://docs.aws.amazon.com/AmazonS3/latest/userguide/restoring-objects.html", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/restoring-objects-retrieval-options.html", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/batch-ops-initiate-restore-object.html", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/archival-storage.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Restoring from S3 Glacier storage classes

Glacier **Instant Retrieval** needs no restore (millisecond GETs, retrieval fee). This skill is
for **Glacier Flexible Retrieval** and **Glacier Deep Archive** (and Intelligent-Tiering archive tiers).

## 1. Tiers and times
| Tier | Flexible Retrieval | Deep Archive |
|---|---|---|
| Expedited | 1–5 min for objects under 250 MB (not available for Deep Archive; provisioned capacity optional, otherwise requests may be rejected in high demand) | — |
| Standard | 3–5 hours | within 12 hours |
| Bulk | 5–12 hours (free retrieval for Flexible) | within 48 hours |

## 2. Restore one object
```bash
aws s3api restore-object --bucket archive --key 2019/ledger.csv \
  --restore-request '{"Days":7,"GlacierJobParameters":{"Tier":"Standard"}}'
aws s3api head-object --bucket archive --key 2019/ledger.csv --query Restore
# "ongoing-request=\"true\""  ->  "ongoing-request=\"false\", expiry-date=\"...\""
```
- Creates a **temporary copy** (billed as Standard storage for `Days`) alongside the archived
  object; the object stays in its archive class. To move it permanently, `copy-object` onto
  itself with `--storage-class STANDARD` while restored.
- Intelligent-Tiering archive tiers: restore with `--restore-request '{}'` (no `Days`; the object moves back to Frequent Access and has no expiry).
- A restore can be upgraded to a faster tier while in progress (console: Upgrade retrieval tier). Subsequent restore requests on an already-restored object are billed as GET requests.

## 3. Bulk restores
S3 Batch Operations with a manifest (CSV or S3 Inventory report; `GlacierJobTier` is `BULK` or `STANDARD`). One job can restore either Glacier Flexible/Deep Archive objects or Intelligent-Tiering archive-tier objects, not both:
```bash
aws s3control create-job --account-id <ACCOUNT_ID> --operation '{"S3InitiateRestoreObject":{"ExpirationInDays":5,"GlacierJobTier":"BULK"}}' \
  --manifest '{"Spec":{"Format":"S3InventoryReport_CSV_20161130"},"Location":{"ObjectArn":"arn:aws:s3:::inv/archive/manifest.json","ETag":"..."}}' \
  --report '{"Bucket":"arn:aws:s3:::batch-reports","Format":"Report_CSV_20180820","Enabled":true,"ReportScope":"FailedTasksOnly"}' \
  --priority 10 --role-arn arn:aws:iam::<ACCOUNT_ID>:role/batch-restore --no-confirmation-required
```

## 4. Know when it's done
Event notifications `s3:ObjectRestore:Post` (initiated), `s3:ObjectRestore:Completed`,
`s3:ObjectRestore:Delete` (temp copy expired) — to SQS/Lambda/EventBridge to kick off the
processing that needed the data.

## Gotchas
- Cost: retrieval per GB plus per-request charges by tier; the S3 documentation advises aggregating many small objects into fewer large ones before archiving.
- Restore requests are limited to 1,000 transactions per second per account; use Batch Operations for large sets (a `ThrottlingException` means the rate was exceeded).
- Minimum storage durations: 90 days (Flexible), 180 days (Deep Archive) — early deletion is billed.
- Each archived object has 40 KB of metadata overhead billed (8 KB at S3 Standard rates + 32 KB at the archive class rate).
- `aws s3 cp` on an unrestored archived object fails with `InvalidObjectState`.

## Verify
- [ ] `head-object` shows `ongoing-request="false"` and an expiry date; `GetObject` succeeds.
- [ ] `ObjectRestore:Completed` event reaches the processing queue.
- [ ] Batch job completion report shows 0 failed tasks.

## Checked

2026-10-24 against the AWS documentation (docs.aws.amazon.com, current Amazon S3 User Guide) and the botocore API models. Confirmed: tier times for Flexible Retrieval and Deep Archive, Bulk free for Flexible Retrieval, Expedited limits and provisioned capacity, restore-object request shape and the Intelligent-Tiering empty request, head-object `Restore` values, `copy` to make a permanent copy, one Batch Operations job per archive type, event names (botocore `Event` enum: `s3:ObjectRestore:Post`, `Completed`, `Delete`), manifest format enum (S3 Control `JobManifestFormat`) and `GlacierJobTier` values, 1,000 restores/s limit. Removed the unconfirmed claim that re-issuing a restore extends its expiry and corrected the manifest format value.

Method: documentation only; no commands were run.
