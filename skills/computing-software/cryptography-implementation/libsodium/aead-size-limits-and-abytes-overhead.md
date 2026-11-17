---
id: computing-software.cryptography-implementation.libsodium.aead-size-limits-and-abytes-overhead
name: aead-size-limits-and-abytes-overhead
category: computing-software
field: cryptography-implementation
product: libsodium
tags: [cryptography-implementation, aead-abytes, libsodium, aead, message-size-limit, buffer-sizing]
level: practitioner
status: verified
description: "Size buffers and messages for libsodium AEADs: ABYTES tag overhead, messagebytes_max per construction, NPUBBYTES, and per-key message count limits."
sources: ["https://doc.libsodium.org/secret-key_cryptography/aead", "https://doc.libsodium.org/secret-key_cryptography/aead/aes-256-gcm", "https://github.com/jedisct1/libsodium/tree/master/src/libsodium/include/sodium"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AEAD size limits and ABYTES overhead

## Constants per construction
| Construction | KEYBYTES | NPUBBYTES | ABYTES | Max message |
|---|---|---|---|---|
| `xchacha20poly1305_ietf` | 32 | 24 | 16 | `SIZE_MAX - ABYTES` (about 2^64 bytes) |
| `chacha20poly1305_ietf` | 32 | 12 | 16 | 256 GiB - 64 |
| `chacha20poly1305` (original) | 32 | 8 | 16 | `SIZE_MAX - ABYTES` (about 2^64 bytes) |
| `aes256gcm` | 32 | 12 | 16 | 16 * (2^32 - 2) = 68719476704 bytes (2^36 - 32, just under 64 GiB) |
| `aegis256` / `aegis128l` | 32/16 | 32/16 | 32 for both | 2^61 - 1 bytes |

Values checked against the libsodium 1.0.20 headers and by calling PyNaCl 1.6.2 (`nacl.bindings.crypto_aead_*_MESSAGEBYTES_MAX`). The `chacha20poly1305_ietf` maximum is `64 * (2^32 - 1)` bytes, which the docs round to 256 GB. Query at runtime: `crypto_aead_xchacha20poly1305_ietf_messagebytes_max()`.

## Buffers
- Combined mode: `c` needs `mlen + ABYTES`; output length via `clen_p`.
- Detached mode: ciphertext same length as message, separate `mac` buffer of `ABYTES`.
- Decrypt fails (returns -1) if `clen < ABYTES`; check lengths before calling to give clean errors.

## Limits beyond size
- Random nonces, libsodium's table of safe message counts per key: `aes256gcm` and `chacha20poly1305_ietf` 2^32, original `chacha20poly1305` 2^16, `aegis128l` 2^48; `xchacha20poly1305_ietf` and `aegis256` have no practical limit. The docs recommend counters or permutations for the 12-byte and 8-byte nonce constructions.
- AES-256-GCM: switch to a new key before about 350 GB encrypted under one key (libsodium docs).
- For big files use `crypto_secretstream` (chunks with automatic rekeying) instead of one huge AEAD call.

## Verify
- [ ] Unit tests use the `*_ABYTES` / `*_NPUBBYTES` macros, not hard-coded numbers.
