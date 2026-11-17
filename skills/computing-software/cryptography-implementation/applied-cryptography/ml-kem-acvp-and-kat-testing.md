---
id: computing-software.cryptography-implementation.applied-cryptography.ml-kem-acvp-and-kat-testing
name: ml-kem-acvp-and-kat-testing
category: computing-software
field: cryptography-implementation
product: applied-cryptography
tags: [applied-cryptography, cryptography-implementation, ml-kem-test-vectors, ml-kem, fips-203, acvp, kat, wycheproof]
level: advanced
status: draft
description: "Test ML-KEM implementations with NIST ACVP JSON vectors and FIPS 203 KATs: keyGen, encaps and decaps prompts, implicit rejection cases and Wycheproof."
sources: ["https://github.com/usnistgov/ACVP-Server/tree/master/gen-val/json-files", "https://pages.nist.gov/ACVP/draft-celi-acvp-ml-kem.html", "https://github.com/C2SP/wycheproof"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# ML-KEM ACVP and KAT testing

## Vector sources
- NIST ACVP-Server `gen-val/json-files/ML-KEM-keyGen-FIPS203` and `ML-KEM-encapDecap-FIPS203`: `prompt.json`,
  `expectedResults.json`, `internalProjection.json`.
- Wycheproof ML-KEM files (decapsulation with malformed ciphertext, invalid encapsulation keys).
- C2SP CCTV "accumulated" tests: hash of 10,000 or 1,000,000 deterministic runs for fast regression.

## What each tests
| Test | Inputs | Checks |
|---|---|---|
| keyGen | seeds d, z | ek, dk exactly |
| encapsulation | ek, m | c, K |
| decapsulation | dk, c | K, including modified c returning implicit-rejection K |
| key checks | ek or dk | modulus check (encaps) and hash check (decaps) per FIPS 203 7.2-7.3 |

## Harness
Expose deterministic internal functions (`ML-KEM.KeyGen_internal(d, z)`, `Encaps_internal(ek, m)`) behind a
test-only build flag; production APIs must draw randomness internally.

## Pitfalls
- Using Round 3 Kyber vectors: FIPS 203 changed domain separation and the shared-key derivation, so Kyber KATs
  will not match.
- Not testing implicit rejection: invalid ciphertexts must yield `J(z || c)`, not an error.

## Verify
- [ ] All ACVP groups for ML-KEM-512/768/1024 pass; CCTV accumulated hash matches.
