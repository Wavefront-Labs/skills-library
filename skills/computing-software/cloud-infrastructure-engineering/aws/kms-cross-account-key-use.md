---
id: computing-software.cloud-infrastructure-engineering.aws.kms-cross-account-key-use
name: kms-cross-account-key-use
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, kms, cross-account-kms, external-account-key-use, key-policy, encrypted-snapshot-sharing, s3-cross-account-kms]
level: advanced
status: docs-checked
description: "Let another account use a KMS key: the two-sided key policy plus IAM policy, which operations work cross-account, key ARN or alias ARN identifiers, ViaService scoping and grants."
sources: ["https://docs.aws.amazon.com/kms/latest/developerguide/key-policy-modifying-external-accounts.html", "https://docs.aws.amazon.com/kms/latest/developerguide/conditions-kms.html", "https://docs.aws.amazon.com/kms/latest/developerguide/grants.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cross-account use of a KMS key

**Rule:** cross-account KMS access needs **both** sides to agree. The key policy in the key
owner's account must allow the external account (or a role in it), and an IAM policy in
the external account must allow its principal to use that key ARN.

## 1. Key owner: key policy statement
```json
{"Sid": "AllowUseByAnalyticsAccount", "Effect": "Allow",
 "Principal": {"AWS": "arn:aws:iam::444455556666:role/AnalyticsReader"},
 "Action": ["kms:Decrypt", "kms:DescribeKey"],
 "Resource": "*",
 "Condition": {"StringEquals": {"kms:ViaService": "s3.eu-west-1.amazonaws.com"}}}
```
- Naming a role (rather than the account) limits the permissions the external IAM administrators can delegate; if you name the account, its IAM administrators can delegate to any of its users and roles. Never use `Principal: "*"` without conditions.
- Cross-account permission is effective only if the external account is enabled in the Region that hosts the key (opt-in Regions).
- Add `kms:Encrypt`, `kms:GenerateDataKey*`, `kms:ReEncrypt*` for writers.
- For services that create grants on your behalf (EBS, RDS, Redshift, Aurora), also
  allow `kms:CreateGrant` with `"Bool": {"kms:GrantIsForAWSResource": "true"}`.

## 2. External account: IAM policy
```json
{"Effect": "Allow", "Action": ["kms:Decrypt", "kms:DescribeKey"],
 "Resource": "arn:aws:kms:eu-west-1:111122223333:key/1234abcd-..."}
```
Use the **key ARN** in IAM `Resource`. Cross-account permission is effective only for cryptographic operations, `CreateGrant`, `DescribeKey`, `GetKeyRotationStatus`, `GetPublicKey`, `ListGrants`, `RetireGrant` and `RevokeGrant`; other permissions given to an external principal have no effect. When calling, a key ARN or alias ARN works for cryptographic operations, `DescribeKey` and `GetPublicKey`; a bare alias name or key ID is looked up in the caller's own account. The IAM policy can only delegate actions the key policy allows, and only to principals the key policy names. Use calls are logged in both accounts' CloudTrail.

## 3. Services and AWS managed keys
To use your key with a service in another account (for example S3 or Secrets Manager), the key policy must allow the external user or account, the external identity needs IAM permission for the service, and the service may need extra key permissions; read the service's data-protection page for the exact list. For services that create grants for resources (EBS, RDS and similar), allow `kms:CreateGrant` with the `kms:GrantIsForAWSResource` condition shown above. Check the service documentation before sharing encrypted snapshots or AMIs; the required key type and permissions differ by service.

## 5. Grants instead of policy edits
For programmatic, revocable access (e.g. a pipeline granting a specific role for one job):
```bash
aws kms create-grant --key-id <key-arn> --grantee-principal arn:aws:iam::444455556666:role/Job \
  --operations Decrypt DescribeKey --constraints EncryptionContextSubset={project=alpha}
aws kms revoke-grant --key-id <key-arn> --grant-id <id>
```
Operation names come from the CreateGrant API model (for example `Decrypt`, `Encrypt`, `GenerateDataKey`, `DescribeKey`). For cross-account `CreateGrant`, `RevokeGrant` and `ListGrants` use the key ARN. The KMS API is eventually consistent; use the returned grant token to use a new grant immediately.

## Troubleshooting
- An access-denied error names whether the missing permission is on the resource (key policy) or identity side; check both policies.
- Check CloudTrail in both the key owner's and the caller's account for the KMS call and its error.
- `kms:ViaService` takes a Region-qualified service endpoint such as `ec2.us-west-2.amazonaws.com` (documented example).

## Verify
- [ ] From the external role, `aws kms describe-key --key-id <arn>` succeeds and a sample S3 GET of a KMS-encrypted object works.
- [ ] Another role in the external account is denied.
- [ ] Key-owner CloudTrail shows the external `Decrypt` calls.

## Checked
2026-10-27. Documentation: AWS KMS Developer Guide (allowing users in other accounts to use a KMS key, KMS condition keys, resource quotas) and KMS API model documentation, read this date. Confirmed: two-policy requirement, list of operations that work cross-account, key ARN or alias ARN rules (the draft said aliases cannot be used cross-account), opt-in Region note, root versus named principal, kms:ViaService value format, kms:GrantIsForAWSResource, grant operation names. Removed unconfirmed claims on role-recreation behaviour, per-service snapshot and bucket steps, AWS managed key policies, error message wording and CloudTrail encryption-context conditions.
Method: documentation only; no commands were run.
