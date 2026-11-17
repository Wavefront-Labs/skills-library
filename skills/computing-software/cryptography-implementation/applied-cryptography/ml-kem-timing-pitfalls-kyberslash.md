---
id: computing-software.cryptography-implementation.applied-cryptography.ml-kem-timing-pitfalls-kyberslash
name: ml-kem-timing-pitfalls-kyberslash
category: computing-software
field: cryptography-implementation
product: applied-cryptography
tags: [applied-cryptography, cryptography-implementation, kyberslash, ml-kem, timing-attack, constant-time, division, decapsulation]
level: sme
status: draft
description: "Avoid ML-KEM timing leaks like KyberSlash: secret-dependent division in compression, branchy decapsulation comparison, and tooling to detect them."
sources: ["https://kyberslash.cr.yp.to/", "https://eprint.iacr.org/2024/1049", "https://github.com/agl/ctgrind"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# ML-KEM timing pitfalls (KyberSlash)

## KyberSlash (2023-2024)
Reference Kyber code compressed coefficients with `(x << d) + q/2) / q`. Division by the constant q compiles to a
`div` instruction on some compilers/targets (notably with `-Os` or on ARM Cortex-M and some x86 paths), whose
latency depends on the secret numerator. Researchers recovered keys from timing across many decapsulations.
Fix: replace division by a multiply-and-shift with a precomputed constant (Barrett style).

## Other hotspots
- Decapsulation re-encrypts and compares `c'` to `c`; the comparison and the selection between real key and
  rejection key must be constant time (`cmov`, not `if`).
- Polynomial sampling and NTT: no secret-indexed table lookups.
- Clangover (2024): clang turned a constant-time mask into a branch in `poly_frommsg`; check compiled output.

## Detection
- Run under ctgrind/Valgrind memcheck with secrets marked undefined, or TIMECOP (SUPERCOP).
- `dudect` statistical timing tests on decapsulation with fixed vs random ciphertexts.
- Inspect disassembly for `div`, `idiv`, `udiv` and conditional branches in secret paths.

## Verify
- [ ] Library version includes KyberSlash fixes (PQClean, liboqs 0.10+, reference after Jan 2024).
- [ ] Constant-time checker passes on the release build flags.
