---
id: computing-software.cloud-infrastructure-engineering.aws.kms-aliases-in-applications
name: kms-aliases-in-applications
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, kms, kms-alias, key-identification, key-rotation]
level: practitioner
status: docs-checked
description: "Use KMS aliases to decouple applications from key IDs: create and repoint aliases, know where aliases are rejected, and scope access with alias conditions."
sources: ["https://docs.aws.amazon.com/kms/latest/developerguide/kms-alias.html", "https://docs.aws.amazon.com/kms/latest/developerguide/alias-authorization.html", "https://docs.aws.amazon.com/kms/latest/developerguide/resource-limits.html", "https://docs.aws.amazon.com/kms/latest/developerguide/key-policy-modifying-external-accounts.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# KMS aliases and key identification

## 1. Four ways to name a key
| Form | Example | Works cross-account |
|---|---|---|
| Key ID | `1234abcd-12ab-...` | no |
| Key ARN | `arn:aws:kms:<REGION>:<ACCOUNT_ID>:key/1234abcd-...` | yes |
| Alias name | `alias/app/prod` | no |
| Alias ARN | `arn:aws:kms:<REGION>:<ACCOUNT_ID>:alias/app/prod` | yes, for cryptographic operations, `DescribeKey` and `GetPublicKey` |
For a key in another account, use the key ARN or alias ARN for those operations; use the key ARN for `CreateGrant`, `GetKeyRotationStatus`, `ListGrants` and `RevokeGrant`. A bare key ID or alias name is assumed to be in your own account.

## 2. Create and repoint
```bash
aws kms create-alias --alias-name alias/app/prod --target-key-id <KEY_ID>
aws kms update-alias --alias-name alias/app/prod --target-key-id <NEW_KEY_ID>   # repoint to a new key
aws kms list-aliases --key-id <KEY_ID>
```
Repointing does not re-encrypt data. The new and old key must be the same type (both symmetric, both asymmetric or both HMAC) with the same key usage. An alias is an independent resource, not a property of the key. Symmetric `Decrypt` needs no key ID because KMS stores it in the ciphertext blob (API documentation for `Encrypt`), so keep the old key enabled until old data is re-encrypted.
An alias name is unique per account and Region, is case-sensitive, and cannot be renamed (delete and recreate). Each customer managed key can have up to 50 aliases (quota page, read 2026-10-27; adjustable).

## 3. Where aliases work
- Cryptographic operations (for example `Encrypt` and `GenerateDataKey`), `DescribeKey` and `GetPublicKey` accept an alias name or alias ARN.
- Other operations take key IDs or ARNs; check the `KeyId` parameter description in the API reference for each.
- You cannot identify a key by alias in an IAM policy: an alias in `Resource` refers to the alias itself. Use the `kms:RequestAlias` or `kms:ResourceAliases` condition keys to allow or deny by alias.

## 4. Access control by alias
```json
{"Effect":"Allow","Action":["kms:Encrypt","kms:Decrypt","kms:GenerateDataKey"],"Resource":"*",
 "Condition":{"ForAnyValue:StringLike":{"kms:ResourceAliases":"alias/app/*"}}}
```
`kms:RequestAlias` matches the alias used in the request. Be cautious granting `kms:CreateAlias`, `kms:UpdateAlias` or `kms:DeleteAlias`: changing an alias can grant or remove access under alias-based conditions. `kms:ResourceAliases` is effective only while the key is within the 50-aliases-per-key quota; beyond it, principals relying on that condition are denied.

## Gotchas
- An alias and its key must be in the same account and Region, so each Region (including each multi-Region replica) needs its own alias; the same alias name can exist in several Regions.
- `alias/aws/<service>` aliases are created by AWS for AWS managed keys; you cannot associate an alias with an AWS managed key.
- Aliases appear in plaintext in CloudTrail; keep sensitive data out of alias names.

## Verify
- [ ] Application config contains alias names only; `aws kms describe-key --key-id alias/app/prod` returns the expected key.

## Checked
2026-10-27. Documentation: AWS KMS Developer Guide (Aliases in AWS KMS, Use aliases to control access, resource quotas, allowing users in other accounts) and the UpdateAlias/Encrypt API documentation in the KMS service model, read this date. Confirmed: alias ARNs are valid cross-account identifiers for cryptographic operations, DescribeKey and GetPublicKey (the draft said they were not), same-type and same-usage rule for UpdateAlias, no alias in IAM Resource, kms:RequestAlias and kms:ResourceAliases, 50 aliases per key quota, same account and Region, no rename. Removed unconfirmed statements about which other operations accept aliases.
Method: documentation only; no commands were run.
