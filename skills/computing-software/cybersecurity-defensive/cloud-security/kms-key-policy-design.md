---
id: computing-software.cybersecurity-defensive.cloud-security.kms-key-policy-design
name: kms-key-policy-design
category: computing-software
field: cybersecurity-defensive
product: cloud-security
tags: [cloud-data-protection, kms-key-policy, aws-kms, key-policy, kms-grants, viaservice-condition, cross-account-keys, separation-of-duties]
level: advanced
status: docs-checked
description: "Write AWS KMS key policies that separate key admins from key users, scope use with service and encryption context conditions, and review grants and cross-account use."
sources: ["https://docs.aws.amazon.com/kms/latest/developerguide/key-policy-default.html", "https://docs.aws.amazon.com/kms/latest/developerguide/conditions-kms.html", "https://docs.aws.amazon.com/kms/latest/developerguide/key-policy-modifying-external-accounts.html", "https://docs.aws.amazon.com/kms/latest/developerguide/encrypt_context.html", "https://docs.aws.amazon.com/kms/latest/developerguide/grants.html", "https://docs.aws.amazon.com/kms/latest/developerguide/deleting-keys-scheduling-key-deletion.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# KMS key policy design

**Goal:** a customer-managed key whose policy alone tells you exactly who can manage it and who
can use it, for which service, so encryption actually restricts data access.

## Structure
```json
{
 "Version": "2012-10-17",
 "Statement": [
  {"Sid": "RootAccountForIAMDelegation", "Effect": "Allow",
   "Principal": {"AWS": "arn:aws:iam::111122223333:root"}, "Action": "kms:*", "Resource": "*"},
  {"Sid": "KeyAdmins", "Effect": "Allow",
   "Principal": {"AWS": "arn:aws:iam::111122223333:role/KeyAdmin"},
   "Action": ["kms:Create*","kms:Describe*","kms:Enable*","kms:List*","kms:Put*","kms:Update*",
              "kms:Revoke*","kms:Disable*","kms:Get*","kms:Delete*","kms:TagResource","kms:UntagResource",
              "kms:ScheduleKeyDeletion","kms:CancelKeyDeletion"],
   "Resource": "*"},
  {"Sid": "UseViaS3Only", "Effect": "Allow",
   "Principal": {"AWS": "arn:aws:iam::111122223333:role/app-role"},
   "Action": ["kms:Decrypt","kms:GenerateDataKey*"], "Resource": "*",
   "Condition": {"StringEquals": {"kms:ViaService": "s3.eu-west-1.amazonaws.com"}}}
 ]
}
```
- Unlike other AWS resource policies, a key policy gives no permission to the account unless a statement says so. The root-principal statement lets IAM policies in the account grant access. Without any statement for the account principal a key can become unmanageable (for example if the one named user is deleted) and you must contact AWS Support.
- In the default console policy, key administrators can manage the key but do not have permission to use it in cryptographic operations. Their permissions use wildcards (for example `kms:Create*`), so new API operations are allowed automatically unless you list a fixed set.
- `kms:ViaService` limits use of the key to requests made by the named AWS services (forward access sessions) and applies to KMS key resource operations. `kms:EncryptionContext:context-key` requires a particular encryption context for symmetric encryption keys, binding use to specific data.

## Cross-account
Cross-account use needs permission in the key policy of the key **and** an IAM policy in the external account; neither alone is sufficient. Only use operations on the key are effective across accounts (for example `kms:ScheduleKeyDeletion` granted to an external principal has no effect). Use `kms:CallerAccount` (single-valued) to constrain the calling account. Operations are logged in CloudTrail in both accounts.

## Grants
Integrated services such as EBS create grants; review them with `aws kms list-grants --key-id <id>` and retire unused ones. The default key policy lets key users delegate grant permission to all integrated services; `kms:ViaService` can restrict that to specified services.

## Monitoring
Alert on CloudTrail `ScheduleKeyDeletion` events. The deletion waiting period is 7 to 30 days; a key is unusable for cryptographic operations as soon as deletion is scheduled, and `kms:ScheduleKeyDeletionPendingWindowInDays` can enforce a minimum waiting period.

## Gotchas
- `"Principal": "*"` with weak conditions exposes the key to other accounts.
- The key policy decides who can have access; the IAM policy decides who does have it.

## Verify
- [ ] IAM Access Analyzer reports no external access to keys except intended.
- [ ] Test: app role can decrypt through S3 but direct `aws kms decrypt` fails.

## Checked
Checked 2026-11-09 against the AWS KMS Developer Guide pages in `sources` (default key policy, condition keys, cross-account access, encryption context, grants, key deletion); `aws kms list-grants` verified with the command checker. Removed unconfirmed claims: the S3 encryption-context ARN condition, multi-Region policy behaviour, the NIST and Security Reference Architecture sources, and DisableKey/PutKeyPolicy/Decrypt alert examples.
Method: documentation only; no commands were run.
