---
id: computing-software.cloud-infrastructure-engineering.aws.s3-bucket-policy-lockout-recovery
name: s3-bucket-policy-lockout-recovery
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, s3, bucket-policy-lockout, root-user, centralized-root-access, access-denied]
level: advanced
status: docs-checked
description: "Recover from an S3 bucket policy that denies everyone, using the account root user or Organizations centralized root access, and prevent lockouts."
sources: ["https://docs.aws.amazon.com/AmazonS3/latest/userguide/troubleshoot-403-errors.html", "https://docs.aws.amazon.com/IAM/latest/UserGuide/id_root-user-privileged-task.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Recovering from a bucket policy lockout

## 1. Symptom
After `put-bucket-policy`, every principal (including admins) gets `AccessDenied` on the bucket, even
`GetBucketPolicy`. Typical cause: a `Deny` with `"Principal":"*"` and a condition nobody meets
(`aws:SourceVpce` for an endpoint admins do not use, `aws:SourceIp` typo, `NotPrincipal` mistakes).

## 2. Fix with the root user (standalone account)
The bucket owner account's **root user** can always delete the bucket policy:
1. Sign in as root (console) or use root credentials.
2. `aws s3api delete-bucket-policy --bucket <BUCKET>` (or S3 console, Permissions, Bucket policy, Delete).
3. Re-apply a corrected policy.

## 3. Fix with centralized root access (Organizations)
Member accounts without root credentials: from the management account or delegated admin for IAM:
```bash
aws sts assume-root --target-principal <MEMBER_ACCOUNT_ID> \
  --task-policy-arn arn=arn:aws:iam::aws:policy/root-task/S3UnlockBucketPolicy
# export the returned credentials, then:
aws s3api delete-bucket-policy --bucket <BUCKET>
```
Requires centralized root access enabled for the organization, an `sts:AssumeRoot` permission for the
caller (root user credentials cannot call it) and a Regional STS endpoint (the global endpoint is not
supported for AssumeRoot).

## 4. Prevent
- Exempt an admin/break-glass role in every Deny: `"ArnNotLike": {"aws:PrincipalArn": "arn:aws:iam::<ACCOUNT_ID>:role/BreakGlass"}`.
- Validate before applying: `aws accessanalyzer validate-policy --policy-type RESOURCE_POLICY --validate-policy-resource-type AWS::S3::Bucket --policy-document file://policy.json`.
- Apply through IaC with a reviewed diff, and test on a non-production bucket.

## Verify
- [ ] Admin role can `get-bucket-policy` after the fix; the corrected policy still blocks the intended traffic.

## Checked

Checked 2026-10-27 against the S3 User Guide page Troubleshoot access denied (403 Forbidden) errors, the IAM User Guide page on tasks that require root user credentials (centralized root access), and the botocore accessanalyzer model.
Confirmed: the account root user can delete an incorrect bucket policy to regain access; the management or delegated administrator account can run the privileged task Delete Amazon S3 bucket policy with aws sts assume-root and the policy arn:aws:iam::aws:policy/root-task/S3UnlockBucketPolicy; sts:AssumeRoot must be explicitly granted and goes to a Regional endpoint; validate-policy accepts policy type RESOURCE_POLICY and resource type AWS::S3::Bucket.

Method: documentation only; no commands were run.
