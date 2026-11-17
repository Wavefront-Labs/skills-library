---
id: computing-software.cloud-infrastructure-engineering.aws.s3-inventory-reports
name: s3-inventory-reports
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, s3, s3-inventory, inventory-report, athena, batch-operations, encryption-audit, storage-analysis]
level: practitioner
status: docs-checked
description: "Configure S3 Inventory reports (fields, Parquet, daily/weekly, destination policy) and query them with Athena to audit encryption, storage classes, replication status and sizes."
sources: ["https://docs.aws.amazon.com/AmazonS3/latest/userguide/storage-inventory.html", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/configure-inventory.html", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/storage-inventory-location.html", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/storage-inventory-athena-query.html", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/batch-ops-create-job.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# S3 Inventory reports

**Why:** `ListObjectsV2` over a billion-object bucket is slow and costly. Inventory gives a
daily/weekly flat file of every object with metadata — the input for audits, Athena and
Batch Operations manifests.

## 1. Configure
Destination bucket policy (allow S3 to write):
```json
{"Effect": "Allow", "Principal": {"Service": "s3.amazonaws.com"}, "Action": "s3:PutObject",
 "Resource": "arn:aws:s3:::inventory-dest/*",
 "Condition": {"StringEquals": {"aws:SourceAccount": "<ACCOUNT_ID>", "s3:x-amz-acl": "bucket-owner-full-control"},
               "ArnLike": {"aws:SourceArn": "arn:aws:s3:::datalake"}}}
```
```bash
aws s3api put-bucket-inventory-configuration --bucket datalake --id daily-full --inventory-configuration '{
 "Id":"daily-full","IsEnabled":true,"IncludedObjectVersions":"Current",
 "Schedule":{"Frequency":"Daily"},
 "Destination":{"S3BucketDestination":{"Bucket":"arn:aws:s3:::inventory-dest","Prefix":"datalake","Format":"Parquet",
    "Encryption":{"SSES3":{}}}},
 "OptionalFields":["Size","LastModifiedDate","StorageClass","ETag","IsMultipartUploaded","ReplicationStatus",
   "EncryptionStatus","BucketKeyStatus","ObjectLockMode","ObjectLockRetainUntilDate","IntelligentTieringAccessTier","ChecksumAlgorithm","ObjectOwner"]}}'
```
The first report can take up to 48 hours; after that it follows the configured Daily or Weekly schedule. The destination bucket must be in the same Region as the source bucket. Each delivery has a `manifest.json` (file
list + checksums) and Hive-style `hive/dt=YYYY-MM-DD-HH-MM/symlink.txt` for Athena.

## 2. Athena
Create a table over the Parquet data with `dt` partition (DDL in the docs), `MSCK REPAIR TABLE`
or partition projection, then:
```sql
-- unencrypted or SSE-S3 objects that policy says must be SSE-KMS
SELECT key, encryption_status FROM datalake_inventory
WHERE dt = '2026-10-16-01-00' AND encryption_status <> 'SSE-KMS' LIMIT 100;
-- storage by class
SELECT storage_class, count(*) objects, sum(size)/power(1024,4) tib
FROM datalake_inventory WHERE dt = '2026-10-16-01-00' GROUP BY 1 ORDER BY tib DESC;
-- replication failures
SELECT key FROM datalake_inventory WHERE dt = '2026-10-16-01-00' AND replication_status = 'FAILED';
```

## 3. Feed Batch Operations
Batch Operations accepts an inventory report only if it is CSV-formatted (you give it the report's
`manifest.json`); for a Parquet inventory, filter in Athena and write a CSV manifest instead. Jobs can
copy, update encryption, tag, restore, invoke Lambda or replicate the selected objects.

## Gotchas
- Inventory is eventually consistent: very recent writes/deletes may be missing.
- Include `AllVersions` when auditing versioned buckets (noncurrent versions are where the storage hides).
- Cost: Inventory is billed per the S3 pricing page; compare it with the LIST request cost for your bucket size.

## Verify
- [ ] `manifest.json` appears daily under the destination prefix.
- [ ] Athena query returns object counts matching CloudWatch `NumberOfObjects` (± recent churn).
- [ ] Encryption audit query result is empty or has a remediation Batch job.

## Checked

Checked 2026-10-27 against the S3 User Guide pages Cataloging and analyzing your data with S3 Inventory, Configuring Inventory, Inventory manifest, Querying with Athena and Batch Operations, plus the botocore s3 model.
Confirmed: PutBucketInventoryConfiguration shape (IncludedObjectVersions All or Current, Schedule Frequency Daily or Weekly, OptionalFields including ObjectLockMode, ObjectOwner, BucketKeyStatus, ChecksumAlgorithm, IntelligentTieringAccessTier); CSV, ORC and Parquet output; first report up to 48 hours; destination must be in the same Region; destination policy conditions (aws:SourceAccount, s3:x-amz-acl bucket-owner-full-control); manifest.json and hive symlink layout with Athena partition projection on dt; encryption status values include SSE-S3, SSE-KMS, DSSE-KMS, SSE-C and NOT-SSE; inventory lists are eventually consistent; Batch Operations needs a CSV inventory report. Replaced the claim that any inventory manifest can drive Batch Operations.

Method: documentation only; no commands were run.
