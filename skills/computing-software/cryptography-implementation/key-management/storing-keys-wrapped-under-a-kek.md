---
id: computing-software.cryptography-implementation.key-management.storing-keys-wrapped-under-a-kek
name: storing-keys-wrapped-under-a-kek
category: computing-software
field: cryptography-implementation
product: key-management
tags: [cryptography-implementation, key-management, key-storage, wrapped-key-storage, kek, dek, key-hierarchy, keyring, key-wrapping, master-key]
level: advanced
status: gated
description: "Persist keys only in wrapped form under a KEK held in KMS/HSM: keyring record layout, unwrap-on-start and caching, KEK rotation by rewrap, and bootstrapping the root."
sources: ["https://csrc.nist.gov/pubs/sp/800/57/pt1/r5/final", "https://cheatsheetseries.owasp.org/cheatsheets/Cryptographic_Storage_Cheat_Sheet.html", "https://developers.google.com/tink/client-side-encryption"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Storing keys wrapped under a KEK

The OWASP Cryptographic Storage Cheat Sheet says encryption keys should, where possible, be stored in an encrypted form and in a separate location from the encrypted data. The standard pattern is a key
hierarchy: data encryption keys (DEKs) stored wrapped by a key-encryption key
(KEK), which lives in a KMS/HSM and never leaves it.

## Keyring record

```json
{
  "key_id": "dek-2026-10-a1b2",
  "purpose": "users.pii field encryption",
  "algorithm": "AES-256-GCM",
  "wrapped_key": "<base64 ciphertext>",
  "kek_ref": "arn:aws:kms:eu-west-1:<acct>:key/<uuid>",
  "wrap_alg": "KMS-SYMMETRIC_DEFAULT | AES-KWP",
  "status": "active | decrypt-only | destroyed",
  "created": "2026-10-16T00:00:00Z"
}
```

Tink keysets encrypted with a KMS KEK (`KeysetHandle.write(..., kmsAead)`)
implement exactly this.

## Runtime

1. On start (or first use), load the keyring and unwrap needed DEKs via KMS
   (`Decrypt`), or with the HSM KEK (`C_UnwrapKey`).
2. Cache unwrapped DEKs in memory with a TTL (minutes to hours); limits KMS
   calls and limits exposure after KMS access is revoked.
3. Never write unwrapped DEKs to disk, logs, or swap (see secure memory skill).

## Rules

- KEK only wraps keys; never encrypt data directly with it.
- KEK strength >= DEK strength.
- Bind context when wrapping: KMS encryption context or AEAD AAD containing
  key id and purpose, so a wrapped key cannot be swapped into another slot.
- Separate storage: the wrapped keyring can sit next to the data (it is
  useless without the KEK), but access to the KEK should be a different
  permission than access to the data store.

## KEK rotation

Rotate the KEK by unwrapping each DEK with the old KEK and rewrapping under
the new one - cheap, no data re-encryption. With AWS KMS automatic rotation,
the key ARN stays the same and old backing keys still decrypt, so no rewrap is
needed (gated: unconfirmed, source is paywalled or blocked); with a manual new key, run a rewrap job and keep the old KEK
decrypt-only until the job finishes.

## Bootstrapping the root

Something must authenticate to the KMS: a workload identity (IAM role, GCP
service account, Kubernetes service account federation) rather than a static
credential in a file. For on-prem HSMs, the HSM partition credential belongs
in a TPM-sealed store or an operator-entered quorum at boot.

## Verify

- [ ] No plaintext DEK in any database, file or backup (search for raw key lengths in dumps).
- [ ] Revoking the app's KMS permission stops new unwraps (after cache TTL).
- [ ] Keyring entries carry kek_ref and status; rewrap job tested.
