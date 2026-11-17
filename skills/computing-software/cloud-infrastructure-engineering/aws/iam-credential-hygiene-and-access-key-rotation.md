---
id: computing-software.cloud-infrastructure-engineering.aws.iam-credential-hygiene-and-access-key-rotation
name: iam-credential-hygiene-and-access-key-rotation
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, iam, access-key-rotation, credential-report, last-accessed, unused-access, mfa, least-privilege]
level: practitioner
status: docs-checked
description: "Audit and clean IAM credentials: credential reports, rotating access keys with zero downtime, last-accessed data to trim permissions, and finding unused users, keys and roles."
sources: ["https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_getting-report.html", "https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_last-accessed.html", "https://docs.aws.amazon.com/general/latest/gr/iam-service.html", "https://github.com/boto/botocore/blob/develop/botocore/data/iam/2010-05-08/service-2.json"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# IAM credential hygiene and access key rotation

## 1. Credential report
```bash
aws iam generate-credential-report
aws iam get-credential-report
```
`get-credential-report` returns the last generated report (a CSV); the console offers the same download.
A report can be generated as often as once every four hours (a newer request inside that window returns the
existing report), and only one report is stored. It covers passwords, the first two access keys per user, MFA
devices and signing certificates; use `ListAccessKeys` for users with more.
Columns to act on: `password_enabled`, `password_last_used`, `mfa_active`, `access_key_1_active`,
`access_key_1_last_rotated`, `access_key_1_last_used_date` (and the `access_key_2_*` equivalents), plus the
account's root row (it should have MFA and **no** active access keys).
Flags to raise: console users without MFA; keys older than your rotation limit; keys never used or unused
beyond your limit. Last-used values are recorded at most once per 15 minutes for keys and once per 5 minutes
for passwords.

## 2. Zero-downtime key rotation
A user can have at most 2 access keys, which is what makes rotation possible.
```bash
aws iam create-access-key --user-name svc-legacy           # 2nd key (max 2 per user)
# deploy new key to the consumer (Secrets Manager), confirm it is in use:
aws iam get-access-key-last-used --access-key-id AKIA_NEW
aws iam update-access-key --user-name svc-legacy --access-key-id AKIA_OLD --status Inactive
# wait a few days, watch for errors, then
aws iam delete-access-key --user-name svc-legacy --access-key-id AKIA_OLD
```
Better: eliminate the key: IAM roles for workloads, Identity Center for humans, OIDC for CI,
IAM Roles Anywhere for on-prem servers.

## 3. Last-accessed data to trim permissions
```bash
JOB=$(aws iam generate-service-last-accessed-details --arn arn:aws:iam::<ACCOUNT_ID>:role/app --granularity ACTION_LEVEL --query JobId --output text)
aws iam get-service-last-accessed-details --job-id $JOB
```
`--granularity` is `SERVICE_LEVEL` or `ACTION_LEVEL`; each `ServicesLastAccessed` entry has `ServiceNamespace`,
`LastAuthenticated` and `TotalAuthenticatedEntities` (and `TrackedActionsLastAccessed` at action level).
Service information is tracked for at least 400 days; action-level data covers management actions only, for the
supported services, and not data events. Recent activity can take up to four hours to appear, attempts that
were denied are included, and the report excludes access allowed only by resource policies, SCPs, boundaries or
session policies. The same principal must generate and read the report. For
AWS Organizations, management-account reports show services allowed by SCPs for an OU or account.
IAM Access Analyzer **unused access** analyzers monitor continuously for unused roles, access keys, passwords
and permissions.

## 4. Enforcement
- An SCP denying `iam:CreateAccessKey` except for a break-glass role suits accounts that should not have IAM users.

## Gotchas
- Deactivating a key used by an unknown system: search CloudTrail for the key ID first.
- Last-used information is not a substitute for CloudTrail, which is the authoritative record of API calls.

## Verify
- [ ] Credential report: zero console users without MFA, zero active keys older than your limit, root has no keys.
- [ ] Access Analyzer unused-access findings reviewed and resolved/archived with reasons.
- [ ] Rotated key's old ID shows no new `LastUsedDate` after deactivation.

## Checked
Checked 2026-10-24 against the IAM User Guide pages "Generate credential reports" and "Refine permissions using
last accessed information", the IAM General Reference quotas and the botocore IAM model. Confirmed: report
commands and 4-hour regeneration window, single stored report, column names, the 5-minute and 15-minute
last-used recording rules, 2 access keys per user, 400-day service tracking, the 4-hour display delay, the
`SERVICE_LEVEL`/`ACTION_LEVEL` granularity values and `ServicesLastAccessed` fields, and the report-owner rule.
Removed unchecked material: the base64/`sleep` pipeline and CSV file name, the JMESPath `--query` filter on
last-accessed fields, the `<root_account>` literal, the AWS Config managed-rule names, parameters and the 90-day thresholds, and the
statement about Organizations last-accessed data feeding SCP design.
Method: documentation only; no commands were run.
