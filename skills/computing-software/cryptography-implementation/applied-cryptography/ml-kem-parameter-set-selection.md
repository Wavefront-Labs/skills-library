---
id: computing-software.cryptography-implementation.applied-cryptography.ml-kem-parameter-set-selection
name: ml-kem-parameter-set-selection
category: computing-software
field: cryptography-implementation
product: applied-cryptography
tags: [cryptography-implementation, applied-cryptography, ml-kem, ml-kem-parameter-sets, fips-203, post-quantum, kyber, key-encapsulation]
level: practitioner
status: docs-checked
description: "Pick ML-KEM-512, 768 or 1024: security categories, key and ciphertext sizes from FIPS 203, the NIST default, and what changes on the wire."
sources: ["https://csrc.nist.gov/pubs/fips/203/final", "https://datatracker.ietf.org/doc/draft-ietf-tls-ecdhe-mlkem/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ML-KEM-512/768/1024 selection

ML-KEM (FIPS 203, formerly Kyber) is the NIST post-quantum key-encapsulation
mechanism. All three parameter sets produce a 32-byte shared secret; they
differ in security category and size.

| Parameter set | NIST category | Encaps key | Decaps key (expanded) | Ciphertext |
|---|---|---|---|---|
| ML-KEM-512 | 1 | 800 B | 1632 B | 768 B |
| ML-KEM-768 | 3 | 1184 B | 2400 B | 1088 B |
| ML-KEM-1024 | 5 | 1568 B | 3168 B | 1568 B |

FIPS 203 also allows storing the key-generation seed (d, z) instead of the expanded decapsulation key.

## How to choose

- **ML-KEM-768** is the general default: FIPS 203 says NIST recommends it as the
  default parameter set, and the TLS hybrid group X25519MLKEM768 uses it.
- **ML-KEM-1024** where policy requires category 5 (for example the
  SecP384r1MLKEM1024 TLS hybrid group); check your own policy, which may mandate it.
- **ML-KEM-512** only when size is critical and category 1 is acceptable;
  check that your policy accepts it.

## Practical notes

- Pin the parameter set in the protocol or key metadata; never infer it from
  key length at runtime without validating.
- Pair with a classical KEM (hybrid) during the transition unless a policy
  explicitly requires pure PQ.
- Check your library supports the parameter sets you need before committing.

## Verify

- [ ] Chosen set recorded in the crypto inventory with the policy reason.
- [ ] Wire formats, database columns and message limits accommodate the sizes above.

## Checked
2026-11-01. Confirmed in the FIPS 203 PDF: the three parameter sets and categories 1/3/5, the encapsulation key,
decapsulation key and ciphertext sizes and 32-byte shared secret, the NIST recommendation of ML-KEM-768 as default,
and seed (d, z) storage. Confirmed in the IETF TLS ECDHE-MLKEM draft: X25519MLKEM768, SecP256r1MLKEM768 and
SecP384r1MLKEM1024 groups. Removed: CNSA 2.0 mandate, browser/vendor/library adoption lists, performance comparison and
EU guidance claims (not confirmed).
Method: documentation only; no commands were run.
