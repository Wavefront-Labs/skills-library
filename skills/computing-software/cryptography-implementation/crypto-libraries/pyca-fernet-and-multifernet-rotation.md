---
id: computing-software.cryptography-implementation.crypto-libraries.pyca-fernet-and-multifernet-rotation
name: pyca-fernet-and-multifernet-rotation
category: computing-software
field: cryptography-implementation
product: crypto-libraries
tags: [cryptography-implementation, crypto-libraries, python, pyca-cryptography, fernet, multifernet, key-rotation, token-ttl]
level: practitioner
status: verified
description: "Encrypt with pyca Fernet, rotate keys with MultiFernet.rotate, enforce TTLs, and know Fernet's limits: no AAD, whole-message in memory, base64 overhead."
sources: ["https://cryptography.io/en/latest/fernet/", "https://github.com/fernet/spec/blob/master/Spec.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Fernet and MultiFernet rotation (pyca/cryptography)

Fernet is the misuse-resistant recipe layer: AES-128-CBC + HMAC-SHA256 (encrypt-then-MAC),
random IV, a timestamp, url-safe base64 output. Use it when you want "encrypt a small blob"
without choosing modes.

## Basic use
```python
from cryptography.fernet import Fernet, InvalidToken

key = Fernet.generate_key()          # 32 random bytes, url-safe base64 (44 chars)
f = Fernet(key)                      # 16 bytes signing key || 16 bytes encryption key
token = f.encrypt(b"card=4111...")   # bytes, url-safe base64
try:
    pt = f.decrypt(token, ttl=3600)  # reject tokens older than 1 hour
except InvalidToken:
    ...                              # bad key, tampered, or expired: one error for all
```
- `ttl` is checked against the embedded timestamp; it also rejects tokens more than 60 seconds
  in the future (clock skew; tested: 60 s ahead passes, 61 s fails). Omit `ttl` for data at rest.
- `f.extract_timestamp(token)` verifies the HMAC, then returns the issue time (a wrong key raises `InvalidToken`).
- Store the key in a secret manager or KMS-wrapped; a Fernet key in source code is the usual finding.

## Rotation with MultiFernet
```python
from cryptography.fernet import MultiFernet
new, old = Fernet(NEW_KEY), Fernet(OLD_KEY)
mf = MultiFernet([new, old])         # encrypts with the FIRST key, decrypts with any
token = mf.encrypt(b"...")
rotated = mf.rotate(old_token)       # decrypt with any key, re-encrypt under first key,
                                     # keeps the ORIGINAL timestamp
```
Rotation procedure:
1. Deploy `[new, old]` everywhere (readers first).
2. Background job: `rotate()` every stored token; write back.
3. When no token decrypts only under `old` (check by trying `Fernet(old)` alone on a sample or
   counting), drop `old` from the list.

## Limits that push you to something else
- No associated data: bind context by putting it inside the plaintext, or use `AESGCM` with AAD.
- The whole message is held in memory; for files use streaming AEAD (Tink, libsodium secretstream, age).
- AES-128 only; fine for confidentiality, but policies demanding AES-256 need `AESGCM`.
- Overhead: 57 bytes (1 version, 8 timestamp, 16 IV, 32 HMAC) plus PKCS7 padding (always 1-16 bytes, so an empty plaintext gives a 73-byte raw token), all then
  base64-encoded (x4/3).
- The timestamp is in clear: it reveals when data was encrypted.

## Verify
- [ ] Tampered token, wrong key and expired token each raise `InvalidToken`.
- [ ] Rotation job re-encrypts and old key removal is gated on a zero-remaining count.
- [ ] Keys are loaded from a secret store, never committed.
