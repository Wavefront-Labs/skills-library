---
id: computing-software.cryptography-implementation.applied-cryptography.choosing-primitives-and-modes
name: choosing-primitives-and-modes
category: computing-software
field: cryptography-implementation
product: applied-cryptography
tags: [cryptography-implementation, applied-cryptography, chacha20-poly1305, aes-gcm-siv, hkdf, argon2id, scrypt, bcrypt, pbkdf2, nonce-reuse, algorithm-selection]
level: practitioner
status: docs-checked
description: "Pick password hashing and parameters per OWASP, plus ChaCha20-Poly1305 and AES-GCM-SIV nonce rules and HKDF salt and info from the RFCs."
sources: ["https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html", "https://www.rfc-editor.org/rfc/rfc8439.txt", "https://www.rfc-editor.org/rfc/rfc5869.txt", "https://www.rfc-editor.org/rfc/rfc8452.txt"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Choosing cryptographic primitives and modes

**Goal:** pick one well-supported option per job, with parameters, so nobody designs a mode at review time. Prefer
high-level libraries (libsodium, Tink, the platform AEAD) that make these choices for you. See
`computing-software.cryptography-implementation.libsodium.authenticated-encryption-and-signatures`.

## 1. Password hashing (OWASP Password Storage Cheat Sheet)
Order of preference: Argon2id; scrypt when Argon2id is not available; bcrypt only for legacy systems; PBKDF2 when FIPS-140
validated implementations are required.

| Function | Minimum configurations |
|---|---|
| Argon2id | m=47104 (46 MiB), t=1, p=1; m=19456 (19 MiB), t=2, p=1; m=12288 (12 MiB), t=3, p=1; m=9216 (9 MiB), t=4, p=1; m=7168 (7 MiB), t=5, p=1 |
| scrypt | N=2^17 (128 MiB), r=8, p=1; N=2^16, r=8, p=2; N=2^15, r=8, p=3; N=2^14, r=8, p=5; N=2^13, r=8, p=10 |
| bcrypt | work factor as large as the server allows, minimum 10; most implementations accept at most 72 bytes of password, so enforce that maximum |
| PBKDF2 | HMAC-SHA256 600,000 iterations; HMAC-SHA512 220,000; HMAC-SHA1 1,400,000 (legacy only, not for new systems) |

- The Argon2id configurations give an equal level of defence and trade CPU for RAM. Benchmark on the target system; raising
  parallelism does not guarantee slower guessing.
- Do not use the two largest Argon2id settings with Argon2i.
- Pre-hashing before bcrypt is dangerous (null bytes in the hash output, password shucking). If it must be done, OWASP
  gives `bcrypt(base64(hmac-sha384(data:$password, key:$pepper)), $salt, $cost)` with the pepper stored outside the database.

## 2. Nonce rules
- **ChaCha20-Poly1305 (RFC 8439):** a 96-bit nonce that must not be repeated for the same key.
- **AES-GCM-SIV (RFC 8452):** a nonce-misuse-resistant AEAD: encrypting two messages under the same nonce does not fail
  catastrophically as in ordinary AEADs. Its RFC says this suits cases where nonce uniqueness cannot be guaranteed.

## 3. HKDF (RFC 5869)
The salt is optional and is a non-secret random value; the optional info string carries context and application-specific
information. Use a distinct info value per derived key.

## Checked
Date: 2026-11-09. Read: the OWASP Password Storage Cheat Sheet and the RFC 8439, 5869 and 8452 texts. Removed as not
confirmed: the whole algorithm decision table for AES-GCM, hashes, MACs, signatures, key exchange and HPKE, the GCM
2^32 and 64 GiB limits (the NIST SP 800-38D page gives only an abstract), the XChaCha20 notes, the composition rules,
the key-size advice, the post-quantum section, the gotchas, and the RFC 9106, 8032, 7748 and FIPS 203/204 sources.
Method: docs-checked 2026-11-09 against the OWASP Password Storage Cheat Sheet and RFC 8439, RFC 5869 and RFC 8452.
