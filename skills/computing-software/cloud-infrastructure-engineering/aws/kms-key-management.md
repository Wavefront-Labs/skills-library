---
id: computing-software.cloud-infrastructure-engineering.aws.kms-key-management
name: kms-key-management
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, kms, aws-kms, envelope-encryption, key-policy, cmk, customer-managed-key, encryption-at-rest, data-key, generate-data-key, encryption-context, key-rotation, multi-region-keys, grants, kms-viaservice, s3-bucket-keys, key-alias, schedule-key-deletion, cloudhsm, external-key-store, xks, asymmetric-keys, hmac, encryption]
level: advanced
status: docs-checked
description: "Run AWS KMS: key types, a key policy that cannot lock you out, envelope encryption and encryption context, rotation, multi-region keys and request quotas."
sources: ["https://docs.aws.amazon.com/kms/latest/developerguide/key-policy-default.html", "https://docs.aws.amazon.com/kms/latest/developerguide/data-keys.html", "https://docs.aws.amazon.com/kms/latest/developerguide/rotate-keys.html", "https://docs.aws.amazon.com/kms/latest/developerguide/multi-region-keys-overview.html", "https://docs.aws.amazon.com/kms/latest/developerguide/requests-per-second.html", "https://docs.aws.amazon.com/kms/latest/developerguide/deleting-keys-scheduling-key-deletion.html", "https://docs.aws.amazon.com/kms/latest/developerguide/encrypt_context.html", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/bucket-key.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AWS KMS key management — keys you can audit, rotate and never lose

**Goal:** every service encrypts at rest under a key whose policy a reviewer can read,
whose use is scoped by service and context, whose rotation is automatic, and whose
deletion is survivable. Policy-document authoring in general is in
`computing-software.cloud-infrastructure-engineering.aws.iam-policy-design`.

## 1. Which key type
| Key | Who owns policy | Cross-account | Rotation |
|---|---|---|---|
| AWS owned (`SSE-S3`, DynamoDB default) | AWS | n/a | managed by the owning service |
| AWS managed (`aws/s3`, `aws/rds`) | AWS (fixed policy) | no | every year, cannot be changed |
| Customer managed (CMK) | you | yes | optional, configurable |
KMS charges for customer managed keys and API calls; see the KMS pricing page.
Use a **customer managed key** whenever you need cross-account access, a deny statement,
`kms:ViaService` scoping, or the ability to revoke access by changing policy. One key per
data classification per environment is a sane default.

Symmetric `ENCRYPT_DECRYPT` covers nearly everything. Asymmetric (RSA/ECC) only for
signing or encrypting outside AWS; HMAC keys for tokens; `SIGN_VERIFY` ECC_NIST_P256 for
JWT-style signatures. Asymmetric keys, HMAC keys and keys in custom key stores support neither
automatic nor on-demand rotation (rotate them manually with a new key and an alias swap).

Create: `aws kms create-key --description "app-data prod" --tags TagKey=env,TagValue=prod`
then `aws kms create-alias --alias-name alias/app-data-prod --target-key-id <KEY_ID>`.
Always address keys by alias in application config; swap the alias target to re-key.

## 2. Key policy that cannot lock you out
A key policy is the *only* policy that grants by default — IAM policies work on a key
only if the key policy delegates to them. Keep this statement or nothing in IAM applies:
```json
{"Sid": "EnableIAMUserPermissions", "Effect": "Allow",
 "Principal": {"AWS": "arn:aws:iam::<ACCOUNT_ID>:root"}, "Action": "kms:*", "Resource": "*"}
```
Then add scoped statements:
- **Administrators** (`kms:Create*`, `Describe*`, `Enable*`, `Put*`, `Update*`,
  `Revoke*`, `Disable*`, `Get*`, `Delete*`, `ScheduleKeyDeletion`, `CancelKeyDeletion`)
  — no `kms:Encrypt`/`Decrypt`; admins manage, they do not read data.
- **Users** (`kms:Encrypt`, `Decrypt`, `ReEncrypt*`, `GenerateDataKey*`, `DescribeKey`)
  with a condition such as `"kms:ViaService": "s3.<region>.amazonaws.com"` or
  `"kms:EncryptionContext:aws:rds:db-id": "<DB_ID>"` so the key is only usable through
  the intended service.
- Cross-account: name the external account's root principal in the key policy, then that
  account's IAM policies narrow access down (see the KMS cross-account access page).
A `Deny` with `kms:*` and a wrong condition is a classic self-lockout; test policy changes on
a non-production key first.

## 3. Envelope encryption done right
`Encrypt` accepts at most 4,096 bytes of plaintext per call. Everything larger uses **data keys**:
1. `aws kms generate-data-key --key-id alias/app-data-prod --key-spec AES_256
   --encryption-context purpose=invoice,tenant=<ID>` → plaintext key + `CiphertextBlob`.
2. Encrypt the payload locally with the plaintext key (AES-GCM), zero the plaintext,
   store the ciphertext blob beside the data.
3. To read: `aws kms decrypt --ciphertext-blob fileb://blob --encryption-context ...`
   (same context, or KMS refuses) → plaintext key → decrypt locally.
Use the **AWS Encryption SDK** or S3/EBS/RDS native SSE-KMS rather than hand-rolling
this; they add key caching (`GenerateDataKey` once per N messages) which is what keeps
you under the request quota.

**Encryption context** is authenticated-but-not-secret metadata: it binds a ciphertext
to a purpose, appears in CloudTrail, and is usable in policy conditions. Always set it.

## 4. Rotation, multi-region, deletion
- Automatic rotation: `aws kms enable-key-rotation --key-id <ID> --rotation-period-in-days 180`
  (90–2560; default 365). Old material stays for decrypting old ciphertext; nothing
  needs re-encrypting. `rotate-key-on-demand` suits an incident. On-demand rotation covers
  symmetric encryption keys with AWS_KMS or EXTERNAL (imported) material. AWS managed keys
  rotate every year and cannot be changed.
- **Multi-Region keys** (`--multi-region`, then `replicate-key --replica-region`) share
  key id and material so a ciphertext from one Region decrypts in another without a
  cross-Region call. They are *not* global keys: each replica is a fully functional key with
  its own key policy, grants, alias and tags, managed independently. They cannot be created in a
  custom key store.
- Imported key material (`origin EXTERNAL`); CloudHSM key stores and **external key stores
  (XKS)** put the material in hardware you control at an operational cost, so use them only
  for a regulatory mandate.
- Deletion: `schedule-key-deletion --pending-window-in-days 30` (the console accepts 7–30; the
  `kms:ScheduleKeyDeletionPendingWindowInDays` condition key can enforce a minimum). Disable first
  (`disable-key`) for a month and watch CloudTrail for `Decrypt` failures; anything
  encrypted under a deleted key is gone forever, including snapshots and S3 objects.

## 5. Cost and quota control
- The cryptographic-operations request quota is per account and Region and shared across
  symmetric (and HMAC) operations such as `GenerateDataKey`, `Encrypt` and `Decrypt`; the
  AWS docs give 100,000 per second for us-east-1 and 10,000 for Europe (London) and Asia
  Pacific (Singapore). RSA and ECC keys have separate, lower quotas, and each custom key store
  has its own. Look up your Region's value on the KMS request quotas page. Requests above the
  quota get `ThrottlingException`.
- **S3 Bucket Keys** (`--server-side-encryption-configuration ... BucketKeyEnabled=true`)
  reduce the request traffic from S3 to KMS for SSE-KMS buckets. They use the bucket ARN as
  encryption context, so IAM or key policies that match on the object ARN stop working: update
  them before enabling Bucket Keys. KMS CloudTrail events then log the bucket ARN.

## Gotchas
- Test with `aws kms encrypt --key-id ... --plaintext ...` from the same role to separate
  policy errors from service wiring.

## Verify
- [ ] Every CMK key policy retains the account-root statement and separates admin from use.
- [ ] Use statements carry `kms:ViaService` or `kms:EncryptionContext` conditions.
- [ ] Automatic rotation enabled on all symmetric CMKs; `get-key-rotation-status` confirms.
- [ ] Bucket Keys enabled on SSE-KMS buckets; KMS request count dropped in CloudWatch.
- [ ] A disable-key dry run on a non-prod key surfaces every dependent workload in CloudTrail before any deletion is scheduled.

## Checked
2026-10-31. Confirmed against the AWS KMS Developer Guide pages on the default key policy (account root `kms:*` statement delegates to IAM), rotation (default 365 days, `RotationPeriodInDays` 90-2560 in the botocore model, AWS managed keys yearly, on-demand scope, manual rotation for asymmetric, HMAC and custom key store keys), multi-Region keys (shared key ID and material, independent replicas, not global, not in custom key stores), request quotas (shared symmetric quota, separate RSA/ECC/custom key store quotas, the 100,000 and 10,000 per second examples), scheduling key deletion (console 7-30 days) and the botocore `Encrypt` plaintext limit of 4,096 bytes, the encryption context page (not secret, appears in CloudTrail, usable in conditions and grants) and the S3 Bucket Keys page (bucket ARN context). Removed as unconfirmed: all prices, the Bucket Key percentage saving, the per-Region rps figures that no longer match the docs, the DynamoDB global tables use case, the EBS boot-time Decrypt remark, alias scoping and the self-lockout recovery path.
Method: documentation only; no commands were run.
