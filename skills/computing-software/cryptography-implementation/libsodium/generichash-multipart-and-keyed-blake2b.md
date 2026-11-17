---
id: computing-software.cryptography-implementation.libsodium.generichash-multipart-and-keyed-blake2b
name: generichash-multipart-and-keyed-blake2b
category: computing-software
field: cryptography-implementation
product: libsodium
tags: [cryptography-implementation, libsodium, crypto-generichash, generichash-multipart, blake2b, keyed-hashing, streaming-hash, file-hashing, personalization]
level: practitioner
status: docs-checked
description: "Hash streams and files with libsodium's multi-part crypto_generichash (init/update/final), keyed BLAKE2b as a MAC, output lengths, and state handling."
sources: ["https://doc.libsodium.org/hashing/generic_hashing", "https://github.com/jedisct1/libsodium/blob/master/src/libsodium/include/sodium/crypto_generichash_blake2b.h", "https://github.com/jedisct1/libsodium/blob/master/src/libsodium/crypto_generichash/blake2b/ref/blake2b-ref.c"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Multi-part and keyed BLAKE2b with crypto_generichash

## Multi-part (streaming) hashing

```c
crypto_generichash_state st;
unsigned char out[crypto_generichash_BYTES];          /* 32 default; 16..64 allowed */
crypto_generichash_init(&st, key, keylen, sizeof out); /* key = NULL, keylen = 0 for unkeyed */
while ((n = fread(buf, 1, sizeof buf, f)) > 0)
    crypto_generichash_update(&st, buf, n);
crypto_generichash_final(&st, out, sizeof out);
```

- Output length is fixed at `init`; the same length must be passed to `final`.
- Output length is part of the BLAKE2b parameter block, so a 32-byte hash is
  **not** a prefix of the 64-byte hash of the same input. Fix the length in
  your format spec.
- After `crypto_generichash_final` the state must not be used again unless it is re-initialised with `crypto_generichash_init`; `sodium_memzero` it after keyed use as a precaution.
- `crypto_generichash_statebytes()` gives the size for bindings that allocate opaquely.

## Keyed mode (MAC)

Passing a key (any length from 0 to `crypto_generichash_KEYBYTES_MAX` = 64; `crypto_generichash_KEYBYTES` = 32 is recommended, and for a secret key the recommended minimum is `crypto_generichash_KEYBYTES_MIN` = 16)
makes BLAKE2b usable as a PRF. No HMAC wrapper is needed (the docs say it is safe against length extension).

```c
crypto_generichash(tag, 32, msg, msglen, key, 32);
/* verify: recompute and compare with sodium_memcmp (constant time) */
if (sodium_memcmp(tag, expected, 32) != 0) { /* reject */ }
```

For interop with non-libsodium systems that expect HMAC-SHA-256, use
`crypto_auth_hmacsha256` instead.

## Domain separation

libsodium exposes BLAKE2b salt and personalization via
`crypto_generichash_blake2b_salt_personal` (`crypto_generichash_blake2b_SALTBYTES` and `_PERSONALBYTES`, both 16). Use a personalization string per purpose ("myapp-file-v1") when the
same key or input type serves several uses; or prefix inputs with a context
label.

## Verify

- [ ] Published BLAKE2b test vectors reproduce for the chosen length.
- [ ] Streaming hash of a file equals one-shot hash of its contents.
- [ ] Keyed tags compared with `sodium_memcmp`.

## Checked

2026-10-26, libsodium documentation (libsodium-doc, master) and libsodium source at 1.0.22 era master. Confirmed: init/update/final signatures and outlen handling, state reuse rule, output 16 to 64 bytes with default 32, key size rules, salt and personal functions with 16-byte sizes (header), digest length stored in the BLAKE2b parameter block (blake2b-ref.c), sodium_memcmp for constant-time comparison, crypto_generichash_statebytes. Removed unconfirmed PyNaCl and hashlib compatibility claims and an RFC 7693 appendix reference.

Method: documentation only; no commands were run.
