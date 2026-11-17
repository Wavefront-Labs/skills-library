---
id: computing-software.cloud-infrastructure-engineering.aws.auto-remediating-public-s3-buckets
name: auto-remediating-public-s3-buckets
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, s3, public-bucket-remediation, block-public-access, aws-config, auto-remediation, ssm-automation]
level: practitioner
status: docs-checked
description: "Prevent and fix public S3 buckets: account-level Block Public Access, Config rules with SSM Automation remediation runbooks, Access Analyzer for S3, and safe exceptions."
sources:
  - https://docs.aws.amazon.com/AmazonS3/latest/userguide/access-control-block-public-access.html
  - https://docs.aws.amazon.com/config/latest/developerguide/s3-bucket-public-read-prohibited.html
  - https://docs.aws.amazon.com/config/latest/developerguide/s3-account-level-public-access-blocks-periodic.html
  - https://docs.aws.amazon.com/systems-manager-automation-runbooks/latest/userguide/automation-aws-block-public-s3-bucket.html
  - https://docs.aws.amazon.com/systems-manager-automation-runbooks/latest/userguide/automation-aws-disables3bucketpublicreadwrite.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Auto-remediating public S3 buckets

## Prevent first
```bash
aws s3control put-public-access-block --account-id <ACCOUNT_ID> --public-access-block-configuration \
  BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true
```
- Block Public Access (BPA) settings exist for access points, buckets, accounts and AWS Organizations. New buckets, access points and objects do not allow public access by default.
- To stop anyone turning the account setting off, deny `s3:PutAccountPublicAccessBlock` in an SCP, excluding a security-admin role:
```json
{"Effect":"Deny","Action":["s3:PutAccountPublicAccessBlock"],"Resource":"*",
 "Condition":{"ArnNotLike":{"aws:PrincipalArn":"arn:aws:iam::*:role/SecurityAdmin"}}}
```

## Detect
- Config rules: `s3-account-level-public-access-blocks-periodic` (compliance against the BPA settings you require), `s3-bucket-public-read-prohibited`, `s3-bucket-public-write-prohibited`.
- IAM Access Analyzer for S3 reviews buckets with public access.

## Remediate automatically
Attach an SSM Automation runbook as a remediation action on the Config rule (`aws configservice put-remediation-configurations`, or the console):
- `AWSConfigRemediation-ConfigureS3BucketPublicAccessBlock` (bucket level).
- `AWSConfigRemediation-ConfigureS3PublicAccessBlock` (account level).
- `AWS-DisableS3BucketPublicReadWrite`.
Read each runbook page for its input parameters and required permissions (the bucket-level runbook needs `s3:PutBucketPublicAccessBlock`; the account-level one `s3:PutAccountPublicAccessBlock`). Use a dedicated Automation assume role.

## Exceptions
- Legitimate public buckets are rare: tag them with an approval marker and scope the Config rule or remediation to skip them; review exceptions regularly.

## Verify
- [ ] A test bucket made public in a sandbox is blocked and the Config rule returns to compliant.
- [ ] Remediation execution status shows success.

## Checked
2026-10-28. Confirmed on the S3 "Blocking public access" page (settings scope, new-bucket default, `s3:PutAccountPublicAccessBlock`, `s3:PutBucketPublicAccessBlock`, Access Analyzer for S3), the Config rule pages and the runbook pages: rule names, runbook names and the permissions above; `check_commands.py` accepted the CLI commands.
Removed as unconfirmed: the ACLs-disabled default, CloudFront/OAC advice, `s3-bucket-level-public-access-prohibited`, Security Hub control IDs, `RemovePrincipalStarFromS3BucketPolicy`, the remediation JSON parameter names, `ssm.amazonaws.com` trust note and the EventBridge fast path.
Method: documentation only; no commands were run.
