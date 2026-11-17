---
id: computing-software.cryptography-implementation.applied-cryptography.blake2-and-blake3-selection
name: blake2-and-blake3-selection
category: computing-software
field: cryptography-implementation
product: applied-cryptography
tags: [cryptography-implementation, applied-cryptography, hash-functions, blake2b, blake2s, blake3, keyed-hashing, b3sum, derive-key, personalization]
level: practitioner
status: verified
description: "Choose BLAKE2b, BLAKE2s or BLAKE3 and use their keyed, personalised and derive-key modes correctly; when FIPS rules them out."
sources: ["https://www.rfc-editor.org/rfc/rfc7693", "https://github.com/BLAKE3-team/BLAKE3-specs/blob/master/blake3.pdf", "https://docs.python.org/3/library/hashlib.html#blake2"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# BLAKE2 and BLAKE3 selection and keyed modes

## Which one

| Hash | Use when |
|---|---|
| BLAKE2b | 64-bit platforms, digests 1-64 bytes, libsodium `crypto_generichash` |
| BLAKE2s | 8-32-bit platforms (WireGuard uses BLAKE2s) |
| BLAKE3 | Large inputs, parallel/SIMD speed, file hashing, one function for hash/MAC/KDF |
| SHA-256/SHA-3 | FIPS 140 is required: NIST lists only SHA-2 and SHA-3 (FIPS 180-4, FIPS 202) as approved hashes, no BLAKE |

## BLAKE2 modes (RFC 7693)

```python
import hashlib
hashlib.blake2b(data, digest_size=32).digest()
hashlib.blake2b(data, key=k32, digest_size=32).digest()      # MAC, key <= 64 bytes
hashlib.blake2b(data, digest_size=32, person=b"myapp-v1-tok") # domain separation, <= 16 bytes
```

Keyed BLAKE2 is a secure MAC (no HMAC wrapper needed). `person` and `salt`
give domain separation without changing the key.

## BLAKE3 modes

```python
import blake3                                  # pip install blake3
blake3.blake3(data).digest()                   # 32 bytes, XOF via .digest(length=n)
blake3.blake3(data, key=k32).digest()          # keyed_hash, key exactly 32 bytes
blake3.blake3(ikm, derive_key_context="example.com 2026-10 session keys").digest()
```

`derive_key` context strings should be hardcoded, globally unique and never
contain variable data; variable data goes in the input material.

CLI: `b3sum file`; verify with `b3sum --check sums.txt` (b3sum 1.8.7 run);
`--keyed` reads the 32-byte key from stdin, `--derive-key <CONTEXT>` is the KDF mode.
Python limits (run): `blake2b` key over 64 bytes and `person` over 16 bytes raise
`ValueError`; `blake3` key not 32 bytes raises `ValueError`; empty-input BLAKE3
is `af1349b9...3262`, the published value.

## Pitfalls

- Different digest sizes in BLAKE2 are different functions (the size is a
  parameter), unlike SHA-512 truncation; peers must agree on size.
- Library defaults vary (BLAKE2b-512 vs BLAKE2b-256); state the size explicitly.
- Do not hash secrets with plain BLAKE3 as a "KDF"; use `derive_key`.

## Verify

- [ ] Official test vectors pass for the chosen variant and size.
- [ ] Keys for keyed modes are random and of the required length.
