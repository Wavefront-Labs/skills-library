---
id: computing-software.cloud-infrastructure-engineering.aws.s3-replicating-kms-encrypted-objects
name: s3-replicating-kms-encrypted-objects
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, s3, replicate-kms-objects, replication-kms, sse-kms, multi-region-keys, cross-account-replication]
level: advanced
status: docs-checked
description: "Replicate SSE-KMS objects across regions or accounts: SourceSelectionCriteria, ReplicaKmsKeyID, role and key policies, bucket keys, multi-region keys and throttling."
sources: ["https://docs.aws.amazon.com/AmazonS3/latest/userguide/replication-config-for-kms-objects.html", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/replication-troubleshoot.html", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/replication-time-control.html", "https://docs.aws.amazon.com/kms/latest/developerguide/multi-region-keys-overview.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Replicating KMS-encrypted objects

By default replication **skips** SSE-KMS objects. You must opt in and give the replication
role access to both keys.

## 1. Replication rule
```json
{"Role": "arn:aws:iam::111122223333:role/s3-replication",
 "Rules": [{
   "ID": "to-dr", "Status": "Enabled", "Priority": 1, "Filter": {},
   "DeleteMarkerReplication": {"Status": "Enabled"},
   "SourceSelectionCriteria": {"SseKmsEncryptedObjects": {"Status": "Enabled"}},
   "Destination": {
     "Bucket": "arn:aws:s3:::data-dr-eu-central-1",
     "Account": "444455556666",
     "AccessControlTranslation": {"Owner": "Destination"},
     "EncryptionConfiguration": {"ReplicaKmsKeyID": "arn:aws:kms:eu-central-1:444455556666:key/abcd-..."}}}]}
```
```bash
aws s3api put-bucket-replication --bucket data --replication-configuration file://repl.json
```
`ReplicaKmsKeyID` takes a KMS key ARN or key alias ARN in the **same Region as the destination
bucket**; the key must be a symmetric customer managed key. `PutBucketReplication` does not validate
the key: an invalid key still returns `200 OK` and replication then fails. Unencrypted source objects
are encrypted with the destination bucket's default encryption; objects encrypted with SSE-S3,
SSE-KMS or DSSE-KMS keep the same encryption type as the source.

## 2. Replication role policy
```json
[{"Effect": "Allow", "Action": ["kms:Decrypt"],
  "Resource": "arn:aws:kms:eu-west-1:111122223333:key/src-key",
  "Condition": {"StringLike": {"kms:ViaService": "s3.eu-west-1.amazonaws.com",
                               "kms:EncryptionContext:aws:s3:arn": "arn:aws:s3:::data/*"}}},
 {"Effect": "Allow", "Action": ["kms:Encrypt", "kms:GenerateDataKey"],
  "Resource": "arn:aws:kms:eu-central-1:444455556666:key/abcd-...",
  "Condition": {"StringLike": {"kms:ViaService": "s3.eu-central-1.amazonaws.com",
                               "kms:EncryptionContext:aws:s3:arn": "arn:aws:s3:::data-dr-eu-central-1/*"}}}]
```
With **S3 Bucket Keys** enabled, the encryption context is the **bucket ARN**
(`arn:aws:s3:::data`), not the object ARN; adjust the condition or replication fails. The key policy
of the key protecting the replica must also allow `kms:Decrypt` to the calling principal for Bucket Key
replication. The role also needs `s3:GetObjectVersionForReplication` on source objects (not only
`s3:GetObjectVersion`, which does not cover KMS-encrypted objects).

## 3. Key policies
- Source key policy: allow the replication role `kms:Decrypt` (same account: IAM policy is
  enough if the key policy enables IAM).
- Destination key (other account): key policy must allow the source account's replication
  role `kms:Encrypt`/`kms:GenerateDataKey`. The destination bucket policy must also allow
  the role to `s3:ReplicateObject` etc., plus `s3:ObjectOwnerOverrideToBucketOwner` when
  using owner override.

## 4. Multi-Region keys
You can use multi-Region KMS keys with S3, but S3 currently treats them as single-Region keys and
does not use their multi-Region features: set `ReplicaKmsKeyID` to the key ARN in the destination
Region as for any other key.

## 5. Throughput and cost
Replication requests count toward your AWS KMS requests-per-second quotas; the S3 documentation's
example is that replicating 1,000 objects per second can use about 2,000 KMS requests per second of
your quota. A throttled request returns `ThrottlingException`. Monitor KMS request rates in
CloudWatch and request a quota increase through Service Quotas if needed.

## Gotchas
- DSSE-KMS objects need the same opt-in; SSE-C objects are replicated without extra permissions.
- KMS key policies that restrict access by CIDR range, VPC endpoint or S3 access point can make replication fail.
- AWS managed key `aws/s3` cannot be used cross-account at the destination.

## Verify
- [ ] Upload a test object with `--sse aws:kms --sse-kms-key-id <src-key>`; source shows `COMPLETED`, destination object shows `ServerSideEncryption: aws:kms` with the destination key.
- [ ] Destination account principals can read it with their key; source key not needed there.
- [ ] No `OperationsFailedReplication` with KMS reasons over a day of traffic.

## Checked

2026-10-24 against the AWS documentation (docs.aws.amazon.com, current Amazon S3 User Guide) and the botocore API models. Confirmed: SSE-KMS and DSSE-KMS opt-in via `SourceSelectionCriteria`, `ReplicaKmsKeyID` accepts key or alias ARN in the destination Region and is not validated on put, role permissions, `kms:ViaService` and Bucket Key encryption-context rules, multi-Region keys treated as single-Region, `aws/s3` unusable cross-account, KMS throttling guidance. Removed the unconfirmed Bucket Key percentage and the copy-in-place claim.

Method: documentation only; no commands were run.
