---
id: computing-software.software-engineering.erlang.crypto-module
name: crypto-module
category: computing-software
field: software-engineering
product: erlang
tags: [erlang, erl-security, crypto-module]
level: advanced
status: draft
description: "Erlang crypto: strong_rand_bytes, hash, mac, AEAD with crypto_one_time_aead, pbkdf2_hmac and constant-time compare."
sources:
  - https://www.erlang.org/doc/apps/crypto/
  - https://www.erlang.org/doc/apps/ssl/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# The crypto module
**Goal:** use crypto primitives correctly.

```erlang
Rand = crypto:strong_rand_bytes(32),
Digest = crypto:hash(sha256, <<"data">>),
Tag = crypto:mac(hmac, sha256, Key, Data),
{Cipher, AuthTag} = crypto:crypto_one_time_aead(aes_256_gcm, Key32, IV12, Plain, AAD, true),
Plain = crypto:crypto_one_time_aead(aes_256_gcm, Key32, IV12, Cipher, AAD, AuthTag, false),
Derived = crypto:pbkdf2_hmac(sha256, Password, Salt, 600000, 32),
true = crypto:hash_equals(Tag, Tag).        % constant time compare (OTP 25+)
```
- Use `crypto:strong_rand_bytes/1` for keys, tokens, IVs; `rand:uniform/1` is not cryptographically secure.
- Never reuse an IV/nonce with the same key in GCM; generate a fresh random 12-byte IV per message.
- Prefer AEAD (GCM, ChaCha20-Poly1305) over unauthenticated CBC.
- Choose the iteration count for password hashing from current guidance (OWASP) and your latency budget; consider Argon2 via a library.
- Application `crypto` must be in `applications`; it needs OpenSSL at runtime.

## Gotchas
- Comparing MACs with `=:=` leaks timing; use `crypto:hash_equals/2`.
- Old crypto functions (`crypto:block_encrypt/4`) were removed; use `crypto_one_time*`.

## Self-check
Encrypt and decrypt a message and flip one bit in the ciphertext to confirm the tag check fails.
