---
id: computing-software.cryptography-implementation.libsodium.crypto-auth-hmacsha256-and-hmacsha512
name: crypto-auth-hmacsha256-and-hmacsha512
category: computing-software
field: cryptography-implementation
product: libsodium
tags: [cryptography-implementation, crypto-auth-hmacsha256, crypto-auth-hmacsha512, hmac, libsodium, interop]
level: practitioner
status: verified
description: "Use libsodium crypto_auth_hmacsha256 and hmacsha512 for interop with standard HMAC, versus the default crypto_auth (HMAC-SHA-512-256), including multi-part APIs."
sources: ["https://doc.libsodium.org/advanced/hmac-sha2", "https://doc.libsodium.org/secret-key_cryptography/secret-key_authentication"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# crypto_auth_hmacsha256 and hmacsha512

## Which function
- `crypto_auth` = HMAC-SHA-512 truncated to 32 bytes (HMAC-SHA-512-256). Fine inside libsodium-only systems,
  but other stacks computing "HMAC-SHA256" produce different tags.
- `crypto_auth_hmacsha256` = standard HMAC-SHA-256 (RFC 2104), 32-byte tag. Use for webhooks, AWS SigV4-style
  APIs, JWT HS256.
- `crypto_auth_hmacsha512` = standard HMAC-SHA-512, 64-byte tag.

## One-shot
```c
unsigned char key[crypto_auth_hmacsha256_KEYBYTES];      /* 32 */
crypto_auth_hmacsha256_keygen(key);
unsigned char tag[crypto_auth_hmacsha256_BYTES];
crypto_auth_hmacsha256(tag, msg, msg_len, key);
if (crypto_auth_hmacsha256_verify(tag, msg, msg_len, key) != 0) { /* reject */ }
```
The one-shot API takes a fixed 32-byte key. Verify is constant time.

## Arbitrary key length (interop with existing secrets)
```c
crypto_auth_hmacsha256_state st;
crypto_auth_hmacsha256_init(&st, key, key_len);          /* any length; long keys are hashed */
crypto_auth_hmacsha256_update(&st, part1, len1);
crypto_auth_hmacsha256_update(&st, part2, len2);
crypto_auth_hmacsha256_final(&st, tag);
```
Compare with `sodium_memcmp(tag, expected, 32)` when you compute rather than call `_verify`.

## Verify
- [ ] RFC 4231 test case 2 (`key = "Jefe"`) reproduces via the multi-part API (done in libsodium.js 1.0.22: `5bdcc146...ec3843`, which is in the RFC text). The one-shot call rejected a 5-byte key; `crypto_auth` equals HMAC-SHA-512 truncated to 32 bytes and `crypto_auth_hmacsha256` equals Node's `createHmac('sha256')`.
