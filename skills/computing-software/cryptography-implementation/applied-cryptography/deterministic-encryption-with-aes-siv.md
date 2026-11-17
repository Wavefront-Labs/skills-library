---
id: computing-software.cryptography-implementation.applied-cryptography.deterministic-encryption-with-aes-siv
name: deterministic-encryption-with-aes-siv
category: computing-software
field: cryptography-implementation
product: applied-cryptography
tags: [cryptography-implementation, applied-cryptography, storage-encryption-modes, aes-siv-deterministic, aes-siv, rfc5297, deterministic-encryption, daead, tink, equality-search]
level: advanced
status: docs-checked
description: "Use AES-SIV (RFC 5297) for deterministic authenticated encryption: equality lookups on encrypted columns, key size gotcha (512-bit for AES-256), AAD vectors, and leakage."
sources: ["https://datatracker.ietf.org/doc/html/rfc5297", "https://developers.google.com/tink/deterministic-aead", "https://cryptography.io/en/latest/hazmat/primitives/aead/#cryptography.hazmat.primitives.ciphers.aead.AESSIV"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Deterministic encryption with AES-SIV

AES-SIV computes a synthetic IV as a CMAC-based PRF over the associated data
and plaintext, then encrypts with CTR using that value. Same key + same AD +
same plaintext gives the same ciphertext; anything else gives an unrelated
ciphertext. It is a deterministic AEAD (DAEAD), and with a random nonce added
as an AD component it is also a nonce-misuse-resistant AEAD.

## When it is the right tool

- Encrypted column that must support `WHERE col = ?` and unique indexes.
- Deduplication of encrypted blobs within one tenant.

When equality search is the only need and you never decrypt from the index,
an HMAC blind index next to a randomized AEAD ciphertext leaks the same
equality but keeps the stored ciphertext randomized.

## Gotchas

- **Key size is doubled**: AES-SIV uses two AES keys (CMAC + CTR). "AES-SIV-256"
  in RFC 5297 terms is a 64-byte key giving AES-256 security: RFC 5297 keys are 256, 384 or 512 bits
  and are split in half, so pyca needs `AESSIV.generate_key(512)` for AES-256. Tink recommends its `AES256_SIV`
  key type for deterministic AEAD.
- **AD is a vector**, not one string: RFC 5297 allows no more than 126 AD
  components, and pyca takes a list. Keep the same structure on both sides.
- In pyca the final element of the AD list is treated as a nonce for nonce-based use; with no nonce,
  encryption is deterministic, and the same inputs always give the same ciphertext either way.
- Ciphertext = 128-bit synthetic IV || ciphertext of the plaintext's length (RFC 5297 2.6), so it is 16 bytes
  longer than the plaintext. No separate nonce field.
- AES-SIV is not AES-GCM-SIV: pyca documents them as separate classes (`AESSIV`, `AESGCMSIV`). Pick AES-SIV
  (RFC 5297, Tink `DeterministicAead`) for deterministic use.

```python
from cryptography.hazmat.primitives.ciphers.aead import AESSIV
k = AESSIV.generate_key(512)
s = AESSIV(k)
ct = s.encrypt(b"alice@example.com", [b"users.email", b"tenant-42"])
assert s.encrypt(b"alice@example.com", [b"users.email", b"tenant-42"]) == ct
```

## Leakage and mitigation

Equal values are linkable: frequency analysis on low-cardinality columns
recovers values. Put tenant and column name in AD so equality only leaks within
a column of one tenant. Never use deterministic encryption on enums, booleans,
dates of birth or other small domains.

## Verify

- [ ] Key is 64 bytes for AES-256-level SIV.
- [ ] RFC 5297 Appendix A vectors (A.1 deterministic, A.2 nonce-based) pass.
- [ ] AD includes column and tenant; cross-column equality does not match.
- [ ] Column cardinality reviewed; low-entropy fields excluded.

## Checked
Date: 2026-10-31. Confirmed in RFC 5297 (keys of 256, 384 or 512 bits, at most 126 AD components, 128-bit SIV plus
equal-length ciphertext, Appendix A.1 and A.2), the pyca `AESSIV` documentation (256, 384, 512-bit keys, AD list, final
element as nonce, deterministic without one) and Tink's deterministic AEAD page (AES256_SIV recommended). Removed:
the key-wrapping use, the Tink 64-byte key figure, the pyca versus Tink AD comparison and the GCM-SIV speed claim.
The pyca snippet was not run (the package is not installed here).
Method: documentation only; no commands were run.
