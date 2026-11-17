---
id: computing-software.cryptography-implementation.key-management.fips-186-5-ecc-key-generation
name: fips-186-5-ecc-key-generation
category: computing-software
field: cryptography-implementation
product: key-management
tags: [key-management, cryptography-implementation, ecc-key-generation, fips-186-5, ecdsa, key-generation, rejection-sampling]
level: advanced
status: gated
description: "Generate ECC private keys per FIPS 186-5 Appendix A.2: extra random bits versus rejection sampling, valid scalar range, public point computation and validation."
sources: ["https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.186-5.pdf", "https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-186.pdf"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# FIPS 186-5 ECC key generation

## Two approved methods for d in [1, n-1]
- **A.2.1 extra random bits**: draw l random bits as integer c, then `d = (c mod (n-1)) + 1` (conversion A.4.1, bias bound 2^-t with t at least 64). FIPS 186-5 Table A.2 gives the required and recommended l per curve: P-256 288 required / 352 recommended, P-224 224/224, P-384 384/384, P-521 521/521 (so `len(n) + 64` is a safe rule of thumb, not the table's value; for P-384 and P-521 n is so close to a power of two that no extra bits are needed).
- **A.2.2 rejection sampling**: draw `len(n)` bits as c; if c is out of range (A.4.2 discard method) the procedure returns an ERROR, so the caller starts again with fresh bits; otherwise `d = c + 1`.

Then compute `Q = d*G`. The DRBG must provide at least the curve's security strength (128 for P-256).

## Common bugs
- `d = random_bytes(32) mod n` with no extra bits: biased for curves where n is not close to a power of two
  (biased nonces were exploited in ECDSA; keys share the bias concern).
- Allowing d = 0.
- Using a non-approved RNG (`Math.random`, `rand()`).

## Validation
- Private: 1 <= d <= n-1.
- Public: Q is on the curve, not the identity, and n*Q = identity (SP 800-56A Rev. 3 section 5.6.2.3, full public-key validation for ECC in 5.6.2.3.3). FIPS modules run a
  pairwise consistency test (sign and verify) after generation (gated: unconfirmed, source is paywalled or blocked).

## In practice
Call the library (OpenSSL `EVP_PKEY_keygen`, Go `ecdsa.GenerateKey`, Java `KeyPairGenerator("EC")`); they use
compliant methods. Implement A.2 only in constrained firmware, and test against ACVP/CAVP KeyGen vectors (gated: unconfirmed, source is paywalled or blocked).

## Verify
- [ ] ACVP ECDSA KeyGen/KeyVer tests pass; generation code reviewed for bias.
