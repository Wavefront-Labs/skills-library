---
id: computing-software.cybersecurity-defensive.cloud-security.s3-block-public-access
name: s3-block-public-access
category: computing-software
field: cybersecurity-defensive
product: cloud-security
tags: [cloud-data-protection, s3-block-public-access, s3-bucket-policy, object-ownership, acls-disabled, public-exposure, aws-organizations-policy, data-exposure]
level: practitioner
status: docs-checked
description: "Prevent public S3 exposure: Block Public Access at org, account, bucket and access point level, ACLs disabled via Object Ownership, and Access Analyzer for S3 review."
sources: ["https://docs.aws.amazon.com/AmazonS3/latest/userguide/access-control-block-public-access.html", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/about-object-ownership.html", "https://docs.aws.amazon.com/securityhub/latest/userguide/s3-controls.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# S3 Block Public Access

**Goal:** no bucket or object becomes public by mistake, while intentionally public content is
served through a deliberate, recorded exception.

## Layers
1. **Block Public Access (BPA)** can be set at organization level (an AWS Organizations S3 policy
   that overrides account-level settings), account level, bucket level and access point level.
   There is no per-object setting. Turn on all four settings (BlockPublicAcls, IgnorePublicAcls,
   BlockPublicPolicy, RestrictPublicBuckets) in every account:
```
aws s3control put-public-access-block --account-id <ACCOUNT_ID> --public-access-block-configuration \
  BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true
```
2. **Object Ownership = Bucket owner enforced**: ACLs are disabled and access is governed by
   policies; it is the default for newly created buckets.
3. **IAM Access Analyzer for S3** reviews buckets whose ACLs, bucket policies or access point
   policies grant public access, including to other AWS accounts outside your organization.
   Intentional exceptions can be recorded by archiving the finding.

## Detection
- Security Hub control S3.8 (general purpose buckets should block public access) and S3.19 (access
  points should have block public access settings enabled).

## Gotchas
- Access points have their own BPA settings; they are all enabled by default at creation and
  cannot be changed afterwards.
- BPA settings override bucket policies and object permissions that would otherwise allow public access.

## Verify
- [ ] Every account reports all four BPA settings true.
- [ ] Access Analyzer shows no unintended public or external buckets.

## Checked
2026-11-01. Confirmed against the S3 User Guide pages on Block Public Access and Object Ownership and the
Security Hub S3 controls page: BPA levels, the four setting names, organization-level policy, Bucket owner
enforced as default, Access Analyzer for S3, S3.8, S3.19 and access point BPA behaviour. The `aws s3control`
command passes the CLI model check. Removed (not stated on those pages): the SCP on
`s3:PutAccountPublicAccessBlock`, the April 2023 date, S3.1/S3.2/S3.3, Macie, the AWS Config rule names, CloudTrail
event list, CloudFront OAC detail and the presigned URL note.
Method: documentation only; no commands were run.
