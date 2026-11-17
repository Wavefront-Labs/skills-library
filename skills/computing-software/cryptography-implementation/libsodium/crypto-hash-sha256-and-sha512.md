---
id: computing-software.cryptography-implementation.libsodium.crypto-hash-sha256-and-sha512
name: crypto-hash-sha256-and-sha512
category: computing-software
field: cryptography-implementation
product: libsodium
tags: [cryptography-implementation, crypto-hash-sha256, crypto-hash-sha512, sha256, libsodium, interop]
level: practitioner
status: verified
description: "Use libsodium crypto_hash_sha256 and crypto_hash_sha512 when a protocol mandates SHA-2: one-shot and streaming state APIs, and why generichash is the default otherwise."
sources: ["https://doc.libsodium.org/advanced/sha-2_hash_function", "https://doc.libsodium.org/hashing/generic_hashing"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# crypto_hash_sha256 and crypto_hash_sha512

## When
`crypto_generichash` (BLAKE2b) is libsodium's recommended hash. Use SHA-2 only for interop: file digests compared
with `sha256sum`, protocols that specify SHA-256, certificate fingerprints, Bitcoin-style formats.

## API
```c
unsigned char h[crypto_hash_sha256_BYTES];             /* 32 */
crypto_hash_sha256(h, msg, msg_len);

crypto_hash_sha512_state st;
crypto_hash_sha512_init(&st);
crypto_hash_sha512_update(&st, part1, len1);
crypto_hash_sha512_update(&st, part2, len2);
crypto_hash_sha512_final(&st, h512);                    /* 64 bytes */
```
`crypto_hash` (no suffix) is SHA-512.

## Cautions
- Plain SHA-2 is vulnerable to length extension; do not use `H(key || msg)` as a MAC. Use
  `crypto_auth_hmacsha256` instead.
- Not suitable for passwords; use `crypto_pwhash`.
- The state structs are not thread-safe; one per thread/stream.

## Verify
- [ ] `crypto_hash_sha256("abc")` equals `ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad` (FIPS 180-4 example; reproduced on libsodium.js 1.0.22, where `crypto_hash` also matched SHA-512 of the same input).
