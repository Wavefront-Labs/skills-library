---
id: computing-software.cryptography-implementation.applied-cryptography.chacha20-poly1305-construction-and-usage
name: chacha20-poly1305-construction-and-usage
category: computing-software
field: cryptography-implementation
product: applied-cryptography
tags: [applied-cryptography, cryptography-implementation, chacha20-poly1305-rfc8439, chacha20-poly1305, rfc-8439, aead, poly1305, chacha20, nonce, aes-gcm-alternative]
level: practitioner
status: docs-checked
description: "Use ChaCha20-Poly1305 (RFC 8439) correctly: key and nonce sizes, Poly1305 key derivation, AAD layout, limits, and when to prefer it over AES-GCM."
sources: ["https://www.rfc-editor.org/rfc/rfc8439", "https://www.rfc-editor.org/rfc/rfc7905", "https://datatracker.ietf.org/doc/draft-irtf-cfrg-xchacha/", "https://cryptography.io/en/latest/hazmat/primitives/aead/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ChaCha20-Poly1305 (RFC 8439)

## The construction (RFC 8439 2.8)
- 256-bit key, 96-bit nonce, 32-bit block counter. Block 0 of the keystream generates the one-time Poly1305 key;
  encryption starts at counter 1.
- Tag = Poly1305 over `AAD || pad16 || ciphertext || pad16 || len(AAD) as u64le || len(ciphertext) as u64le`.
- Output = ciphertext || 16-byte tag. Max plaintext per key and nonce is 274,877,906,880 bytes (2^32-1 blocks of 64 bytes, nearly 256 GB).

## When to choose it
- No AES hardware (older ARM, embedded, some mobile): constant-time and fast in software.
- When you want a 192-bit nonce so stateless writers can use random nonces: XChaCha20-Poly1305 (HChaCha20 turns
  the key and part of the nonce into a subkey). It is only an expired Internet-Draft (draft-irtf-cfrg-xchacha-03),
  so check your library's documentation for its exact construction.
- With AES-NI/ARMv8 crypto, AES-GCM is usually faster; both are fine security-wise.

## Using it
```python
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305
import os
key = ChaCha20Poly1305.generate_key()
aead = ChaCha20Poly1305(key)
nonce = os.urandom(12)          # never reuse a nonce with a key; prefer a counter if you can keep state
ct = aead.encrypt(nonce, b"payload", b"header-v1")
pt = aead.decrypt(nonce, ct, b"header-v1")   # raises InvalidTag on any change
```
The Python `cryptography` docs define `ChaCha20Poly1305` per the RFC, with a 12-byte nonce, and warn never to reuse a
nonce with a key; a wrong key, nonce, AAD or changed ciphertext raises `InvalidTag`.

## Gotchas
- The nonce must be unique per invocation with the same key; RFC 8439 2.6 says it MUST NOT be randomly generated
  for Poly1305 key generation and suggests a counter. If writers are stateless and must use random nonces, use
  a 192-bit-nonce variant.
- Poly1305 keys are one-time: never reuse the key, and do not use bare Poly1305 with a long-term key.

## Verify
- [ ] Round-trip and tamper tests using the RFC 8439 test vectors (Appendix A.5 is the AEAD decryption vector) pass.
- [ ] Nonce size matches the variant (12 bytes for RFC 8439).
- [ ] Decryption failures are counted.

## Checked
Date: 2026-10-31. Confirmed in RFC 8439 (2.8): 256-bit key, 96-bit nonce, Poly1305 key from block counter 0,
encryption from counter 1, the padded AAD and ciphertext plus 64-bit little-endian lengths, 128-bit tag, the
274,877,906,880-byte plaintext maximum, the 2.6 nonce rule and Appendix A.5; cryptography.io for the 12-byte nonce and
InvalidTag. Removed: Go and libsodium API claims, the 2^36 forgery limit, the GCM budget comparison, the early-TLS
draft note and the XChaCha 128-bit nonce split (the draft page is an abstract only).
Method: documentation only; no commands were run.
