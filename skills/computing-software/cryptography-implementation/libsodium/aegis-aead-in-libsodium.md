---
id: computing-software.cryptography-implementation.libsodium.aegis-aead-in-libsodium
name: aegis-aead-in-libsodium
category: computing-software
field: cryptography-implementation
product: libsodium
tags: [cryptography-implementation, libsodium, crypto-aead, aegis-256, aegis-128l, aead, high-throughput, random-nonce, cfrg-aegis]
level: advanced
status: verified
description: "Use AEGIS-256 and AEGIS-128L in libsodium 1.0.19+: when they beat AES-GCM, nonce and tag sizes (32-byte tags), hardware requirements, and interop status."
sources: ["https://doc.libsodium.org/secret-key_cryptography/aead/aegis-256", "https://doc.libsodium.org/secret-key_cryptography/aead/aegis-128l", "https://www.rfc-editor.org/rfc/rfc10032"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AEGIS AEAD in libsodium

AEGIS (RFC 10032, September 2026, an informational CFRG/IRTF document; CAESAR
finalist) is an AES-round-based AEAD designed to be much faster than AES-GCM
on CPUs with AES instructions, with larger nonces and longer tags. libsodium
1.0.19+ ships `crypto_aead_aegis128l_*` and `crypto_aead_aegis256_*`.

## Sizes

| | AEGIS-128L | AEGIS-256 |
|---|---|---|
| Key | 16 B | 32 B |
| Nonce | 16 B | 32 B |
| Tag (`ABYTES`) | 32 B | 32 B |
| Random nonces safe? | up to ~2^48 messages per key | effectively unlimited |

libsodium uses the 256-bit tag variant (checked: `ABYTES` is 32 for both, and
PyNaCl 1.6.2 reproduces the RFC 10032 Appendix A.2.2 and A.2.4 256-bit tag test
vectors). RFC 10032 allows 128- or 256-bit tags, so other implementations may
default to 128-bit. Interop requires the same tag length.

## Code

```c
if (sodium_init() < 0) abort();
unsigned char k[crypto_aead_aegis256_KEYBYTES], n[crypto_aead_aegis256_NPUBBYTES];
crypto_aead_aegis256_keygen(k);
randombytes_buf(n, sizeof n);
crypto_aead_aegis256_encrypt(c, &clen, m, mlen, ad, adlen, NULL, n, k);
if (crypto_aead_aegis256_decrypt(m, &mlen, NULL, c, clen, ad, adlen, n, k) != 0) { /* reject */ }
```

## When to pick it

- High-throughput bulk encryption on servers/desktops with AES-NI or ARMv8
  crypto: libsodium's docs call AEGIS extremely fast on CPUs with AES
  pipelines (measure the ratio to AES-GCM yourself).
- You want random nonces with AES-class speed: AEGIS-256's 256-bit nonce
  removes the GCM 2^32 random-nonce ceiling.
- Key-committing behaviour: libsodium's docs say AEGIS is assumed to be
  key-committing; RFC 10032 says a 128-bit tag gives 64-bit committing
  security and a 256-bit tag makes finding a collision impractical. This is
  an assumption, not a proof; check it against your requirements.

## When not to

- No AES hardware: libsodium has a software fallback but it is slower and not
  the reason to choose AEGIS; use XChaCha20-Poly1305.
- FIPS requirement: AEGIS is not NIST-approved.
- Interop with systems that only speak GCM/ChaCha (TLS, JOSE, cloud KMS).
- Standard status: RFC 10032 is informational (not Internet Standards Track);
  pin library versions.

## Verify

- [ ] libsodium version >= 1.0.19 (`sodium_version_string()`).
- [ ] Tag length agreed (32 bytes) with any non-libsodium peer.
- [ ] Test vectors from RFC 10032 Appendix A (256-bit tag cases) pass.
- [ ] Benchmark on target hardware confirms the speed gain.
