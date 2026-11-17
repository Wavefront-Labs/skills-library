---
id: computing-software.cloud-infrastructure-engineering.aws.s3-replication-failure-troubleshooting
name: s3-replication-failure-troubleshooting
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, s3, replication-status, replication-failure, s3-replication, operationfailedreplication, batch-replication]
level: advanced
status: docs-checked
description: "Diagnose S3 replication that is FAILED or silently skipping objects: replication status per object, failure event reasons, IAM/KMS/ownership/Object Lock causes, and re-driving."
sources: ["https://docs.aws.amazon.com/AmazonS3/latest/userguide/replication-troubleshoot.html", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/replication-metrics-events.html", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/replication-what-is-isnot-replicated.html", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/repl-metrics.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# S3 replication failure troubleshooting

## 1. Per-object status
```bash
aws s3api head-object --bucket src --key path/obj --query ReplicationStatus
```
- Source object: `PENDING`, `COMPLETED` or `FAILED` (returned in the `x-amz-replication-status` header).
- Destination object: `REPLICA`.
For bulk status add the optional `ReplicationStatus` field to an S3 Inventory report and query it with Athena.

## 2. Get the failure reason
Enable S3 Replication metrics on the rule (RTC is not required), then add an S3 Event Notification
for `s3:Replication:OperationFailedReplication` on the **source** bucket (SQS, SNS or Lambda). The event carries a `failureReason`:
| failureReason | Fix |
|---|---|
| `AssumeRoleNotPermitted` | Replication role trust must allow `s3.amazonaws.com` (`batchoperations.s3.amazonaws.com` for the Batch Operations job role) |
| `DstBucketNotFound`, `DstBucketUnversioned` | Destination missing or versioning not enabled |
| `DstPutObjectNotPermitted` | Destination bucket policy lacks `s3:ReplicateObject` or `s3:ObjectOwnerOverrideToBucketOwner`, or the destination KMS key policy does not let the role use the key (`kms:Decrypt`, `kms:GenerateDataKey*`) |
| `DstPutAclNotPermitted`, `DstPutTaggingNotPermitted`, `DstMultipartInitNotPermitted`, `DstMultipartUploadNotPermitted`, `DstMultipartCompleteNotPermitted` | `s3:ReplicateObject` may be missing on the destination |
| `DstDelObjNotPermitted` | `s3:ReplicateDelete` may be missing on the destination |
| `SrcGetObjectNotPermitted`, `SrcHeadObjectNotPermitted` | Role lacks `s3:GetObjectVersionForReplication` on the source |
| `SrcGetAclNotPermitted`, `SrcGetTaggingNotPermitted` | Role lacks `s3:GetObjectVersionAcl` / `s3:GetObjectVersionTagging`; objects must be owned by the source bucket owner |
| `DstKmsKeyNotFound`, `DstKmsKeyInvalidState`, `SrcKmsKeyInvalidState` | KMS key missing, disabled or pending deletion |
| `DstBucketObjectLockConfigMissing`, `DstPutRetentionNotPermitted`, `DstPutLegalHoldNotPermitted`, `SrcGetRetentionNotPermitted`, `SrcGetLegalHoldNotPermitted` | Object Lock: the destination needs Object Lock enabled; the role needs `s3:PutObjectRetention` / `s3:PutObjectLegalHold` on the destination and `s3:GetObjectRetention` / `s3:GetObjectLegalHold` on the source |
| `DstObjectHardDeleted` | Batch Replication only: the version was deleted from the destination by version ID and cannot be re-replicated; copy the source object in place (Batch Copy) |
| `SrcObjectNotEligible` | Storage class or tags do not match the rule |
| `InitiateReplicationNotPermitted` | Batch Replication only: `s3:InitiateReplication` missing on the job role |
Also check CloudTrail in the destination account for `PutObject` denials by the role.

## 3. Objects that never replicate (no FAILED status)
- Objects that existed **before** the rule: use **S3 Batch Replication**
  (`aws s3control create-job` with operation `S3ReplicateObject` and a manifest generated
  from the replication configuration).
- Objects that are themselves replicas made by another replication rule (A to B to C does not
  chain); Batch Replication can replicate them.
- SSE-KMS or DSSE-KMS objects when the rule lacks
  `SourceSelectionCriteria.SseKmsEncryptedObjects: Enabled`.
- Objects in Glacier Flexible Retrieval, Glacier Deep Archive or the Intelligent-Tiering archive
  tiers (restore and copy first).
- Actions performed by lifecycle configuration, and (for rules with a `Filter`) delete markers
  unless delete marker replication is enabled; delete markers are not replicated cross-account by default.
- Tag-filtered rules: the tag must be set in the `PutObject` request; tagging afterwards does not replicate
  the object (use Batch Replication).
- Objects the bucket owner lacks permission to read (ACL-era cross-account uploads).
- Cross-account destinations configured as Requester Pays buckets.

## 4. Re-drive failed objects
Fix the cause, then run Batch Replication with `ObjectReplicationStatuses: ["FAILED"]`, or re-upload
the failed objects to the source bucket, which starts replication for the new objects. If the rule uses
the change-ownership-to-destination option and the object already exists in the destination but shows
`FAILED`, Batch Replication might not resolve it; the documentation says to contact AWS Support.

## 5. Monitoring
Replication metrics (enabled per rule, or automatically with RTC): `ReplicationLatency`,
`BytesPendingReplication`, `OperationsPendingReplication`, `OperationsFailedReplication`. Set
alarm missing-data treatment to ignore. Alarm on failed operations > 0 and on pending bytes growing.

## Verify
- [ ] Test object reaches `COMPLETED` on source and `REPLICA` on destination.
- [ ] `OperationsFailedReplication` alarm exists and is at zero.
- [ ] Inventory query shows no FAILED objects after the re-drive job.

## Checked

2026-10-24 against the AWS documentation (docs.aws.amazon.com, current Amazon S3 User Guide) and the botocore API models. Confirmed: head-object status values, failure-reason table (rewritten from the S3 replication failure reasons table), metrics prerequisite for failure events, what is not replicated (replicas, Glacier tiers, lifecycle actions, tag-after-put, delete markers), Batch Replication re-drive and caveats, Inventory `ReplicationStatus` field (botocore). Removed the SSE-C exclusion (SSE-C is replicated), an unconfirmed console option and the copy-over-itself trick.

Method: documentation only; no commands were run.
