---
id: computing-software.cryptography-implementation.libsodium.aes256gcm-availability-in-libsodium
name: aes256gcm-availability-in-libsodium
category: computing-software
field: cryptography-implementation
product: libsodium
tags: [cryptography-implementation, libsodium, crypto-aead, aes256gcm-is-available, aes-256-gcm, hardware-acceleration, aes-ni, nonce-limits, crypto-aead-aes256gcm-beforenm, aes256gcm-beforenm]
level: advanced
status: verified
description: "Use crypto_aead_aes256gcm in libsodium safely: mandatory availability check, hardware-only implementation, 12-byte nonce limits, precomputation API, and fallback planning."
sources: ["https://doc.libsodium.org/secret-key_cryptography/aead/aes-256-gcm", "https://doc.libsodium.org/secret-key_cryptography/aead", "https://csrc.nist.gov/pubs/sp/800/38/d/final"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# AES256-GCM availability in libsodium

libsodium only implements AES-256-GCM with hardware instructions (x86 AES-NI +
PCLMULQDQ + AVX, per the `crypto_aead_aes256gcm_is_available` source; ARMv8
crypto extensions since 1.0.18, when the implementation was rewritten for
aarch64). The docs state there are no plans for a software fallback, so
calling the functions on unsupported hardware is a bug.

## Mandatory check

```c
if (sodium_init() < 0) abort();
if (crypto_aead_aes256gcm_is_available() == 0) {
    /* fall back: crypto_aead_xchacha20poly1305_ietf_* */
}
```

The docs require `sodium_init()` to have run before `is_available`: it
detects the CPU features the check reads.

Interop consequence: if your format allows only AES-256-GCM and a client runs
on hardware without AES (old ARM, some VMs with masked flags), it cannot
decrypt using libsodium. Either choose XChaCha20-Poly1305 for the format or
use another library (OpenSSL, BoringSSL) with software AES on those clients.

## Nonce and message limits

- Nonce 12 bytes (`NPUBBYTES`); libsodium docs: with random nonces, do not
  encrypt more than 2^32 messages per key, and their nonce table lists only
  counters and permutations as safe options. Prefer a counter nonce or rotate
  keys.
- Switch to a new key before about 350 GB total under one key (docs; the
  figure is for roughly 16 KB messages).
- Max message size per call: `MESSAGEBYTES_MAX` = 16 * (2^32 - 2) = 68719476704
  bytes, just under 64 GiB.
- Tag 16 bytes.

## Precomputation API

For many messages under one key, expand the key schedule once:

```c
crypto_aead_aes256gcm_state st;
crypto_aead_aes256gcm_beforenm(&st, key);
crypto_aead_aes256gcm_encrypt_afternm(c, &clen, m, mlen, ad, adlen, NULL, nonce, &st);
crypto_aead_aes256gcm_decrypt_afternm(m, &mlen, NULL, c, clen, ad, adlen, nonce, &st);
```

The state must be 16-byte aligned (the header declares
`CRYPTO_ALIGN(16)`; allocate with `sodium_malloc` or aligned storage), and it
contains key material - zero it with `sodium_memzero` when done.

## When to choose it

Interop with AES-GCM peers (cloud services, TLS-like formats, FIPS-adjacent
designs) on known hardware. For libsodium-only systems, XChaCha20-Poly1305 or
AEGIS are simpler (larger nonces, no hardware check).

## Verify

- [ ] `is_available` checked after `sodium_init` on every platform build.
- [ ] Fallback path or documented hardware requirement exists.
- [ ] Nonce strategy documented with a per-key message limit.
