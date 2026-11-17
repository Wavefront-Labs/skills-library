---
id: computing-software.cloud-infrastructure-engineering.aws.s3-cross-account-access-and-vpce-conditions
name: s3-cross-account-access-and-vpce-conditions
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, s3, cross-account-s3, s3-vpce-condition, aws-sourcevpce, bucket-policy, kms, iam-role]
level: practitioner
status: docs-checked
description: "Grant S3 access across accounts: bucket policy plus IAM on both sides, SSE-KMS key policy, direct vs assumed-role access, and aws:SourceVpce restrictions."
sources: ["https://docs.aws.amazon.com/AmazonS3/latest/userguide/troubleshoot-403-errors.html", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/example-bucket-policies-vpc-endpoint.html", "https://docs.aws.amazon.com/vpc/latest/privatelink/vpc-endpoints-s3.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cross-account S3 access and VPC endpoint conditions

## 1. Two patterns
- **Direct**: account B's role calls S3 on account A's bucket. Needs **both** A's bucket
  policy allowing B's principal **and** B's IAM policy allowing the action on A's ARNs.
- **Assume role**: B assumes a role in A that has bucket access. Only A's IAM matters for S3;
  simpler auditing, works with services that can't use resource policies.

## 2. Direct access, done fully
Bucket policy in A:
```json
{"Sid": "BReadWrite", "Effect": "Allow",
 "Principal": {"AWS": "arn:aws:iam::<ACCOUNT_B>:role/ingest"},
 "Action": ["s3:GetObject", "s3:PutObject"], "Resource": "arn:aws:s3:::shared-data/inbox/*"},
{"Sid": "BList", "Effect": "Allow",
 "Principal": {"AWS": "arn:aws:iam::<ACCOUNT_B>:role/ingest"},
 "Action": "s3:ListBucket", "Resource": "arn:aws:s3:::shared-data",
 "Condition": {"StringLike": {"s3:prefix": ["inbox/*"]}}}
```
Role policy in B: allow the same actions on `arn:aws:s3:::shared-data` / `.../inbox/*`.
If the bucket uses **SSE-KMS with a customer managed key**: A's key policy must allow B's role
`kms:Decrypt` (reads) and `kms:GenerateDataKey` (writes), and B's IAM must allow them on the
key ARN. Objects encrypted with the AWS-managed `aws/s3` key **cannot** be read cross-account.
Ensure Object Ownership is BucketOwnerEnforced so A owns B's uploads.

## 3. Restrict to VPC endpoints
```json
{"Sid": "OnlyViaOurEndpoints", "Effect": "Deny", "Principal": "*", "Action": "s3:*",
 "Resource": ["arn:aws:s3:::shared-data", "arn:aws:s3:::shared-data/*"],
 "Condition": {"StringNotEquals": {"aws:SourceVpce": ["vpce-0a1", "vpce-0b2"]},
               "ArnNotLike": {"aws:PrincipalArn": ["arn:aws:iam::<ACCOUNT_A>:role/admin"]}}}
```
`aws:SourceVpce` works only for requests through an S3 VPC endpoint (gateway or interface);
`aws:SourceVpc` matches the VPC ID; `aws:SourceIp` cannot be used for requests that traverse a VPC
endpoint (use `aws:VpcSourceIp`). A policy that allows only your endpoints can lock out your own
administrators, hence the exempted admin role above.

## 4. Debugging AccessDenied
Check in order: bucket policy (explicit denies, conditions), B's IAM policy, SCPs/RCPs on
both accounts, KMS key policy, Block Public Access (not relevant for named principals),
object ownership (objects owned by a third account), the endpoint policy in B's VPC. The
error message in CloudTrail often states which policy type denied (`explicit deny in a
resource-based policy`, `... service control policy`).

## Verify
- [ ] From B: `aws s3 cp s3://shared-data/inbox/x .` works; `aws s3 ls s3://shared-data/other/` denied.
- [ ] KMS-encrypted object written by B is readable by A and by B.
- [ ] Same request from outside the listed endpoints is denied.

## Checked

Checked 2026-10-27 against the S3 User Guide pages Troubleshoot access denied (403 Forbidden) errors and Controlling access from VPC endpoints with bucket policies, and the Amazon VPC gateway endpoints for S3 page.
Confirmed: SSE-KMS with a customer managed key needs kms:Decrypt (reads) and kms:GenerateDataKey (writes) on the key policy, while objects under the AWS managed aws/s3 key are readable only by the key-owning account; aws:SourceVpce takes the endpoint ID (not an ARN) and aws:SourceVpc takes the VPC ID; the VPC endpoint bucket policy warning about locking yourself out; aws:SourceIp cannot be used for traffic through a VPC endpoint; denied messages in CloudTrail name the policy type for same-account or same-organization requests.

Method: documentation only; no commands were run.
