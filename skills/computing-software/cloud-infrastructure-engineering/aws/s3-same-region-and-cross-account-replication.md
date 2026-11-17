---
id: computing-software.cloud-infrastructure-engineering.aws.s3-same-region-and-cross-account-replication
name: s3-same-region-and-cross-account-replication
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, s3, s3-replication, same-region-replication, owner-override, replica-ownership, cross-account, log-aggregation]
level: practitioner
status: docs-checked
description: "Set up S3 same-region and cross-account replication: destination bucket policy, owner override, KMS keys, two-way replica modification sync, and when SRR beats CRR."
sources: ["https://docs.aws.amazon.com/AmazonS3/latest/userguide/replication.html", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/replication-change-owner.html", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/replication-walkthrough-2.html", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/replication-what-is-isnot-replicated.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# S3 same-region and cross-account replication

## 1. When SRR
- Aggregate logs from many buckets into one analytics/security bucket in the same region.
- Keep a **separate-account** copy for ransomware/insider protection (backup account).
- Live replica between prod and test accounts for data that must stay in-region.

## 2. Cross-account rule with owner override
Source rule (in account A):
```json
{"ID": "to-backup-acct", "Status": "Enabled", "Priority": 1, "Filter": {"Prefix": ""},
 "DeleteMarkerReplication": {"Status": "Disabled"},
 "Destination": {"Bucket": "arn:aws:s3:::orders-vault", "Account": "<ACCOUNT_B>",
   "AccessControlTranslation": {"Owner": "Destination"},
   "EncryptionConfiguration": {"ReplicaKmsKeyID": "arn:aws:kms:<REGION>:<ACCOUNT_B>:key/..."}},
 "SourceSelectionCriteria": {"SseKmsEncryptedObjects": {"Status": "Enabled"}}}
```
Destination bucket policy (account B):
```json
{"Effect": "Allow", "Principal": {"AWS": "arn:aws:iam::<ACCOUNT_A>:role/s3-replication"},
 "Action": ["s3:ReplicateObject", "s3:ReplicateDelete", "s3:ReplicateTags", "s3:ObjectOwnerOverrideToBucketOwner"],
 "Resource": "arn:aws:s3:::orders-vault/*"},
{"Effect": "Allow", "Principal": {"AWS": "arn:aws:iam::<ACCOUNT_A>:role/s3-replication"},
 "Action": ["s3:GetBucketVersioning", "s3:PutBucketVersioning"], "Resource": "arn:aws:s3:::orders-vault"}
```
- **Owner override** (`AccessControlTranslation`) makes account B own replicas. With
  BucketOwnerEnforced on the destination, B owns them anyway — keep both consistent.
- Account B's KMS key policy must allow A's replication role `kms:Encrypt`/`GenerateDataKey`.
- For a vault copy, **disable delete marker replication** so deletes in A don't hide data in B,
  and consider Object Lock on B.

## 3. Two-way replication
Rules on both buckets plus `ReplicaModifications: Enabled` in `SourceSelectionCriteria` to sync
metadata changes on replicas back (enable it on both rules). AWS recommends it for Multi-Region Access Point two-way replication.

## Gotchas
- Both buckets need versioning; destination can be in a different storage class (`StorageClass` in Destination).
- Replication doesn't replicate actions performed by lifecycle configuration or updates to bucket-level subresources (lifecycle, notification configuration); SSE-C objects are replicated.
- A cross-account destination cannot be a Requester Pays bucket.
- Chained replication (A → B → C) doesn't happen automatically; B's replicas aren't re-replicated.

## Verify
- [ ] Upload to A: object appears in B with owner = B and the B KMS key (`head-object --query SSEKMSKeyId`).
- [ ] Delete in A doesn't remove/hide the object in B (vault pattern).
- [ ] `aws s3api get-bucket-replication --bucket <source>` matches IaC.

## Checked

2026-10-24 against the AWS documentation (docs.aws.amazon.com, current Amazon S3 User Guide) and the botocore API models. Confirmed: cross-account destination bucket policy actions (including `s3:GetBucketVersioning` / `s3:PutBucketVersioning` on the bucket), owner override via `AccessControlTranslation` plus `Account`, Bucket owner enforced makes the override unnecessary, KMS key policy actions, delete markers not replicated cross-account by default, replicas not chained. Removed the SSE-C exclusion.

Method: documentation only; no commands were run.
