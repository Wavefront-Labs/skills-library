---
id: computing-software.cryptography-implementation.key-management.one-key-one-purpose-enforcement
name: one-key-one-purpose-enforcement
category: computing-software
field: cryptography-implementation
product: key-management
tags: [cryptography-implementation, key-management, key-types-and-cryptoperiods, key-usage-separation, key-usage, extended-key-usage, kms-key-usage, pkcs11-attributes, jwk]
level: practitioner
status: draft
description: "Enforce one key, one purpose: why dual-use keys break, and how to pin usage with X.509 keyUsage, KMS KeyUsage, PKCS#11 flags, JWK key_ops and WebCrypto."
sources: ["https://csrc.nist.gov/pubs/sp/800/57/pt1/r5/final", "https://www.rfc-editor.org/rfc/rfc5280#section-4.2.1.3", "https://docs.aws.amazon.com/kms/latest/developerguide/create-keys.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# One key, one purpose enforcement

SP 800-57 5.2: a key should be used for one cryptographic purpose
(encryption, signing, MAC, key wrapping, key derivation). Dual use creates
cross-protocol attacks:

- RSA key used for both PKCS#1 v1.5 decryption and signing: a Bleichenbacher
  decryption oracle becomes a signature forgery oracle.
- Same AES key for CBC encryption and CBC-MAC: forgeries.
- TLS server key reused for code signing or for SSH: compromise of one
  system is compromise of all.
- One HMAC key for session tokens and password-reset tokens: tokens
  interchangeable.

## Enforce it where keys live

| Place | Mechanism |
|---|---|
| X.509 | `keyUsage` (critical) and `extendedKeyUsage`; e.g. `digitalSignature` + `serverAuth` only |
| AWS KMS | `KeyUsage` fixed at creation: `ENCRYPT_DECRYPT`, `SIGN_VERIFY`, `GENERATE_VERIFY_MAC`, `KEY_AGREEMENT` |
| GCP KMS | key `purpose`: `ENCRYPT_DECRYPT`, `ASYMMETRIC_SIGN`, `ASYMMETRIC_DECRYPT`, `MAC` |
| PKCS#11 | set only the needed flags: `CKA_SIGN` or `CKA_DECRYPT`, not both; `CKA_WRAP` only on KEKs |
| JWK | `use` (`sig`/`enc`) and `key_ops`; reject keys whose `use` does not match |
| WebCrypto | `keyUsages` array at import/generate |
| Tink | key templates bind a key to one primitive |

## In application code

- Derive separate subkeys per purpose (HKDF with distinct `info`) instead of
  reusing one secret.
- Name keys by purpose in config (`TOKEN_MAC_KEY`, `FIELD_ENC_KEY`), never a
  generic `SECRET_KEY` used everywhere.
- Validate `keyUsage`/`use` on keys received from others before using them.

## Verify

- [ ] Inventory shows one purpose per key id.
- [ ] Test: KMS sign call on an ENCRYPT_DECRYPT key fails; PKCS#11 decrypt with a sign-only key fails.
- [ ] Certificates carry keyUsage/EKU matching their role.
