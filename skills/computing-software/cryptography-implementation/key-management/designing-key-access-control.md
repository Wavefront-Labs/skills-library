---
id: computing-software.cryptography-implementation.key-management.designing-key-access-control
name: designing-key-access-control
category: computing-software
field: cryptography-implementation
product: key-management
tags: [cryptography-implementation, key-management, key-management-policy, key-access-control, least-privilege, iam-conditions, encryption-context-condition, workload-identity, per-tenant-keys]
level: advanced
status: docs-checked
description: "Design who can use which key: per-service and per-tenant key boundaries, least-privilege operations, context-bound conditions, and reviewing effective access."
sources: ["https://docs.aws.amazon.com/kms/latest/developerguide/control-access.html", "https://cloud.google.com/kms/docs/reference/permissions-and-roles", "https://csrc.nist.gov/pubs/sp/800/57/pt1/r5/final"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Designing key access control

Encryption only moves the access-control problem to the key. If every service
can call Decrypt on the one shared key, encryption adds little against an
insider or a compromised service. Design the key boundaries as deliberately as
the data boundaries.

## Granularity

- **One key per data domain and environment**: `prod-payments-pii`,
  `prod-analytics`, never shared between prod and staging.
- **Per-tenant keys** where tenants need isolation guarantees or
  customer-managed keys (CMK/BYOK). Cost and quotas grow with key count; a
  common compromise is per-tenant DEKs under a per-region KEK, with
  encryption context binding the tenant id.
- **Separate keys per operation type** (signing vs encryption) - required
  anyway by key usage rules.

## Least-privilege operations

| Role | Allowed |
|---|---|
| Writer service | `Encrypt`, `GenerateDataKey` only |
| Reader service | `Decrypt` only, ideally constrained by context |
| Batch re-encryption job | `ReEncrypt*` temporarily |
| Signing service | `Sign`; verifiers use the public key offline, no KMS call |

Writers that cannot decrypt limit the blast radius of an ingest-path compromise.

## Conditions

- AWS: `kms:EncryptionContext:tenant` must equal the caller's tenant tag
  (`${aws:PrincipalTag/tenant}`), `kms:ViaService` to force use through a
  specific AWS service, `kms:CallerAccount`.
- GCP: IAM Conditions on resource name; per-key IAM bindings rather than
  project-level `roles/cloudkms.cryptoKeyEncrypterDecrypter`.
- Azure Key Vault: use RBAC (`Key Vault Crypto User` scoped to a single key)
  over legacy access policies.

```json
{"Effect":"Allow","Principal":{"AWS":"arn:aws:iam::<acct>:role/reader"},
 "Action":"kms:Decrypt","Resource":"*",
 "Condition":{"StringEquals":{"kms:EncryptionContext:tenant":"${aws:PrincipalTag/tenant}"}}}
```

## Review

- Enumerate effective access per key (AWS key policies and IAM policies,
  `gcloud kms keys get-iam-policy`, Azure role assignments) quarterly.
- Alert on key policy changes (see key usage audit skill).
- Remove project/account-wide KMS roles; bind per key.

## Verify

- [ ] Writer roles get AccessDenied on Decrypt.
- [ ] A tenant-A principal cannot decrypt tenant-B context data.
- [ ] No wildcard principals or project-wide decrypt roles on production keys.

## Checked

2026-11-01. Confirmed in the AWS KMS condition-keys page (kms:CallerAccount, kms:ViaService, encryption-context condition keys), the Cloud KMS permissions and roles page (cryptoKeyEncrypterDecrypter role) and the Azure Key Vault RBAC guide (Key Vault Crypto User, RBAC over access policies). `gcloud kms keys get-iam-policy` exists per the command checker. Removed the unconfirmed IAM Access Analyzer for KMS claim. Key and tenant names in examples are illustrative.
Method: documentation only; no commands were run.
