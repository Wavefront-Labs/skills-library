---
id: computing-software.cryptography-implementation.applied-cryptography.ml-kem-seed-versus-expanded-key-formats
name: ml-kem-seed-versus-expanded-key-formats
category: computing-software
field: cryptography-implementation
product: applied-cryptography
tags: [cryptography-implementation, applied-cryptography, ml-kem, ml-kem-key-format, fips-203, private-key-seed]
level: advanced
status: docs-checked
description: "Store ML-KEM private keys as the 64-byte seed or the expanded decapsulation key: what each contains, trade-offs and the FIPS 203 consistency checks."
sources: ["https://csrc.nist.gov/pubs/fips/203/final", "https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ML-KEM seed versus expanded key formats

FIPS 203 KeyGen draws two 32-byte random values `d` and `z`. The 64-byte
seed `(d, z)` deterministically produces the encapsulation key `ek` and the
expanded decapsulation key `dk` (1632, 2400 or 3168 bytes for ML-KEM-512,
-768, -1024). `dk` is the K-PKE decryption key, a copy of `ek`, `H(ek)` and
`z`.

## Which to store

| Format | Pros | Cons |
|---|---|---|
| Seed (64 B) | Small; `dk` and `ek` are always consistent | Must re-run ML-KEM.KeyGen_internal to expand |
| Expanded `dk` | No recomputation | Large; seed cannot be recovered from it; can be internally inconsistent if corrupted |

FIPS 203 explicitly allows storing the seed for later expansion with
ML-KEM.KeyGen_internal, and says it is sensitive data that shall get the same
safeguards as a decapsulation key.

## Domain separation in the seed

K-PKE.KeyGen hashes `d` together with the module dimension `k`, so a seed
expanded under the wrong parameter set yields an unrelated key rather than a
related one. Store the parameter set name with the seed anyway.

## Consistency checks on load

Key pair check (section 7.1): if a seed is available, re-run KeyGen_internal
and compare to `(ek, dk)`; check `ek` (length 384k+32 and modulus check);
check `dk` (length 768k+96 and `H(ek)` inside `dk` equals the hash of the
embedded `ek`); then a pairwise test: Encaps with `ek`, Decaps with `dk`, and
reject unless the shared secrets match. These checks detect corruption but
do not prove the pair came from ML-KEM.KeyGen.

## Interop notes

- Pre-standard Kyber encodings differ from ML-KEM (FIPS 203 Appendix C lists
  changes to the algorithms); regenerate keys rather than converting.

## Verify

- [ ] Round-trip test: seed -> dk -> ek matches the stored encapsulation key.
- [ ] Import of a tampered `dk` (wrong `H(ek)`) is rejected.

## Checked

2026-11-01. Confirmed against FIPS 203 (NIST.FIPS.203.pdf): seed (d, z)
and its sensitivity (3.3, 7.1), dk layout (Algorithm 16), key sizes (Table
3), key pair check (7.1), domain separation footnote (Algorithm 13),
Appendix C. Removed: PKCS#8 CHOICE, LAMPS draft, OpenSSL 3.5 and HSM claims
(not read this batch).
Method: documentation only; no commands were run.
