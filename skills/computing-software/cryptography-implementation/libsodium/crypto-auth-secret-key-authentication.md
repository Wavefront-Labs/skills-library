---
id: computing-software.cryptography-implementation.libsodium.crypto-auth-secret-key-authentication
name: crypto-auth-secret-key-authentication
category: computing-software
field: cryptography-implementation
product: libsodium
tags: [cryptography-implementation, libsodium, secretbox, crypto-auth, crypto-auth-verify, hmac-sha512-256, message-authentication, webhook-signing, api-tokens]
level: practitioner
status: verified
description: "Authenticate messages with libsodium crypto_auth (HMAC-SHA-512-256): constant-time verify, HMAC-SHA-256/512 variants for interop, multi-part use."
sources: ["https://doc.libsodium.org/secret-key_cryptography/secret-key_authentication", "https://doc.libsodium.org/advanced/hmac-sha2"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# crypto_auth: secret-key message authentication

`crypto_auth` computes a 32-byte tag over a message with a 32-byte key so a
receiver with the same key can detect tampering. Algorithm:
HMAC-SHA-512-256 (HMAC-SHA-512 truncated to 256 bits).

```c
unsigned char key[crypto_auth_KEYBYTES];      /* 32 */
unsigned char tag[crypto_auth_BYTES];         /* 32 */
crypto_auth_keygen(key);
crypto_auth(tag, msg, msglen, key);
if (crypto_auth_verify(tag, msg, msglen, key) != 0) { /* reject */ }
```

`crypto_auth_verify` compares in constant time; never compute and `memcmp`.

## Interop with HMAC-SHA-256 systems

HMAC-SHA-512-256 here is *not* SHA-512/256 inside HMAC and not
HMAC-SHA-256; other systems (webhooks, AWS SigV4, JWT HS256) need the
explicit variants:

```c
crypto_auth_hmacsha256(tag, msg, msglen, key);          /* 32-byte key */
crypto_auth_hmacsha256_verify(tag, msg, msglen, key);
/* multi-part, arbitrary key length: */
crypto_auth_hmacsha256_state st;
crypto_auth_hmacsha256_init(&st, key, keylen);
crypto_auth_hmacsha256_update(&st, part1, len1);
crypto_auth_hmacsha256_final(&st, tag);
```

Also `crypto_auth_hmacsha512*`. For keyed hashing inside libsodium-only
systems, keyed `crypto_generichash` (BLAKE2b) is an alternative MAC.

## When not to use it

- You also need confidentiality: use an AEAD (MAC alone does not encrypt).
- You need third parties to verify without being able to forge: use
  signatures (`crypto_sign`); anyone with a MAC key can create tags.

## Rules

- One key per purpose; derive MAC keys with `crypto_kdf` rather than reusing an encryption key.
- Authenticate the exact bytes received (raw HTTP body for webhooks), plus a
  timestamp to stop replay.

## Verify

- [ ] RFC 4231 vectors pass for `crypto_auth_hmacsha256` (interop path; test case 2 reproduced on libsodium.js 1.0.22, and `crypto_auth` matched `HMAC-SHA-512` cut to 32 bytes).
- [ ] Verification uses `*_verify`, never manual comparison.
- [ ] Peers agree on the HMAC variant (512-256 vs SHA-256).
