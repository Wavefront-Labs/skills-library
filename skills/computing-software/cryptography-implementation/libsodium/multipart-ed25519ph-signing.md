---
id: computing-software.cryptography-implementation.libsodium.multipart-ed25519ph-signing
name: multipart-ed25519ph-signing
category: computing-software
field: cryptography-implementation
product: libsodium
tags: [cryptography-implementation, libsodium, crypto-sign, crypto-sign-init, ed25519ph, multipart-signing, streaming-signatures, large-files, rfc8032]
level: advanced
status: docs-checked
description: "Sign large or streamed data with libsodium crypto_sign_init/update/final_create (Ed25519ph): API, how it differs from plain Ed25519, and interop."
sources: ["https://doc.libsodium.org/public-key_cryptography/public-key_signatures", "https://github.com/jedisct1/libsodium/blob/master/src/libsodium/crypto_sign/ed25519/ref10/sign.c", "https://github.com/golang/go/blob/master/src/crypto/ed25519/ed25519.go", "https://github.com/jedisct1/libsodium.js"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Multi-part Ed25519ph signing

Plain Ed25519 reads the whole message twice during signing (once to derive the nonce and once for the challenge, as in libsodium's sign.c), so it cannot stream.
libsodium's multi-part API implements **Ed25519ph** (RFC 8032 pre-hash
variant): the message is hashed with SHA-512 incrementally, and the hash is
signed.

```c
crypto_sign_state st;
crypto_sign_init(&st);
while ((n = fread(buf, 1, sizeof buf, f)) > 0) crypto_sign_update(&st, buf, n);
crypto_sign_final_create(&st, sig, NULL, sk);

crypto_sign_init(&st);
/* ... crypto_sign_update over the same bytes ... */
if (crypto_sign_final_verify(&st, sig, pk) != 0) { /* reject */ }
```

The libsodium.js README says its API mirrors the C library, and the libsodium docs prefer the single-part API when the message fits in memory.

## Ed25519ph is a different signature scheme

- A signature from `crypto_sign_final_create` is not expected to verify with
  `crypto_sign_verify_detached` over the same message, and vice versa: the Ed25519ph hash input carries the dom2-style prefix above.
- Same key pair can technically produce both; keep one key per scheme to
  avoid confusion, and label the scheme in your format.
- Interop: other libraries call it Ed25519ph. Go selects it with `crypto.SHA512` as the signing option and expects the message to already be a SHA-512 digest.
  libsodium's source prefixes the hash input with `SigEd25519 no Ed25519 collisions`, the phflag byte 1 and an empty context (length 0).

## Alternative: sign a hash with plain Ed25519

Hash the stream with the multi-part `crypto_generichash_*` API (as the docs suggest) and sign the 512-bit output with
`crypto_sign_detached`, preferably prefixed by your protocol name (for example a label then the digest).
The libsodium docs say `Ed25519ph(m)` is intentionally not equivalent to `Ed25519(SHA512(m))`, and recommend prefixing your own pre-hash with your protocol name.

## Verify

- [ ] RFC 8032 Ed25519ph test vectors verify with libsodium.
- [ ] Format marks signatures as Ed25519ph so verifiers pick the right function.
- [ ] Large-file sign/verify runs in constant memory.

## Checked

2026-10-26, libsodium documentation (libsodium-doc, master) and libsodium source at 1.0.22 era master. Confirmed: multi-part API names and flow, Ed25519ph use with SHA-512 pre-hashing, the Ed25519ph versus Ed25519(SHA512(m)) note and pre-hash advice (docs); sign.c DOM2 prefix with phflag 1 and empty context, message hashed twice in plain signing; Go Options with crypto.SHA512 selecting Ed25519ph. Removed unconfirmed claims about PyNaCl, Bouncy Castle, minisign and the collision-resistance remark.

Method: documentation only; no commands were run.
