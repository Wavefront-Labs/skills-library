---
id: computing-software.cryptography-implementation.libsodium.crypto-onetimeauth-poly1305
name: crypto-onetimeauth-poly1305
category: computing-software
field: cryptography-implementation
product: libsodium
tags: [cryptography-implementation, crypto-onetimeauth, poly1305, libsodium, one-time-mac, mac, poly1305-one-time-key]
level: advanced
status: verified
description: "Use crypto_onetimeauth (Poly1305) only with single-use keys: deriving per-message keys, incremental API, verification, and why long-term keys break it."
sources: ["https://doc.libsodium.org/advanced/poly1305", "https://cr.yp.to/mac/poly1305-20050329.pdf", "https://www.rfc-editor.org/rfc/rfc8439#section-2.5"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# crypto_onetimeauth (Poly1305)

Poly1305 is a one-time authenticator: a key may authenticate **one** message. Two messages under the same key let an
attacker solve for the key and forge tags.

## API
```c
unsigned char key[crypto_onetimeauth_KEYBYTES];       /* 32 bytes, unique per message */
unsigned char tag[crypto_onetimeauth_BYTES];          /* 16 bytes */
crypto_onetimeauth(tag, msg, msg_len, key);
if (crypto_onetimeauth_verify(tag, msg, msg_len, key) != 0) reject();
/* incremental */
crypto_onetimeauth_state st;
crypto_onetimeauth_init(&st, key);
crypto_onetimeauth_update(&st, part1, n1);
crypto_onetimeauth_update(&st, part2, n2);
crypto_onetimeauth_final(&st, tag);
```

## Getting one-time keys
- From a stream cipher keystream per message, the way AEADs do it: first 32 bytes of
  `crypto_stream_xchacha20(key_block, 32, nonce, long_term_key)`.
- From a KDF with a unique message identifier: `crypto_kdf_derive_from_key(otk, 32, msg_id, "OTAUTH__", master)`.

## When to use it
Almost never directly. Use `crypto_aead_*`, `crypto_secretbox` or `crypto_auth` (HMAC-SHA-512-256, reusable key)
instead. Direct use is for implementing a protocol that specifies Poly1305 with its own key schedule.

## Verify
- [ ] Each message's key is derived from a unique nonce/id; no code path reuses a key.
- [ ] RFC 8439 2.5.2 test vector passes (done: key `85d6be78...f51b`, message "Cryptographic Forum Research Group", tag `a8061dc1305136c6c22b8baf0c0127a9` on libsodium.js 1.0.22; KEYBYTES 32, BYTES 16).
