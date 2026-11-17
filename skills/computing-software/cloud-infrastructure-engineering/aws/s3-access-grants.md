---
id: computing-software.cloud-infrastructure-engineering.aws.s3-access-grants
name: s3-access-grants
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, s3, s3-access-grants, access-grants, identity-center, temporary-credentials, data-access]
level: practitioner
status: docs-checked
description: "Grant S3 prefix access to directory users and groups with S3 Access Grants: instances, locations, grants, Identity Center integration and vending temporary credentials to apps."
sources: ["https://docs.aws.amazon.com/AmazonS3/latest/userguide/access-grants.html", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/access-grants-limitations.html", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/access-grants-location-register.html", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/access-grants-integrations.html", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/access-grants-get-data.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# S3 Access Grants

**When:** thousands of prefix-level permissions for users/groups (often from your corporate
directory) — more than bucket policies or IAM policies can hold — e.g. per-team folders in a
data lake, per-user home prefixes.

## 1. Building blocks
- **Instance**: one per account per region; optionally linked to an **IAM Identity Center**
  instance so grants can target directory users/groups.
- **Location**: an S3 scope (`s3://`, a bucket, or a prefix) plus an IAM role that Access
  Grants assumes to vend credentials for it.
- **Grant**: grantee (IAM principal, or directory user/group) + permission (`READ`, `WRITE`,
  `READWRITE`) + sub-prefix of a location.

```bash
aws s3control create-access-grants-instance --account-id <ACCOUNT_ID> \
  --identity-center-arn arn:aws:sso:::instance/ssoins-123
aws s3control create-access-grants-location --account-id <ACCOUNT_ID> \
  --location-scope s3://datalake/ --iam-role-arn arn:aws:iam::<ACCOUNT_ID>:role/s3ag-location
aws s3control create-access-grant --account-id <ACCOUNT_ID> \
  --access-grants-location-id <LOCATION_ID> --access-grants-location-configuration S3SubPrefix='finance/*' \
  --grantee GranteeType=DIRECTORY_GROUP,GranteeIdentifier=<IDC_GROUP_ID> --permission READ
```
Location role trust policy: principal `access-grants.s3.amazonaws.com` with
`sts:AssumeRole` and `sts:SetSourceIdentity`, scoped with `aws:SourceAccount` and
`aws:SourceArn` conditions. The IAM Identity Center use case needs a second trust statement:
copy it from the "Register a location" page rather than from memory.

## 2. Getting data
The application (or user) asks for credentials scoped to the target:
```bash
aws s3control get-data-access --account-id <ACCOUNT_ID> --target 's3://datalake/finance/*' \
  --permission READ --duration-seconds 900
```
`DurationSeconds` accepts 900 to 43200 seconds.
Returns temporary credentials limited to that prefix. With Identity Center, the caller
presents an identity-enhanced session (trusted identity propagation) so the grant matches the
directory user. AWS SDK plugins (Java/Python S3 Access Grants plugin) do this transparently.
Documented integrations include Athena, EMR (also on EKS and Serverless), Redshift, Glue,
SageMaker Unified Studio and Transfer Family.

## 3. Auditing
With Identity Center trusted identity propagation, each CloudTrail data event for S3 carries a
direct reference to the end user, so per-user audit works without per-user IAM roles.

## Gotchas
- Limits: 1 instance per Region per account, 1,000 locations per instance, 100,000 grants per instance
  (S3 Access Grants limitations page; higher limits via AWS support).

## Verify
- [ ] A user in the finance group gets credentials for `finance/*` and reads objects; a request for `hr/*` is denied.
- [ ] CloudTrail data events show the directory user (Identity Center integration).
- [ ] `list-access-grants` matches the documented access model.

## Checked

Checked 2026-10-27 against the S3 User Guide pages S3 Access Grants, limitations, register a location, integrations, and the botocore s3control service model (2018-08-20).
Confirmed: s3control operation names and parameters used in the examples (grantee types DIRECTORY_USER, DIRECTORY_GROUP, IAM; permissions READ, WRITE, READWRITE; GetData DurationSeconds 900-43200); default location s3://; trust policy principal and the AssumeRole and SetSourceIdentity actions; limits of 1 instance per Region, 1,000 locations and 100,000 grants (page undated); integrations list. Removed the unconfirmed SetContext action, Storage Browser integration and most-specific-grant claims.

Method: documentation only; no commands were run.
