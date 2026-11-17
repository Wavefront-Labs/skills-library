---
id: computing-software.cloud-infrastructure-engineering.aws.s3-object-ownership-and-disabling-acls
name: s3-object-ownership-and-disabling-acls
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, s3, object-ownership, bucket-owner-enforced, disable-acls, acl-migration, bucket-policy]
level: practitioner
status: docs-checked
description: "Move S3 buckets to Object Ownership BucketOwnerEnforced: find ACL dependencies, migrate grants to bucket policies, fix cross-account writers, and verify ACLs are off."
sources: ["https://docs.aws.amazon.com/AmazonS3/latest/userguide/about-object-ownership.html", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-ownership-migrating-acls-prerequisites.html", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/ensure-object-ownership.html", "https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/standard-logging-legacy-s3.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# S3 Object Ownership: disabling ACLs

New buckets default to **BucketOwnerEnforced** (ACLs disabled). Older buckets often still use
`ObjectWriter` — cross-account uploads then belong to the *uploader*, and the bucket owner
can't read them. Goal: one model (IAM + bucket policy), bucket owner owns everything.

## 1. Settings
| Setting | Owner of new objects | ACLs |
|---|---|---|
| `BucketOwnerEnforced` | bucket owner | disabled (only bucket-owner-full-control style ACLs accepted) |
| `BucketOwnerPreferred` | bucket owner if uploader sends `bucket-owner-full-control` | enabled |
| `ObjectWriter` | uploading account | enabled |

## 2. Before switching: find ACL use
- Server access logs / CloudTrail data events: requests with `aclRequired = Yes` field
  (S3 server access logs and CloudTrail include an `aclRequired` indicator).
- Bucket ACL grants beyond the owner: `aws s3api get-bucket-acl --bucket b`.
- Object ACLs granting other accounts: sample with `get-object-acl`, or S3 Inventory with
  `ObjectOwner`/ACL fields.
- Log-delivery: S3 server access logging to this bucket must use the bucket policy
  (`logging.s3.amazonaws.com` principal) rather than the log-delivery group ACL.

## 3. Migrate grants to the bucket policy
Example: partner account wrote objects with ACL `public-read` or `bucket-owner-read` →
replace with a policy statement granting `s3:GetObject` to the reader and `s3:PutObject` to the
writer.

## 4. Switch
```bash
aws s3api put-bucket-ownership-controls --bucket b \
  --ownership-controls 'Rules=[{ObjectOwnership=BucketOwnerEnforced}]'
```
Existing object and bucket ACLs stop being evaluated and the bucket owner owns every object. If a
bucket ACL grants access outside your account, migrate it to the bucket policy and reset the ACL to
private first, or the call fails with `InvalidBucketAclWithObjectOwnership`.
PUT requests that set an ACL other than bucket-owner-full-control fail with HTTP 400
`AccessControlListNotSupported` — find and fix those clients (common: old CLI scripts with
`--acl public-read`, CloudFront legacy log delivery).
Org guardrail for new buckets: an IAM policy or SCP denying `s3:CreateBucket` unless
`s3:x-amz-object-ownership` equals `BucketOwnerEnforced` (the pattern in the S3 documentation).

## Gotchas
- CloudFront standard logging (legacy) requires ACLs to be enabled on the log bucket; use standard logging (v2) to CloudWatch Logs, Firehose or S3, or keep that one bucket on `BucketOwnerPreferred`.
- Reverting is possible: you can re-enable ACLs and the preexisting bucket and object ACLs are restored.

## Verify
- [ ] `aws s3api get-bucket-ownership-controls --bucket b` shows `BucketOwnerEnforced`.
- [ ] A cross-account `PutObject` (with no ACL) succeeds and `head-object` from the owner works.
- [ ] No `AccessControlListNotSupported` errors in client logs a week after the switch.

## Checked

Checked 2026-10-27 against the S3 User Guide pages Controlling ownership of objects and disabling ACLs, Prerequisites for disabling ACLs, Ensuring object ownership, server access logging setup, and the CloudFront Developer Guide standard logging pages.
Confirmed: BucketOwnerEnforced is the default for new buckets; the three settings; PUTs with other ACLs return 400 AccessControlListNotSupported; bucket ACL grants outside the account must be migrated or PutBucketOwnershipControls fails with InvalidBucketAclWithObjectOwnership; ACLs are restored if re-enabled; aclRequired field in server access logs and CloudTrail; log delivery must use the logging.s3.amazonaws.com principal in a bucket policy; s3:x-amz-object-ownership condition documented on s3:CreateBucket; CloudFront legacy standard logging requires ACLs enabled on the bucket. Corrected the guardrail action.

Method: documentation only; no commands were run.
