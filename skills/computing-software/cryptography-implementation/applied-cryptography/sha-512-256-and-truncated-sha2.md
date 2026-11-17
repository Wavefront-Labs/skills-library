---
id: computing-software.cryptography-implementation.applied-cryptography.sha-512-256-and-truncated-sha2
name: sha-512-256-and-truncated-sha2
category: computing-software
field: cryptography-implementation
product: applied-cryptography
tags: [applied-cryptography, cryptography-implementation, sha-512-256, sha-512-224, truncated-hash, fips-180-4, length-extension]
level: practitioner
status: verified
description: "Choose SHA-512/256 and SHA-512/224 correctly: distinct IVs from plain truncation, length-extension resistance, speed on 64-bit CPUs, and library names."
sources: ["https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.180-4.pdf", "https://docs.openssl.org/3.0/man7/EVP_MD-SHA2/"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# SHA-512/256 and truncated SHA-2

## What it is (FIPS 180-4 5.3.6)
SHA-512/t runs SHA-512 with a different initial hash value (generated per t; t < 512 and not 384) and outputs the leftmost t bits.
Because the IV differs, `SHA-512/256(m)` is not the first 32 bytes of `SHA-512(m)`; mixing them breaks interop.

## Why use it
- Truncated output hides internal state, so it resists length extension (unlike SHA-256 and SHA-512).
- Speed depends on the CPU: on the test PC (with SHA extensions) SHA-256 hashed 10 MB in 4.7 ms and SHA-512/256 in 10.2 ms (Python), so benchmark rather than assume.
- 128-bit collision strength, same as SHA-256.

## Names
- OpenSSL: `openssl dgst -sha512-256`, EVP name `SHA2-512/256` (alias `SHA512-256`).
- Go: `crypto/sha512.Sum512_256`; Python: `hashlib.new("sha512_256")` (depends on OpenSSL build); both
  return `53048e26...af23` for "abc" (run).
  libsodium `crypto_auth` is named HMAC-SHA512-256 in its docs (HMAC-SHA-512 with 256-bit output), a different construction.
- Java: see the JDK `MessageDigest` docs for the algorithm name (not run here).

## Pitfalls
- libsodium HMAC-SHA-512-256 truncation is not SHA-512/256; document which one a format uses.
- Some platforms lack SHA-512/256 (older WebCrypto, some HSMs). Check before picking it for a protocol.

## Verify
- [ ] `echo -n abc | openssl dgst -sha512-256` gives `53048e2681941ef9...` (checked on OpenSSL 3.2.3, which prints `SHA2-512/256(stdin)=`;
  the first 32 bytes of SHA-512("abc") differ, run).
