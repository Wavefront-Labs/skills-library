---
id: computing-software.cryptography-implementation.applied-cryptography.choosing-a-kdf-by-input-entropy
name: choosing-a-kdf-by-input-entropy
category: computing-software
field: cryptography-implementation
product: applied-cryptography
tags: [applied-cryptography, cryptography-implementation, kdf-input-entropy, kdf, kdf-selection, hkdf, argon2id, pbkdf2, kbkdf, low-entropy-secrets, pake]
level: practitioner
status: docs-checked
description: "Pick the right KDF from the secret's entropy: HKDF or KBKDF for keys and DH outputs, Argon2id, scrypt or PBKDF2 for passwords."
sources: ["https://csrc.nist.gov/pubs/sp/800/56/c/r2/final", "https://www.rfc-editor.org/rfc/rfc5869#section-4", "https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Choosing a KDF by input entropy

The wrong KDF for the input is a common, quiet bug. RFC 5869 says the HKDF
extract step can concentrate existing entropy but cannot amplify it, and that
a slowing-down mechanism is not part of HKDF. A password run through HKDF has
no work factor; a password hash on an already random key adds nothing.

## Decision table
| Input secret | Use |
|---|---|
| Random key that is already a good pseudorandom key | HKDF-Expand (RFC 5869 notes the extract stage can be skipped when the input is already a good pseudorandom key) or an SP 800-108 PRF-based KDF |
| DH / ECDH shared secret | HKDF extract-then-expand, or an SP 800-56C one-step KDF |
| Password / passphrase | A password hash from the OWASP list: Argon2id, then scrypt, then (legacy) bcrypt; PBKDF2-HMAC-SHA256 when FIPS-140 compliance is required |
| Very short secret such as a PIN | A key-derivation function alone cannot fix a small guess space; add online rate limiting or a protocol designed for it (not covered by the sources checked here) |

## Why
- HKDF "naturally accommodates the use of salt" but has no slowing mechanism, so RFC 5869 points password users to PKCS #5 style functions instead.
- SP 800-56C describes two ways to derive keys from a shared secret: a one-step method and a two-step extraction-then-expansion procedure, the latter expanding with SP 800-108 functions.
- OWASP says to prefer Argon2id for new password storage, scrypt when Argon2id is unavailable, bcrypt only for legacy systems, and PBKDF2 where FIPS-140 is needed.

## Patterns
```python
# password -> master key (once), then cheap derivations
from argon2.low_level import hash_secret_raw, Type
mk = hash_secret_raw(password, salt, time_cost=2, memory_cost=19456, parallelism=1, hash_len=32, type=Type.ID)
from cryptography.hazmat.primitives.kdf.hkdf import HKDFExpand
from cryptography.hazmat.primitives import hashes
enc_key = HKDFExpand(hashes.SHA256(), 32, b"app.v1.enc").derive(mk)
mac_key = HKDFExpand(hashes.SHA256(), 32, b"app.v1.mac").derive(mk)
```
The Argon2id values match one of OWASP's minimum configurations (19 MiB, 2 passes, 1 lane); benchmark and raise them on your hardware.
Run the slow function once, then fan out with HKDF-Expand and distinct `info` labels.

## Gotchas
- OWASP minimums: PBKDF2-HMAC-SHA256 at 600,000 iterations; scrypt with a CPU/memory cost of 2^17, block size 8, parallelism 1; bcrypt work factor 10 or more with a 72-byte password limit.
- Salting HKDF does not make it a password hash.

## Verify
- [ ] Every KDF call site is labelled with its input type in review.
- [ ] No HKDF/PBKDF2-with-1-iteration over user passwords.
- [ ] Short secrets such as PINs are protected by rate limiting, not only by a KDF.

## Checked

Confirmed against RFC 5869 section 4 and the start of section 2 (extract can be skipped for good pseudorandom keys, entropy cannot be amplified, no slowing mechanism, PKCS #5 pointer), SP 800-56C Rev. 2 (one-step and two-step methods, SP 800-108 expansion) and the OWASP Password Storage Cheat Sheet (algorithm order, Argon2id minimum configurations, scrypt, bcrypt 72 bytes, PBKDF2 600,000). Removed: the entropy-in-bits column, GPU-speed and "fast by design" remarks, the OPAQUE/TPM/Secure Enclave PIN advice, the API-token SHA-256 row, the bcrypt-on-tokens gotcha and the 40-bit recovery code claim, none of which the sources state. Changed the example Argon2id parameters to an OWASP minimum.

Method: docs-checked 2026-11-09 against SP 800-56C Rev. 2 PDF, RFC 5869 text and the OWASP Password Storage Cheat Sheet.
