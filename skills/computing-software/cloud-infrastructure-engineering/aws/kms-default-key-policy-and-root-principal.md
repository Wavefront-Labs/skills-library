---
id: computing-software.cloud-infrastructure-engineering.aws.kms-default-key-policy-and-root-principal
name: kms-default-key-policy-and-root-principal
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, kms, default-key-policy, kms-root-principal, key-policy, iam]
level: advanced
status: docs-checked
description: "Understand the KMS default key policy and the account-root statement that lets IAM policies grant key access, and recover from unmanageable keys."
sources: ["https://docs.aws.amazon.com/kms/latest/developerguide/key-policy-default.html", "https://docs.aws.amazon.com/kms/latest/developerguide/key-policy-overview.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# KMS default key policy and enabling IAM policies

## 1. The statement that matters
```json
{"Sid":"Enable IAM User Permissions","Effect":"Allow",
 "Principal":{"AWS":"arn:aws:iam::<ACCOUNT_ID>:root"},"Action":"kms:*","Resource":"*"}
```
The principal is the account principal (`arn:aws:iam::<account-id>:root`), which represents the account and its administrators, not just the root user. It allows the account to use IAM policies to delegate `kms:*` on the key. A KMS key policy does not automatically grant the account anything, so without this statement IAM policies alone do not work; only principals named in the key policy get access, and the key can become unmanageable.

## 2. What the console default adds
- Key administrators (console default): `kms:Create*`, `Describe*`, `Enable*`, `List*`, `Put*`, `Update*`, `Revoke*`, `Disable*`, `Get*`, `Delete*`, `TagResource`, `UntagResource`, `ScheduleKeyDeletion`, `CancelKeyDeletion` and `RotateKeyOnDemand`; they get no cryptographic use. Tag and alias permissions can change access to the key under ABAC.
- Key users: cryptographic permissions (encrypt, decrypt, re-encrypt, generate data key, describe).
- Grants for AWS services: `kms:CreateGrant`, `ListGrants` and `RevokeGrant` with `"Bool":{"kms:GrantIsForAWSResource":"true"}`.
The default key policy for keys created programmatically is only the root statement; the console adds it as the first statement.

## 3. Inspect and change
```bash
aws kms get-key-policy --key-id <KEY_ID> --policy-name default --output text > policy.json
aws kms put-key-policy --key-id <KEY_ID> --policy-name default --policy file://policy.json
```
`PutKeyPolicy` has a key policy lockout safety check, and its `BypassPolicyLockoutSafetyCheck` parameter skips it (default false). The API documentation says to set it true only when you intend to stop the calling principal from making a later `PutKeyPolicy` request; it raises the risk of an unmanageable key.

## 4. Tight variant
Keep the root statement unless you have a durable alternative administrator. Policies can narrow use with condition keys such as `kms:CallerAccount` and `kms:ViaService`; see the KMS condition keys page.

## Recovery
If no principal can manage the key, the key policy page says to contact AWS Support to regain access. Prevent this by reviewing key policies before saving changes.

## Verify
- [ ] Every customer managed key either has the root statement or names a durable admin role.
- [ ] An IAM role with only an identity policy for `kms:Decrypt` can decrypt (proves delegation works).

## Checked
2026-10-27. Documentation: AWS KMS Developer Guide (default key policy, key policies overview, KMS condition keys) and the PutKeyPolicy API model documentation, read this date. Confirmed: the root statement text and meaning, console key administrator action list, grant statement and kms:GrantIsForAWSResource, programmatic default policy, lockout safety check parameter, AWS Support recovery. Removed the claim that an SCP or Config rule is the prevention mechanism and unsourced condition-key suggestions.
Method: documentation only; no commands were run.
