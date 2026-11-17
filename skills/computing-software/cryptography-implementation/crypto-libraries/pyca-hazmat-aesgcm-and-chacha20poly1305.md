---
id: computing-software.cryptography-implementation.crypto-libraries.pyca-hazmat-aesgcm-and-chacha20poly1305
name: pyca-hazmat-aesgcm-and-chacha20poly1305
category: computing-software
field: cryptography-implementation
product: crypto-libraries
tags: [cryptography-implementation, crypto-libraries, python, pyca-cryptography, pyca-aead, aes-gcm, chacha20poly1305, aead]
level: practitioner
status: verified
description: "Use pyca hazmat AESGCM, ChaCha20Poly1305 and AESGCMSIV correctly: nonce handling, AAD binding, the appended tag, InvalidTag and interop byte layout."
sources: ["https://cryptography.io/en/latest/hazmat/primitives/aead/", "https://cryptography.io/en/latest/exceptions/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# hazmat AEAD: AESGCM and ChaCha20Poly1305 (pyca/cryptography)

## Encrypt and decrypt
```python
import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
from cryptography.exceptions import InvalidTag

key = AESGCM.generate_key(bit_length=256)
aead = AESGCM(key)

def seal(pt: bytes, aad: bytes) -> bytes:
    nonce = os.urandom(12)
    return nonce + aead.encrypt(nonce, pt, aad)      # ct already ends with the 16-byte tag

def open_(blob: bytes, aad: bytes) -> bytes:
    if len(blob) < 12 + 16:
        raise ValueError("decrypt failed")
    try:
        return aead.decrypt(blob[:12], blob[12:], aad)
    except InvalidTag:
        raise ValueError("decrypt failed") from None   # one generic error to callers
```
- `encrypt()` returns `ciphertext || tag` (16-byte tag appended, per the pyca docs). Web Crypto produces the same shape (checked in Node: output length is plaintext + 16) and Go's `AEAD.Seal` appends its result the same way; libraries that return the tag in a separate buffer need the two joined.
- `aad` may be `None`; pass something meaningful (record id, column name, key version) so a
  ciphertext cannot be moved to another row.
- `ChaCha20Poly1305(key32)` has the identical API; 12-byte nonce.

## Nonces
- 12 random bytes per message; NIST SP 800-38D limits random-IV use to at most 2^32 invocations per key. `AESGCM` also accepts other nonce lengths (an 8-byte nonce worked), but use 12.
- Counter nonces are fine if the counter is persisted and never reused across processes.
- Need huge volumes with random nonces: `AESGCMSIV` (nonce-misuse resistant, 42.0+ and OpenSSL 3.2+ per the changelog) or XChaCha20 via libsodium. pyca has no XChaCha20 AEAD.

## Other classes
- `AESCCM(key, tag_length=16)` (valid tag lengths 4, 6, 8, 10, 12, 14, 16) for constrained-device interop; `AESOCB3`; `AESSIV` for
  deterministic encryption (key-wrap style uses). All of these ran on 50.0.2.
- Tag length is fixed at 16 for AESGCM encrypt; do not truncate tags for interop shortcuts.

## Pitfalls
- Reusing a nonce with GCM leaks the XOR of plaintexts and the authentication key.
- Do not catch `InvalidTag` and return partial data; there is none - decrypt is all-or-nothing.
- Data or AAD above 2^31-1 bytes raises `OverflowError` (pyca docs); chunk with a streaming construction instead.
- The `hazmat` name means you own nonce and key management; prefer `Fernet` when its limits fit.

## Verify
- [ ] Bit flips in nonce, ciphertext, tag and AAD all raise `InvalidTag` (checked; so do empty and 5-byte inputs).
- [ ] A test vector produced by the other language's implementation decrypts here.
- [ ] Nonce source is `os.urandom`/`secrets`, never `random`.
