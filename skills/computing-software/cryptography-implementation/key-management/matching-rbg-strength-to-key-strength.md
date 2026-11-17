---
id: computing-software.cryptography-implementation.key-management.matching-rbg-strength-to-key-strength
name: matching-rbg-strength-to-key-strength
category: computing-software
field: cryptography-implementation
product: key-management
tags: [key-management, cryptography-implementation, rbg-security-strength, sp-800-133, sp-800-90a, drbg, key-generation, security-strength, entropy]
level: advanced
status: gated
description: "Ensure keys get full security strength from their RBG per SP 800-133: DRBG instantiation strength, entropy input, seed sizes and common shortfalls."
sources: ["https://csrc.nist.gov/pubs/sp/800/133/r2/final", "https://csrc.nist.gov/pubs/sp/800/90/a/r1/final", "https://csrc.nist.gov/pubs/sp/800/57/pt1/r5/final"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Matching RBG strength to key strength

SP 800-133 Rev 2 section 4 requires the RBG to be instantiated at a strength that supports the target data's required strength; a key can be no stronger than the random bits it was generated from. A 256-bit AES key
from a DRBG instantiated at 128-bit strength has 128-bit security.

## Requirements
- The RBG must support a security strength at least equal to the key's target strength (e.g. 256 for AES-256 or
  P-521 private keys, 128 for AES-128 or P-256).
- Hash_DRBG/HMAC_DRBG with SHA-256 and CTR_DRBG with AES-256 can instantiate at 256 bits; CTR_DRBG with AES-128 caps
  at 128 bits.
- SP 800-90A Rev. 1 requires at least `3/2 x security_strength` bits of entropy for instantiation, including the nonce (for 256-bit strength: 384 bits, typically entropy input 256 + nonce 128).
- For asymmetric keys the RBG strength must meet the key pair's strength (SP 800-57 Part 1 Rev. 5 Table 2: RSA-3072 = 128, RSA-15360 = 256; FIPS 186-5 A.2.1 requires a DRBG of the strength associated with len(n)).

## Checking real stacks
- OpenSSL 3: default DRBG is CTR_DRBG AES-256 (`openssl list -random-generators` lists CTR-DRBG, HASH-DRBG, HMAC-DRBG, SEED-SRC and TEST-RAND; `openssl info -seeds` prints the seed source, `os-specific` here; the 3.2 source defaults to cipher `AES-256-CTR`), seeded
  from the OS.
- Linux kernel CRNG (getrandom): treated as full-entropy output for application use after initialisation (gated: unconfirmed, source is paywalled or blocked).
- Java `SecureRandom.getInstanceStrong()` vs `DRBG` provider: `securerandom.drbg.config` (e.g. `Hash_DRBG,SHA-256,256,pr_and_reseed`) sets mechanism and strength (gated: unconfirmed, source is paywalled or blocked) (no JDK here).
- Embedded/HSM: read the module security policy for DRBG strength claims.

## Shortfalls seen in practice
- Seeding a DRBG from a 32-bit time value or PID.
- Generating a key from a password or UUID string instead of the RBG.
- Using `/dev/urandom` before CRNG init on old kernels (see early-boot entropy skill).
- Truncating RBG output with modulo when generating scalars (bias).

## Verify
- [ ] Documented DRBG mechanism and strength for each key-generation path.
- [ ] Strength >= target key strength for every key type.
