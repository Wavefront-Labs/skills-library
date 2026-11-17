---
id: computing-software.cryptography-implementation.libsodium.libsodium-nonce-management
name: libsodium-nonce-management
category: computing-software
field: cryptography-implementation
product: libsodium
tags: [cryptography-implementation, aead-nonce-management, secretbox-nonce, libsodium, nonce, sodium-increment, xchacha20poly1305, crypto-secretbox, nonce-reuse]
level: practitioner
status: docs-checked
description: "Manage nonces across libsodium APIs: random 24-byte nonces for secretbox, box and XChaCha AEAD, counters with sodium_increment for 8- and 12-byte nonces, and documented limits."
sources: ["https://doc.libsodium.org/secret-key_cryptography/aead", "https://doc.libsodium.org/secret-key_cryptography/secretbox", "https://doc.libsodium.org/helpers", "https://pynacl.readthedocs.io/en/latest/secret/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# libsodium nonce management

## Nonce sizes and strategies
| API | Nonce | Random nonce safe? | Strategy |
|---|---|---|---|
| `crypto_secretbox_easy` (XSalsa20-Poly1305) | 24 B | Yes | `randombytes_buf(nonce, sizeof nonce)` per message |
| `crypto_box_easy` | 24 B | Yes | Random per message (see the box nonce skill for the shared-key caveat) |
| `crypto_aead_xchacha20poly1305_ietf_*` | 24 B | Yes | Random per message; the recommended AEAD |
| `crypto_aead_chacha20poly1305_ietf_*` | 12 B | Limited: the docs give 2^32 messages with random nonces, and list counter or permutation as the safe options | Counter, or a key per message |
| `crypto_aead_chacha20poly1305_*` (original) | 8 B | Limited: 2^16 messages with random nonces; the docs list counter or permutation | Counter |
| `crypto_aead_aes256gcm_*` | 12 B | Limited: 2^32 messages with random nonces; the docs list counter or permutation | Counter, or a key per message |
| `crypto_aead_aegis256_*` | 32 B | Yes (counter, permutation or random) | Random |
| `crypto_aead_aegis128l_*` | 16 B | Yes up to 2^48 messages with random nonces | Random for moderate volumes; counter otherwise |
| `crypto_secretstream_*` | No nonce argument | n/a | `init_push` creates a header per stream (24 bytes), sent with the stream |

## Counters
```c
unsigned char nonce[crypto_aead_chacha20poly1305_ietf_NPUBBYTES] = {0};
/* ...for each message */
sodium_increment(nonce, sizeof nonce);      /* little-endian, constant-time */
```
- Persist the counter or derive a fresh key per session so restarts never reuse a value.
- Split the nonce space per direction or per sender (first byte = sender id) when several parties share a key.
- `sodium_compare(a, b, len)` compares little-endian numbers in constant time, useful for replay windows.

## Transmitting the nonce
Nonces need not be confidential: prepend to the ciphertext (nonce then ciphertext) and slice on decrypt. Never derive the nonce
from the plaintext.

## Gotchas
- A nonce must never be reused with the same key (libsodium secretbox docs); PyNaCl's docs add that reuse may let an attacker decrypt or forge other messages.
- The `nsec` parameter in the AEAD functions is unused (the docs say pass NULL).
- Language bindings sometimes generate the nonce for you (PyNaCl's `SecretBox.encrypt` does when none is given); confirm before
  adding your own.

## Verify
- [ ] Nonce strategy documented per API used.
- [ ] Test: encrypting the same plaintext twice gives different nonce and ciphertext.

## Checked

2026-10-26, libsodium documentation (libsodium-doc, master) and libsodium source at 1.0.22 era master. Confirmed in the AEAD page: nonce sizes (AEGIS-128L 128 bits, AEGIS-256 256 bits, AES256-GCM and ChaCha20-Poly1305-IETF 96 bits, original ChaCha20-Poly1305 64 bits, XChaCha20-Poly1305-IETF 192 bits), safe nonce options, random-nonce message limits (2^32, 2^16, 2^48), nsec NULL; sodium_increment (little-endian, constant time) and sodium_compare in the helpers page; secretbox and box use randombytes_buf nonces; secretbox and crypto_box 24-byte nonces from headers. The earlier table wrongly called random nonces unsafe for AES-GCM and ChaCha20-Poly1305 without giving the documented limits.

Method: documentation only; no commands were run.
