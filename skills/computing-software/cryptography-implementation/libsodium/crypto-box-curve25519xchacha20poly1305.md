---
id: computing-software.cryptography-implementation.libsodium.crypto-box-curve25519xchacha20poly1305
name: crypto-box-curve25519xchacha20poly1305
category: computing-software
field: cryptography-implementation
product: libsodium
tags: [cryptography-implementation, curve25519xchacha20poly1305, crypto-box, xchacha20, libsodium, public-key-encryption]
level: advanced
status: verified
description: "Use crypto_box_curve25519xchacha20poly1305 for public-key authenticated encryption with 24-byte random nonces, plus beforenm, seal variant and interop notes."
sources: ["https://doc.libsodium.org/public-key_cryptography/authenticated_encryption", "https://github.com/jedisct1/libsodium/blob/master/src/libsodium/include/sodium/crypto_box_curve25519xchacha20poly1305.h", "https://github.com/jedisct1/libsodium/blob/master/src/libsodium/Makefile.am"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# crypto_box_curve25519xchacha20poly1305

Default `crypto_box` is X25519 + XSalsa20-Poly1305. The XChaCha20 variant uses HChaCha20 key derivation and
XChaCha20-Poly1305, matching other ChaCha-based stacks. It is not in the minimal build.

## API
```c
unsigned char pk[crypto_box_curve25519xchacha20poly1305_PUBLICKEYBYTES];
unsigned char sk[crypto_box_curve25519xchacha20poly1305_SECRETKEYBYTES];
crypto_box_curve25519xchacha20poly1305_keypair(pk, sk);

unsigned char n[crypto_box_curve25519xchacha20poly1305_NONCEBYTES];   /* 24 */
randombytes_buf(n, sizeof n);
crypto_box_curve25519xchacha20poly1305_easy(c, m, mlen, n, bob_pk, alice_sk);
if (crypto_box_curve25519xchacha20poly1305_open_easy(m, c, clen, n, alice_pk, bob_sk) != 0) { /* reject */ }
```
Also `_beforenm`/`_easy_afternm` for repeated messages between the same pair and
`crypto_box_curve25519xchacha20poly1305_seal` for anonymous senders.

## Notes
- Keys are ordinary X25519 keys, compatible with `crypto_box_keypair` keys (a `crypto_box_keypair` pair round-tripped through the XChaCha variant on libsodium.js 1.0.22).
- Ciphertext is not compatible with default `crypto_box` (the two ciphertexts differed for the same keys and nonce); both sides must pick the same variant.
- Not available when libsodium is built with `--enable-minimal`: `src/libsodium/Makefile.am` lists `box_curve25519xchacha20poly1305.c` and the seal file under `if !MINIMAL`. Check
  symbol presence or the binding's feature flags.
- Sender authentication is mutual (either party can forge messages "from" the other); sign if third-party
  proof is needed.

## Verify
- [ ] Interop round-trip with the peer binding using the same variant.
