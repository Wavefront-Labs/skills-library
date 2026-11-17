---
id: computing-software.cryptography-implementation.libsodium.crypto-kx-with-secretstream-sessions
name: crypto-kx-with-secretstream-sessions
category: computing-software
field: cryptography-implementation
product: libsodium
tags: [cryptography-implementation, kx-secretstream-session, crypto-kx, secretstream, libsodium, session-keys, forward-secrecy, secure-channel]
level: advanced
status: verified
description: "Build a two-way encrypted session from crypto_kx session keys and two secretstream states, exchange headers, and add forward secrecy with ephemeral authenticated keys."
sources: ["https://doc.libsodium.org/key_exchange", "https://doc.libsodium.org/secret-key_cryptography/secretstream", "https://doc.libsodium.org/public-key_cryptography/public-key_signatures"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# crypto_kx with secretstream sessions

## Key exchange
```c
/* client */
crypto_kx_client_session_keys(rx, tx, client_pk, client_sk, server_pk);
/* server */
crypto_kx_server_session_keys(rx, tx, server_pk, server_sk, client_pk);
```
Client `tx` equals server `rx` and vice versa. Keys are BLAKE2b-512(q || client_pk || server_pk) split in two: the first 32 bytes are the client's `rx`, the last 32 its `tx` (reproduced with `crypto_scalarmult` and `crypto_generichash(64)` on libsodium.js 1.0.22). `crypto_kx_*_session_keys` returns -1 for an unacceptable peer key (an all-zero key was rejected).

## Two streams, one per direction
```c
/* client sends */
crypto_secretstream_xchacha20poly1305_init_push(&out_st, out_header, tx);   /* send out_header */
/* client receives (after server sends its header) */
crypto_secretstream_xchacha20poly1305_init_pull(&in_st, in_header, rx);
```
Each direction has its own key and header, so there is no nonce coordination. Mark message boundaries with
`TAG_PUSH`, close with `TAG_FINAL`, and treat a missing FINAL on disconnect as truncation if it matters.

## Forward secrecy and authentication
`crypto_kx` with long-term keys gives no forward secrecy: a later leak of either secret key decrypts recorded
sessions. For forward secrecy:
1. Each side generates an ephemeral kx keypair per session.
2. Each side signs its ephemeral public key (plus a transcript: both ephemeral keys and identities) with its
   long-term Ed25519 key (`crypto_sign_detached`) and verifies the peer's.
3. Derive session keys from the ephemeral pair; erase ephemeral secrets after.

If you need this, a Noise pattern (XX, IK) implementation is usually a better choice than hand-assembly.

## Verify
- [ ] Messages flow both ways; tampering or reordering fails `pull` (checked: a client `tx` stream pulled with the server `rx` key, and pulling the second chunk first failed).
- [ ] Ephemeral secret keys are zeroised after deriving session keys (`sodium_memzero`).
- [ ] Signature over the ephemeral keys is verified before use.
