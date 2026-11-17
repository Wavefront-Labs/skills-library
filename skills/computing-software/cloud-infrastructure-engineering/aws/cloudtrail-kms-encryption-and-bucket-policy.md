---
id: computing-software.cloud-infrastructure-engineering.aws.cloudtrail-kms-encryption-and-bucket-policy
name: cloudtrail-kms-encryption-and-bucket-policy
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, cloudtrail, trail-kms-encryption, trail-bucket-policy, sse-kms, log-file-validation]
level: advanced
status: docs-checked
description: "Encrypt CloudTrail logs with a KMS key and write the key and bucket policies CloudTrail needs, using SourceArn conditions and log file validation."
sources: ["https://docs.aws.amazon.com/awscloudtrail/latest/userguide/encrypting-cloudtrail-log-files-with-aws-kms.html", "https://docs.aws.amazon.com/awscloudtrail/latest/userguide/create-s3-bucket-policy-for-cloudtrail.html", "https://docs.aws.amazon.com/awscloudtrail/latest/userguide/create-kms-key-policy-for-cloudtrail.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Trail encryption with KMS and trail bucket policies

## 1. Bucket policy
```json
{"Version":"2012-10-17","Statement":[
 {"Sid":"AclCheck","Effect":"Allow","Principal":{"Service":"cloudtrail.amazonaws.com"},
  "Action":"s3:GetBucketAcl","Resource":"arn:aws:s3:::<BUCKET>",
  "Condition":{"StringEquals":{"aws:SourceArn":"arn:aws:cloudtrail:<REGION>:<ACCOUNT_ID>:trail/main"}}},
 {"Sid":"Write","Effect":"Allow","Principal":{"Service":"cloudtrail.amazonaws.com"},
  "Action":"s3:PutObject","Resource":"arn:aws:s3:::<BUCKET>/AWSLogs/<ACCOUNT_ID>/*",
  "Condition":{"StringEquals":{"s3:x-amz-acl":"bucket-owner-full-control",
    "aws:SourceArn":"arn:aws:cloudtrail:<REGION>:<ACCOUNT_ID>:trail/main"}}}]}
```
Organization trail: change the bucket policy to also allow the organization's `AWSLogs/<ORG_ID>/*` path (see the "Creating a trail for an organization" page for the exact statements).

## 2. Key policy statements
```json
{"Sid":"CloudTrailEncrypt","Effect":"Allow","Principal":{"Service":"cloudtrail.amazonaws.com"},
 "Action":"kms:GenerateDataKey*","Resource":"*",
 "Condition":{"StringEquals":{"aws:SourceArn":"arn:aws:cloudtrail:<REGION>:<ACCOUNT_ID>:trail/main"},
   "StringLike":{"kms:EncryptionContext:aws:cloudtrail:arn":"arn:aws:cloudtrail:*:<ACCOUNT_ID>:trail/*"}}},
{"Sid":"CloudTrailDescribe","Effect":"Allow","Principal":{"Service":"cloudtrail.amazonaws.com"},
 "Action":"kms:DescribeKey","Resource":"*"},
{"Sid":"LogReaders","Effect":"Allow","Principal":{"AWS":"arn:aws:iam::<ACCOUNT_ID>:role/SecurityAnalyst"},
 "Action":"kms:Decrypt","Resource":"*",
 "Condition":{"StringLike":{"kms:EncryptionContext:aws:cloudtrail:arn":"arn:aws:cloudtrail:*:<ACCOUNT_ID>:trail/*"}}}
```

## 3. Apply
```bash
aws cloudtrail update-trail --name main --kms-key-id arn:aws:kms:<REGION>:<ACCOUNT_ID>:key/<KEY_ID> \
  --enable-log-file-validation
aws cloudtrail get-trail-status --name main --query '{err:LatestDeliveryError,last:LatestDeliveryTime}'
```
Errors at update time: `InsufficientEncryptionPolicyException` (key policy) or
`InsufficientS3BucketPolicyException` (bucket policy).

## Gotchas
- The key must be in the same Region as the bucket that receives log and digest files.
- If the KMS key is disabled, or its policy is not correctly configured for CloudTrail, CloudTrail cannot deliver logs; data encrypted with disabled or deleted keys is no longer accessible. Alarm on key disable/scheduled deletion and on `LatestDeliveryError`.
- An existing bucket using an S3 Bucket Key needs `kms:Decrypt` permission to create or update a trail with SSE-KMS.
- AWS recommends `aws:SourceArn` in the key policy; `aws:SourceAccount` is supported but not recommended.

## Verify
- [ ] `aws cloudtrail validate-logs --trail-arn <ARN> --start-time <ISO>` reports valid digests.

## Checked

2026-10-28. Confirmed against AWS documentation: bucket policy statements (GetBucketAcl, PutObject with bucket-owner-full-control), key policy actions and encryption-context condition, same-Region key rule, SourceArn recommendation, disabled-key delivery failure; exception names and LatestDeliveryError/Time via botocore cloudtrail model.
Removed: Athena/SIEM decrypt claim, silent-failure wording, head-object ServerSideEncryption check. The organization path `AWSLogs/o-<ORG_ID>/*` is confirmed.
Method: documentation only; no commands were run.
