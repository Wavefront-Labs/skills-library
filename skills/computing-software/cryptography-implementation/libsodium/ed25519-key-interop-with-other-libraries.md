---
id: computing-software.cryptography-implementation.libsodium.ed25519-key-interop-with-other-libraries
name: ed25519-key-interop-with-other-libraries
category: computing-software
field: cryptography-implementation
product: libsodium
tags: [cryptography-implementation, ed25519-interop, ed25519, libsodium, pkcs8, key-conversion, openssl]
level: practitioner
status: docs-checked
description: "Move Ed25519 keys between libsodium and Go: 64-byte seed-plus-public secret keys, 32-byte seeds, RFC 8410 PKCS#8 and SPKI prefixes, and signature-format checks."
sources: ["https://doc.libsodium.org/public-key_cryptography/public-key_signatures", "https://www.rfc-editor.org/rfc/rfc8410", "https://github.com/golang/go/blob/master/src/crypto/ed25519/ed25519.go"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Ed25519 key interop

## Representations
| Library | Private key format |
|---|---|
| libsodium `crypto_sign_SECRETKEYBYTES` | 64 bytes = seed (32 bytes) followed by public key (32 bytes) |
| Go `ed25519.PrivateKey` | same 64-byte layout; `NewKeyFromSeed(seed)` |
| OpenSSL / RFC 8410 PKCS#8 | 32-byte seed in `CurvePrivateKey` OCTET STRING |

## Conversions
```c
unsigned char seed[32];
crypto_sign_ed25519_sk_to_seed(seed, sk64);          /* libsodium -> seed */
crypto_sign_seed_keypair(pk, sk64, seed);            /* seed -> libsodium */
```
- PKCS#8 DER for Ed25519 (RFC 8410, OID 1.3.101.112) is a fixed 16-byte prefix `302e020100300506032b657004220420` followed by the 32-byte seed (the RFC's example key encodes as `MC4CAQAwBQYDK2VwBCIEI...`).
- Public key DER (SPKI): prefix `302a300506032b6570032100` + 32-byte key.

## Pitfalls
- Feeding the 64-byte libsodium key where a 32-byte seed is expected (or vice versa).
- Using `crypto_sign` combined output (signature + message) where others expect a detached 64-byte signature.
- Ed25519ph (libsodium's multi-part `crypto_sign_init` API) is not equivalent to pure Ed25519 over a pre-hashed message, so signatures are not interchangeable.

## Verify
- [ ] Sign in one library, verify in the other, for the same seed; public keys match byte for byte.

## Checked

2026-10-26, libsodium documentation (libsodium-doc, master) and libsodium source at 1.0.22 era master. Confirmed: libsodium sk is seed plus public key with sk_to_seed and seed_keypair; Go PrivateKeySize is 64, SeedSize 32, NewKeyFromSeed and Seed() exist; RFC 8410 examples match the stated PKCS#8 and SPKI prefixes and CurvePrivateKey is an OCTET STRING holding 32 bytes. Removed the WebCrypto/JWK and OpenSSH rows and an openssl shell pipeline that no documentation covers.

Method: documentation only; no commands were run.
