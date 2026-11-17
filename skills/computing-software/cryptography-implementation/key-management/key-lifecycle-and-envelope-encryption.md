---
id: computing-software.cryptography-implementation.key-management.key-lifecycle-and-envelope-encryption
name: key-lifecycle-and-envelope-encryption
category: computing-software
field: cryptography-implementation
product: key-management
tags: [cryptography-implementation, key-management, kms, aws-kms, gcp-cloud-kms, azure-key-vault, envelope-encryption, generatedatakey, kek, dek, key-hierarchy, key-rotation, key-wrapping, hsm, secrets-manager, hashicorp-vault, crypto-period, nist-sp-800-57, encryption-context, crypto-shredding, key-destruction, separation-of-duties, tink, aws-encryption-sdk]
level: advanced
status: gated
description: "Manage keys across their lifecycle and use envelope encryption with AWS KMS, GCP Cloud KMS or Azure Key Vault: KEK/DEK hierarchy, key ids in headers, cheap rotation, access split, destruction."
sources: ["https://csrc.nist.gov/pubs/sp/800/57/pt1/r5/final", "https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html", "https://cloud.google.com/kms/docs/envelope-encryption", "https://learn.microsoft.com/en-us/azure/key-vault/general/basic-concepts", "https://cheatsheetseries.owasp.org/cheatsheets/Key_Management_Cheat_Sheet.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Key lifecycle and envelope encryption

**Goal:** no long-lived plaintext key ever sits in code, config or an environment
variable. Data is encrypted under data keys (DEKs) that are wrapped by a master key
(KEK) that never leaves a KMS/HSM, so rotation and revocation are cheap and auditable.

## 1. The lifecycle (NIST SP 800-57 vocabulary)
Generate → (pre-activation) → **active** → deactivated (decrypt/verify only) →
destroyed, with **compromised** as an exit from any state. For each key class, record
where it is generated (CSPRNG in a KMS/HSM), where it is stored, what it may do,
its crypto-period, and how it is rotated, revoked, backed up and destroyed.

## 2. Envelope encryption
```
KMS/HSM:  KEK (never exported)
            │ wraps
App:      DEK (random 256-bit, one per object / tenant / file)
            │ encrypts (AES-256-GCM)
Stored:   header ‖ wrapped DEK ‖ nonce ‖ ciphertext ‖ tag
```
**AWS KMS:**
```
aws kms generate-data-key --key-id alias/app-data --key-spec AES_256 \
  --encryption-context tenant=t-123,purpose=invoices
```
This returns `Plaintext` (use it, then wipe it; AWS CLI/KMS behaviour here is from documentation, not run, no AWS account) (gated: unconfirmed, source is paywalled or blocked) and `CiphertextBlob` (store it). To
decrypt, call `Decrypt` on the blob with the **same encryption context**. KMS treats
the context as AAD and records it in CloudTrail, so tenant-binding comes free.
Symmetric KMS ciphertext carries the key reference, so `Decrypt` does not need the
key id, but pass `--key-id` anyway so a blob wrapped under a different key is refused.

**GCP Cloud KMS:** there is no GenerateDataKey. Generate the DEK locally from the
CSPRNG, then `cryptoKeys.encrypt` it with the KEK, using
`additionalAuthenticatedData` for context. Tink's KMS envelope AEAD wraps this pattern.

**Azure Key Vault:** `wrapKey`/`unwrapKey` with an RSA key (`RSA-OAEP-256`), or
AES key wrap on Managed HSM.

Prefer the AWS Encryption SDK or Tink to a home-made format.

## 3. Ciphertext header
```
magic(2) | format_version(1) | kek_id(len-prefixed) | wrapped_dek(len-prefixed) | nonce(12) | ct‖tag
```
Pass the whole header as AAD to the data AEAD so that no field can be swapped. The
key id makes rotation possible: the reader knows which KEK version (or local key) to
ask for.

## 4. Rotation without re-encrypting everything
- **KEK rotation:** KMS-managed rotation keeps old key versions for decrypt and uses
  the new one for encrypt. AWS can rotate automatically (default one year, configurable period; check current options (gated: unconfirmed, source is paywalled or blocked)). The GCP rotation schedule sets a new
  primary version. Optionally **re-wrap** DEKs in the background (unwrap with the
  old version, wrap with the new). That touches a few bytes per object, not the data.
- **DEK rotation:** new data gets new DEKs automatically when you generate one per
  object. Re-encrypt old objects lazily on the next write.
- **Compromise:** a compromise is different. Revoke and disable the KEK, re-encrypt
  affected data under new keys, and investigate access logs.

## 5. Crypto-periods (guidance, not law)
SP 800-57 Part 1 Rev. 5 Table 1 suggests: symmetric data-encryption keys and symmetric key-wrapping keys an originator usage period (OUP) under 2 years and a recipient usage period under OUP + 3 years; a symmetric master/key-derivation key about 1 year; private signature keys 1 to 3 years. In
practice: one year for KEKs, per-object DEKs, and immediate rotation when someone
with access leaves or a compromise is suspected.

## 6. Access and separation of duties
- Key **administrators** (create, rotate, schedule deletion, edit policy) are not key
  **users** (encrypt/decrypt). Enforce this in key policy/IAM, not by convention.
- Give encrypt-only to writers and decrypt to the narrowest reader set. Alert on
  unusual `Decrypt` volume.
- Require MFA or approval for deletion. AWS KMS enforces a waiting period of 7 to 30 days before deletion (gated: unconfirmed, source is paywalled or blocked); use it.

## 7. Secrets that aren't KMS keys
Keep API tokens and DB passwords in a secrets manager (HashiCorp Vault, AWS Secrets
Manager, GCP Secret Manager, Azure Key Vault secrets) and fetch them at runtime using
workload identity. Plain environment variables leak through process listings, crash
dumps, debug endpoints and child processes. Run gitleaks or trufflehog in CI;
rotate anything ever committed.

## 8. Backups and destruction
Backups of encrypted data are useless without the keys, and the keys are useless
without access to them. Test restore end to end, including the KMS dependency. Use
HSM backup or M-of-N key ceremonies for root keys. **Crypto-shredding:** destroying
a tenant's KEK/DEK makes their data unrecoverable, including in backups. Useful for
erasure requests; catastrophic by accident.

## Verify
- [ ] No plaintext key or secret in the repo, images, env files or logs (scanner passes).
- [ ] Every ciphertext carries a version and key id, and the header is authenticated.
- [ ] Rotating the KEK leaves old data decryptable, as a test.
- [ ] Admin and user roles for keys are separate principals.
- [ ] Deletion requires approval and has a waiting period.
- [ ] A restore drill and a compromise runbook exist and have been exercised.
