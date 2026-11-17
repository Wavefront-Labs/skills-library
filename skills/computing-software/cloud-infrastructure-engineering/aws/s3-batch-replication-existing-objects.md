---
id: computing-software.cloud-infrastructure-engineering.aws.s3-batch-replication-existing-objects
name: s3-batch-replication-existing-objects
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, s3, batch-replication, replicate-existing-objects, s3-batch-operations, s3-replication, backfill]
level: practitioner
status: docs-checked
description: "Replicate objects that live S3 replication skipped: Batch Replication jobs from generated or custom manifests, filters, IAM, completion reports and re-drives."
sources: ["https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-batch-replication-batch.html", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-batch-replication-policies.html", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/batch-ops-create-job.html", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/replication-what-is-isnot-replicated.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# S3 Batch Replication for existing objects

Live replication only handles objects written **after** the rule exists. Batch Replication
copies: existing objects, objects that previously `FAILED`, objects that are replicas
(for chained/new destinations), and objects already replicated (to a newly added destination).

## 1. Prerequisite
A replication configuration on the source bucket with the destination(s) — Batch Replication
uses those rules (filters, encryption, ownership settings).

## 2. Create a job with a generated manifest
```bash
aws s3control create-job --account-id <ACCOUNT_ID> --region us-east-1 \
  --operation '{"S3ReplicateObject":{}}' \
  --manifest-generator '{"S3JobManifestGenerator":{
      "SourceBucket":"arn:aws:s3:::orders-use1","EnableManifestOutput":true,
      "ManifestOutputLocation":{"Bucket":"arn:aws:s3:::batch-manifests","ManifestFormat":"S3InventoryReport_CSV_20211130"},
      "Filter":{"EligibleForReplication":true,"ObjectReplicationStatuses":["NONE","FAILED"]}}}' \
  --report '{"Bucket":"arn:aws:s3:::batch-reports","Prefix":"repl","Format":"Report_CSV_20180820","Enabled":true,"ReportScope":"AllTasks"}' \
  --priority 10 --role-arn arn:aws:iam::<ACCOUNT_ID>:role/s3-batch-replication --no-confirmation-required
```
- `ObjectReplicationStatuses`: `NONE` (never replicated), `FAILED`, `COMPLETED`, `REPLICA`.
- The generator filter also takes `CreatedAfter`/`CreatedBefore`, `KeyNameConstraint`, object size bounds and storage-class filters (S3 Control `JobManifestGeneratorFilter`). A generated manifest uses the prefix and tags of your replication rules and must be stored in the source bucket's Region.
- Custom manifests (CSV of bucket,key,versionId or an S3 Inventory report) work too.

## 3. IAM for the batch role
Trust `batchoperations.s3.amazonaws.com`. Permissions (generated-manifest policy):
`s3:InitiateReplication` on `<source-bucket>/*`; `s3:GetReplicationConfiguration` and
`s3:PutInventoryConfiguration` on the source bucket; `s3:GetObject` and `s3:GetObjectVersion`
on the manifest bucket; `s3:PutObject` on the completion-report bucket and the manifest bucket.
With a user-supplied manifest the policy drops the first two bucket-level actions. The
replication rule's role must also be allowed to copy on both source and destination (including
KMS rights for encrypted objects).

## 4. Track
```bash
aws s3control describe-job --account-id <ACCOUNT_ID> --job-id <JOB_ID> \
  --query 'Job.[Status,ProgressSummary]'
```
Completion report lists per-object results; failed tasks include reason codes.

## Gotchas
- Objects in S3 Glacier Flexible Retrieval or Deep Archive, and Intelligent-Tiering Archive Access tiers, are not supported: restore them first.
- Consider disabling lifecycle rules while the job runs so delete markers and versions stay in step.
- After changing the replication configuration, wait a few minutes before creating a job with a generated manifest. One job supports a manifest of up to 20 billion objects.
- Objects deleted from the destination by version ID are not re-replicated (error `DstObjectHardDeleted`); copy them in place with a Batch Copy job instead.
- SSE-C objects are replicated like others; no extra SSE-C permissions are needed.

## Verify
- [ ] Job `Complete` with `NumberOfTasksFailed` = 0 (or failures explained).
- [ ] Inventory on the source shows no `NONE`/`FAILED` replication status for in-scope objects.
- [ ] Spot check object counts/bytes in source vs destination (Storage Lens or inventory).

## Checked

2026-10-24 against the AWS documentation (docs.aws.amazon.com, current Amazon S3 User Guide) and the botocore API models. Confirmed: eligible object types, `ObjectReplicationStatuses` values, manifest and filter fields (botocore s3control model), Batch Replication IAM policies and trust principal, Glacier limitation, 20-billion-object manifest limit, SSE-C support. Removed unconfirmed pricing and throttling statements.

Method: documentation only; no commands were run.
