---
id: computing-software.cryptography-implementation.crypto-libraries.pyca-hazmat-kdfs
name: pyca-hazmat-kdfs
category: computing-software
field: cryptography-implementation
product: crypto-libraries
tags: [crypto-libraries, cryptography-implementation, pyca-kdf, python, pyca-cryptography, hkdf, pbkdf2, scrypt]
level: practitioner
status: verified
description: "Derive keys with pyca/cryptography hazmat KDFs: HKDF and HKDFExpand, PBKDF2HMAC, Scrypt, Argon2id, ConcatKDF and KBKDF; single-use objects and verify methods."
sources: ["https://cryptography.io/en/latest/hazmat/primitives/key-derivation-functions/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# pyca hazmat KDFs

## HKDF
```python
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF, HKDFExpand
key = HKDF(algorithm=hashes.SHA256(), length=32, salt=salt, info=b"myapp v1 enc").derive(ikm)
sub = HKDFExpand(algorithm=hashes.SHA256(), length=32, info=b"mac").derive(prk)   # PRK already uniform
```

## Password-based
```python
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.hazmat.primitives.kdf.argon2 import Argon2id     # cryptography 44.0+ (changelog); run on 50.0.2
k1 = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=600_000).derive(pw)
k2 = Scrypt(salt=salt, length=32, n=2**17, r=8, p=1).derive(pw)
k3 = Argon2id(salt=salt, length=32, iterations=3, lanes=4, memory_cost=64 * 1024).derive(pw)
```
Argon2id needs an OpenSSL 3.2+ backend (bundled wheels qualify).

## Others
- `ConcatKDFHash` / `ConcatKDFHMAC` (SP 800-56C one-step), `X963KDF` (ANSI X9.63 for ECIES interop).
- `KBKDFHMAC` / `KBKDFCMAC` (SP 800-108 counter mode) with `Mode.CounterMode`, `CounterLocation`, label, context.

## Rules
- KDF instances are single-use: calling `derive` twice, or `verify` after `derive`, raises `AlreadyFinalized`. Create a new object each time.
- `verify(key_material, expected_key)` on a fresh object raises `InvalidKey` on mismatch.
- Salts: random 16 bytes for password KDFs; HKDF salt optional but recommended.

## Verify
- [ ] RFC 5869 test case 1 (HKDF-SHA256) and the RFC 7914 scrypt empty-password vector reproduce (both checked on 50.0.2); `Scrypt(n=2**17, r=8, p=1)` ran without setting a memory limit.
