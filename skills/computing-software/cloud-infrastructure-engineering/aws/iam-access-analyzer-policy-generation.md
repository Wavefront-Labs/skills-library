---
id: computing-software.cloud-infrastructure-engineering.aws.iam-access-analyzer-policy-generation
name: iam-access-analyzer-policy-generation
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, iam, policy-generation, generate-policy-from-cloudtrail, access-analyzer, least-privilege]
level: advanced
status: docs-checked
description: "Generate a least-privilege IAM policy from a role's CloudTrail history with IAM Access Analyzer policy generation, then refine, validate and swap it in."
sources: ["https://docs.aws.amazon.com/IAM/latest/UserGuide/access-analyzer-policy-generation.html", "https://github.com/boto/botocore/blob/develop/botocore/data/accessanalyzer/2019-11-01/service-2.json"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Generating a policy from CloudTrail activity
**Goal:** replace a broad policy with one built from what the role actually called.

## 1. Prerequisites
- A CloudTrail trail that logs events for the account, covering the period; Access Analyzer reads its log files in
  S3. Policy generation does not identify action-level activity for **data events** (for example S3 data events)
  and does not track `iam:PassRole`, so add those by hand from code review.
- A service role Access Analyzer can assume (trust policy principal `access-analyzer.amazonaws.com`, action
  `sts:AssumeRole`). Its permissions policy needs `cloudtrail:GetTrail`, `iam:GenerateServiceLastAccessedDetails`
  and `iam:GetServiceLastAccessedDetails`, and `s3:GetObject` / `s3:ListBucket` on the trail bucket. The console
  can create the role for you (names beginning `AccessAnalyzerMonitorServiceRole`).
- The person starting a job also needs `iam:PassRole` (and `iam:GetRole`) on that service role plus the
  `access-analyzer:StartPolicyGeneration`, `GetGeneratedPolicy`, `ListPolicyGenerations` and
  `CancelPolicyGeneration` actions.
- Trail logs in another account (for example an organization trail): the role needs cross-account access to the
  bucket, the bucket must be owned by its bucket owner (object ownership "Bucket owner enforced" recommended), and
  a KMS key policy must allow `kms:Decrypt` if logs are encrypted. Trails created by AWS Control Tower are not
  supported.

## 2. Start a job (up to 90 days of activity)
```bash
aws accessanalyzer start-policy-generation \
  --policy-generation-details principalArn=arn:aws:iam::<ACCOUNT_ID>:role/app-role \
  --cloud-trail-details '{"trails":[{"cloudTrailArn":"arn:aws:cloudtrail:<REGION>:<ACCOUNT_ID>:trail/org","allRegions":true}],
     "accessRole":"arn:aws:iam::<ACCOUNT_ID>:role/service-role/AccessAnalyzerMonitorServiceRole",
     "startTime":"2026-07-20T00:00:00Z","endTime":"2026-10-18T00:00:00Z"}'
aws accessanalyzer get-generated-policy --job-id <JOB_ID> \
  --include-resource-placeholders --include-service-level-template
```
The job status moves from `IN_PROGRESS` to `SUCCEEDED` (or `FAILED` / `CANCELED`). A shorter date range
generates faster. In the console a generated policy can be reviewed for up to 7 days; if it exceeds the
6,144-character managed policy limit it is split into several policies.

## 3. Read the output critically
- Some services give action-level results; for others the result is service-level (from last accessed
  information) and you must choose the actions yourself.
- The template contains resource ARN placeholders for actions that support resource-level permissions; replace
  them with real ARNs, and use `*` only where the action does not support resource-level permissions.
- Denied actions in the logs are included (generation reviews all events), so inspect for requests that were
  never allowed.
- Rare paths (quarterly jobs, DR, failure handlers) are missing if they did not run in the window.
  Extend the window or add them from code review.
- Do not use policy generation for auditing; use CloudTrail.

## 4. Validate and roll out
```bash
aws accessanalyzer validate-policy --policy-type IDENTITY_POLICY --policy-document file://generated.json
aws accessanalyzer check-no-new-access --policy-type IDENTITY_POLICY \
  --existing-policy-document file://old.json --new-policy-document file://generated.json
```
`validate-policy` findings are of type `ERROR`, `SECURITY_WARNING`, `SUGGESTION` or `WARNING`.
Attach the generated policy alongside the old one, watch CloudTrail for `AccessDenied` from the role for a
release cycle, then detach the old policy.

## Verify
- [ ] Generated policy passes `validate-policy` with no ERROR/SECURITY_WARNING findings.
- [ ] No new `AccessDenied` events for the principal after the swap (CloudTrail Lake or Athena query on `errorCode`).

## Checked
Checked 2026-10-24 against the IAM User Guide page "IAM Access Analyzer policy generation" and the botocore
Access Analyzer model. Corrected: the old text said to add S3/Lambda data events for object-level actions; the
page says policy generation does not identify action-level activity for data events. Added the role permissions
the page lists (`iam:GenerateServiceLastAccessedDetails`, `iam:GetServiceLastAccessedDetails`), the
`iam:PassRole` non-tracking note, the 7-day console availability and the Control Tower limitation. Confirmed: up
to 90 days of events; trust principal; CLI parameter names (`principalArn`, `trails[].cloudTrailArn`,
`allRegions`, `accessRole`, `startTime`, `endTime`, `includeResourcePlaceholders`, `includeServiceLevelTemplate`);
job statuses; `validate-policy` and `check-no-new-access` operations and parameters; finding types.
Removed the unchecked claim that large trails take minutes and the claim about KMS role permissions on the role
itself (the page shows the key policy instead).
Method: documentation only; no commands were run.
