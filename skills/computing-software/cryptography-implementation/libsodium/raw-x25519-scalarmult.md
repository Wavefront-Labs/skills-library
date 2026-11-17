---
id: computing-software.cryptography-implementation.libsodium.raw-x25519-scalarmult
name: raw-x25519-scalarmult
category: computing-software
field: cryptography-implementation
product: libsodium
tags: [cryptography-implementation, libsodium, libsodium-advanced, crypto-scalarmult, x25519, shared-secret-hashing, crypto-kx, low-order-points]
level: advanced
status: docs-checked
description: "Use crypto_scalarmult (raw X25519) only when you must: never use its output as a key, hash it with both public keys, check the -1 return, and prefer crypto_kx/crypto_box."
sources: ["https://doc.libsodium.org/advanced/scalar_multiplication", "https://doc.libsodium.org/key_exchange", "https://github.com/jedisct1/libsodium/blob/master/src/libsodium/crypto_scalarmult/curve25519/scalarmult_curve25519.c", "https://datatracker.ietf.org/doc/html/rfc7748"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Raw X25519 with crypto_scalarmult

`crypto_scalarmult(q, n, p)` computes the X25519 function: secret scalar `n`
times public point `p`. `crypto_scalarmult_base(q, n)` derives a public key.
libsodium files it under "Advanced" because the output is a raw group element,
not a key.

```c
unsigned char sk[crypto_scalarmult_SCALARBYTES], pk[crypto_scalarmult_BYTES];
randombytes_buf(sk, sizeof sk);
crypto_scalarmult_base(pk, sk);

unsigned char q[crypto_scalarmult_BYTES];
if (crypto_scalarmult(q, my_sk, peer_pk) != 0) {
    /* error: the source returns -1 when the output is all zeros; reject */
}
/* derive the shared key: H(q || client_pk || server_pk), per libsodium docs */
crypto_generichash_state h;
crypto_generichash_init(&h, NULL, 0, 32);
crypto_generichash_update(&h, q, sizeof q);
crypto_generichash_update(&h, client_pk, 32);
crypto_generichash_update(&h, server_pk, 32);
crypto_generichash_final(&h, shared_key, 32);
sodium_memzero(q, sizeof q);
```

## Rules

- `q` is the X coordinate of a point, so the number of possible values is limited to the group size (about 2^252); never use it
  directly as a symmetric key. The docs recommend `h(q || pk1 || pk2)` with both public keys, which also lets each party prove which public key it meant to use (for a given public key, 11 other public keys giving the same shared secret can be computed).
- `crypto_scalarmult` returns -1 when the result is all zeros (a failing exchange); check it.
- Ed25519 and X25519 keys are not interchangeable (see conversion skill).

## Prefer the higher-level APIs

| You want | Use |
|---|---|
| Client/server session keys | `crypto_kx_client_session_keys` / `crypto_kx_server_session_keys` (does the hashing and gives rx/tx keys) |
| Authenticated encryption to a public key | `crypto_box_easy` |
| Anonymous encryption to a public key | `crypto_box_seal` |

The libsodium docs say that on current versions you generally want `crypto_kx` for key exchange instead. Raw scalarmult is for implementing a documented protocol where the spec defines the KDF.

## Verify

- [ ] Return value of `crypto_scalarmult` checked.
- [ ] Shared secret passes through generichash/HKDF with both public keys.
- [ ] RFC 7748 Diffie-Hellman test vectors reproduce (both sides compute the same shared value).

## Checked

2026-10-26, libsodium documentation (libsodium-doc, master) and libsodium source at 1.0.22 era master. Confirmed: scalarmult and scalarmult_base signatures and size constants, the h(q || pk1 || pk2) recipe and its rationale, the return -1 on all-zero output (source), and crypto_kx as the preferred API (docs); the kx key derivation (BLAKE2B-512 split into rx and tx). Removed unconfirmed protocol recommendations (Noise, HPKE, X3DH).

Method: documentation only; no commands were run.
