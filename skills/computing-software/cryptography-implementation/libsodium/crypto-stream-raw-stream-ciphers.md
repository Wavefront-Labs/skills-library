---
id: computing-software.cryptography-implementation.libsodium.crypto-stream-raw-stream-ciphers
name: crypto-stream-raw-stream-ciphers
category: computing-software
field: cryptography-implementation
product: libsodium
tags: [cryptography-implementation, crypto-stream, xchacha20, xsalsa20, stream-cipher, libsodium, unauthenticated-encryption]
level: advanced
status: verified
description: "Use libsodium crypto_stream_* raw stream ciphers only where authentication exists elsewhere: XSalsa20/XChaCha20 keystreams, xor_ic for seeking, and nonce rules."
sources: ["https://doc.libsodium.org/advanced/stream_ciphers", "https://doc.libsodium.org/advanced/stream_ciphers/xchacha20", "https://github.com/jedisct1/libsodium/blob/master/src/libsodium/Makefile.am"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# crypto_stream raw stream ciphers

## Functions
- `crypto_stream` / `crypto_stream_xor`: XSalsa20, 24-byte nonce.
- `crypto_stream_xchacha20_xor`, `crypto_stream_chacha20_ietf_xor`, `crypto_stream_salsa20_xor`.
- `*_xor_ic(c, m, mlen, n, ic, k)`: start at block counter `ic` (64-byte blocks) for random access (checked: `xchacha20_xor_ic` with `ic=1` equals bytes 64-127 of the plain XOR stream).
- XChaCha20 (`crypto_stream_xchacha20*`) is left out of `--enable-minimal` builds.
- `crypto_stream_xchacha20(out, len, n, k)`: raw keystream, useful as a deterministic PRG from a key.

## Why "advanced"
No authentication: flipping a ciphertext bit flips the same plaintext bit. Use only when:
- A MAC covers the ciphertext elsewhere (custom encrypt-then-MAC with `crypto_auth`).
- Generating deterministic pseudorandom bytes from a seed (`crypto_stream_xchacha20` with a fixed nonce).
- Disk-like random access where an outer layer provides integrity.
Otherwise use `crypto_secretbox`, `crypto_aead_*`, or `crypto_secretstream`.

## Rules
- Never reuse (key, nonce). XChaCha20/XSalsa20 24-byte nonces can be random.
- With `xor_ic`, keep offsets aligned: counter = offset / 64, discard `offset % 64` bytes of the first block.
- `crypto_stream_chacha20_ietf` counter is 32-bit: 256 GB per nonce maximum (libsodium docs; `crypto_stream_chacha20_ietf_MESSAGEBYTES_MAX` is `64 * 2^32`).

## Verify
- [ ] Code review confirms an independent MAC verified before decryption, or a non-confidential PRG use.
