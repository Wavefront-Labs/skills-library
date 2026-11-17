---
id: computing-software.cryptography-implementation.libsodium.chacha20-poly1305-variants-in-libsodium
name: chacha20-poly1305-variants-in-libsodium
category: computing-software
field: cryptography-implementation
product: libsodium
tags: [cryptography-implementation, chacha20poly1305-ietf, crypto-aead-chacha20poly1305, xchacha20poly1305-ietf, libsodium, rfc-8439, aead, interop]
level: practitioner
status: verified
description: "Choose between libsodium's original, IETF and XChaCha20-Poly1305 AEADs: nonce and message limits, interop with RFC 8439 libraries, and migrating between them."
sources: ["https://doc.libsodium.org/secret-key_cryptography/aead/chacha20-poly1305", "https://www.rfc-editor.org/rfc/rfc8439", "https://datatracker.ietf.org/doc/draft-irtf-cfrg-xchacha/", "https://pkg.go.dev/golang.org/x/crypto/chacha20poly1305", "https://openjdk.org/jeps/329"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ChaCha20-Poly1305 variants in libsodium

| Variant | Functions | Nonce | Max per message | Interop |
|---|---|---|---|---|
| Original | `crypto_aead_chacha20poly1305_*` | 64-bit | `SIZE_MAX - 16` (64-bit counter, no practical limit) | Early TLS drafts, old NaCl-era code |
| IETF | `crypto_aead_chacha20poly1305_ietf_*` | 96-bit | `64 * (2^32 - 1)` bytes, about 256 GiB | RFC 8439; OpenSSL, BoringSSL, Go, Java 11+ (JEP 329), pyca |
| XChaCha20 | `crypto_aead_xchacha20poly1305_ietf_*` | 192-bit | `SIZE_MAX - 16`, no practical limit (libsodium docs: about 2^64 bytes) | XChaCha draft (not an RFC); Go `chacha20poly1305.NewX`; pyca has no XChaCha class |

All use 32-byte keys and 16-byte tags (`ABYTES`).

## Choosing
- New libsodium-to-libsodium data: XChaCha20-Poly1305 (random nonces always safe).
- Interop with RFC 8439 stacks: IETF variant with counter nonces.
- Never mix variants across sender and receiver: same key and nonce produce different ciphertext; decryption fails
  with a generic error.

## Interop example (IETF variant)
libsodium:
```c
crypto_aead_chacha20poly1305_ietf_encrypt(c, &clen, m, mlen, ad, adlen, NULL, nonce12, key);
```
Python pyca, same output (ciphertext || tag):
```python
ChaCha20Poly1305(key).encrypt(nonce12, m, ad)
```

## Migrating original -> XChaCha
Add a format version byte; decrypt old records with the original variant, re-encrypt with XChaCha and a random
24-byte nonce. Keep the decrypt-only path until all data has moved.

## Verify
- [ ] RFC 8439 A.5 vector decrypts with the IETF functions (done: PyNaCl 1.6.2 `crypto_aead_chacha20poly1305_ietf_decrypt` returned the 265-byte plaintext; the section 2.8.2 example gives the same output as pyca's `ChaCha20Poly1305`, tag `1ae10b594f09e26a7e902ecbd0600691`).
- age uses plain ChaCha20-Poly1305 (12-byte nonces) in its spec, not XChaCha, so it is not an XChaCha precedent.
- [ ] Records carry a version byte naming the variant.
