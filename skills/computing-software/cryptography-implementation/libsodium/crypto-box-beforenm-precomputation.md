---
id: computing-software.cryptography-implementation.libsodium.crypto-box-beforenm-precomputation
name: crypto-box-beforenm-precomputation
category: computing-software
field: cryptography-implementation
product: libsodium
tags: [cryptography-implementation, libsodium, crypto-box, box-beforenm, crypto-box-easy-afternm, shared-key-precomputation, performance, key-hygiene]
level: advanced
status: verified
description: "Speed up repeated crypto_box traffic between the same key pair with crypto_box_beforenm and the _afternm functions, and protect the precomputed shared key like a secret key."
sources: ["https://doc.libsodium.org/public-key_cryptography/authenticated_encryption#precalculation-interface"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# crypto_box_beforenm precomputation

Every `crypto_box_easy` call does an X25519 scalar multiplication (tens of
microseconds: about 57 us per `crypto_box_beforenm` call through PyNaCl on the review host). When the same two parties exchange many messages, compute the
shared key once:

```c
unsigned char k[crypto_box_BEFORENMBYTES];          /* 32 */
if (crypto_box_beforenm(k, peer_pk, my_sk) != 0) { /* peer_pk is a low-order point: reject (an all-zero key was rejected in libsodium.js) */ }
crypto_box_easy_afternm(c, m, mlen, nonce, k);
if (crypto_box_open_easy_afternm(m, c, clen, nonce, k) != 0) { /* reject */ }
/* detached variants: crypto_box_detached_afternm / crypto_box_open_detached_afternm */
sodium_memzero(k, sizeof k);                         /* when the peer session ends */
```

Results are byte-identical to `crypto_box_easy` with the same keys and nonce
(checked on libsodium.js 1.0.22), so the peer does not need to use precomputation.

## Rules

- `k` is equivalent to both parties' secret keys for this pair: anyone with
  it can read and forge all messages between them. Keep it in protected
  memory (`sodium_malloc`), never log or persist it unencrypted.
- Check the return value of `crypto_box_beforenm` (fails for degenerate peer keys).
- Nonce uniqueness still applies per pair; random 24-byte nonces remain fine.
- Cache keyed by peer public key with an eviction policy and zeroisation on
  eviction for servers talking to many clients.

## When it matters

High message rates between fixed pairs (server-to-device telemetry, peer
links). For a handful of messages, the plain API is simpler. If you are
building sessions anyway, `crypto_kx` session keys + AEAD give per-direction
keys and are the more structured choice.

## Verify

- [ ] Outputs from `_afternm` decrypt with plain `crypto_box_open_easy` on the peer.
- [ ] Precomputed keys stored in guarded memory and wiped on session end.
- [ ] `crypto_box_beforenm` return value checked.
