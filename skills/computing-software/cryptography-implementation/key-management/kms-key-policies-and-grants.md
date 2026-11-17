---
id: computing-software.cryptography-implementation.key-management.kms-key-policies-and-grants
name: kms-key-policies-and-grants
category: computing-software
field: cryptography-implementation
product: key-management
tags: [cryptography-implementation, key-management, kms, cloud-kms, kms-key-policy, kms-grants, aws-kms, iam, cross-account-kms, lockout-prevention]
level: advanced
status: docs-checked
description: "Write AWS KMS key policies and grants correctly: the root-account statement, admin vs user separation, cross-account use, grants for services, and avoiding unmanageable keys."
sources: ["https://docs.aws.amazon.com/kms/latest/developerguide/key-policies.html", "https://docs.aws.amazon.com/kms/latest/developerguide/grants.html", "https://docs.aws.amazon.com/kms/latest/developerguide/key-policy-modifying-external-accounts.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# KMS key policies and grants

In AWS KMS the **key policy** is the primary access control: IAM policies only
apply if the key policy delegates to IAM. Mistakes either lock everyone out
or let any role in the account decrypt.

## The default "root" statement

```json
{"Sid":"EnableIAMPolicies","Effect":"Allow",
 "Principal":{"AWS":"arn:aws:iam::111122223333:root"},
 "Action":"kms:*","Resource":"*"}
```

This does **not** grant the root user only; it lets IAM policies in the
account grant access to the key. Keep it (or an equivalent admin path)
unless you deliberately want key-policy-only control. Removing it without
another admin principal can make the key unmanageable. Do not bypass the
`PutKeyPolicy` lockout check with `--bypass-policy-lockout-safety-check`.

## Separate administrators and users

```json
{"Sid":"KeyAdmins","Effect":"Allow","Principal":{"AWS":"arn:aws:iam::111122223333:role/kms-admin"},
 "Action":["kms:Create*","kms:Describe*","kms:Enable*","kms:List*","kms:Put*","kms:Update*",
           "kms:Revoke*","kms:Disable*","kms:Get*","kms:Delete*","kms:TagResource","kms:UntagResource",
           "kms:ScheduleKeyDeletion","kms:CancelKeyDeletion","kms:RotateKeyOnDemand"],"Resource":"*"},
{"Sid":"KeyUsers","Effect":"Allow","Principal":{"AWS":"arn:aws:iam::111122223333:role/app"},
 "Action":["kms:Encrypt","kms:Decrypt","kms:ReEncrypt*","kms:GenerateDataKey*","kms:DescribeKey"],
 "Resource":"*",
 "Condition":{"StringEquals":{"kms:EncryptionContext:app":"billing"}}}
```

## Cross-account

Both sides must allow: the key policy in account A names account B (or a
role in B), and an IAM policy in B grants its principals `kms:Decrypt` on the
key. Use the key ARN or alias ARN from the other account for cryptographic
operations (a bare key ID or alias name is assumed to be in your own account);
`CreateGrant` and `ListGrants` need the key ARN. Restrict with
`kms:ViaService` / `kms:CallerAccount` conditions where possible.

## Grants

Grants give temporary, narrowly scoped permissions, typically to AWS services
that create grants on your behalf and retire them when done:

```bash
aws kms create-grant --key-id <arn> --grantee-principal arn:aws:iam::111122223333:role/worker \
  --operations Decrypt GenerateDataKey --constraints EncryptionContextSubset={tenant=42}
aws kms list-grants --key-id <arn>
aws kms retire-grant --grant-token <token>   # or revoke-grant
```

Grants are eventually consistent (use the grant token, returned only by
`CreateGrant`, for immediate use); audit and retire them.

## Checked

2026-10-31. Confirmed in AWS KMS docs: default key policy (account root statement enables IAM policies), cross-account (key policy and IAM policy both needed; key identifier rules), grants (eventual consistency, grant token from CreateGrant only, services create and retire grants). Removed: AWS Support recovery, grant-visibility claim to IAM tools, GCP and Azure role names (not checked).

Method: documentation only; no commands were run.

## Verify

- [ ] Every key has a policy with an admin path and least-privilege user statements.
- [ ] Grants listed and justified; unused grants retired.
