---
id: computing-software.cryptography-implementation.openssl.raw-key-and-iv-with-openssl-enc
name: raw-key-and-iv-with-openssl-enc
category: computing-software
field: cryptography-implementation
product: openssl
tags: [openssl, cryptography-implementation, enc-raw-key-iv, openssl-enc, aes-cbc, aes-ctr, interop, pkcs7-padding, hex-key, cross-language]
level: practitioner
status: verified
description: "Use openssl enc with raw -K and -iv hex for interop with Java, Python and Node: padding defaults, short-key zero padding warning, CTR mode and no GCM support."
sources: ["https://docs.openssl.org/3.0/man1/openssl-enc/", "https://csrc.nist.gov/pubs/sp/800/38/a/final", "https://cryptography.io/en/latest/hazmat/primitives/symmetric-encryption/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Raw key and IV with openssl enc

When matching another library byte for byte, bypass the password KDF and pass the key and IV directly.

## Commands
```
KEY=$(openssl rand -hex 32); IV=$(openssl rand -hex 16)
openssl enc -aes-256-cbc -K $KEY -iv $IV -in plain.bin -out ct.bin       # PKCS#7 padding, no Salted__ header
openssl enc -d -aes-256-cbc -K $KEY -iv $IV -in ct.bin -out out.bin
openssl enc -aes-256-ctr -K $KEY -iv $IV -in plain.bin -out ct.bin       # IV is the initial 128-bit counter block
openssl enc -aes-256-cbc -nopad -K $KEY -iv $IV ...                       # input must be a multiple of 16 bytes
```

## Equivalents elsewhere
| Library | Matching call |
|---|---|
| Python pyca | `Cipher(algorithms.AES(key), modes.CBC(iv))` + `padding.PKCS7(128)` (output matched byte for byte; cryptography 49.0.0) |
| Node | `crypto.createCipheriv('aes-256-cbc', key, iv)` (auto padding on; output matched byte for byte) |

## Gotchas
- **Short keys are zero-padded with only a warning** ("hex string is too short, padding with zero bytes to length");
  long keys are truncated ("hex string is too long, ignoring excess"); both confirmed on OpenSSL 3.2.3. A 31-byte key silently becomes a weak key.
  Check length before calling.
- `enc` rejects AEAD modes (`AEAD ciphers not supported`); for AES-GCM interop use a short script in the target
  language or `openssl` library APIs, not `enc`.
- CTR in OpenSSL treats the whole 16-byte IV as a big-endian counter (tested: it matched pyca `modes.CTR` and Node `aes-256-ctr`, including a carry across all 128 bits); libraries that use 12-byte nonce plus 4-byte
  counter starting at 0 or 1 differ unless you build the IV the same way.
- Raw `-K` usage leaves no integrity protection; add an HMAC (see the enc integrity skill) or use a real AEAD tool.

## Verify
- [ ] Ciphertext from OpenSSL decrypts in the other library and vice versa.
- [ ] Key length is checked to be exactly 64 hex characters for AES-256.
