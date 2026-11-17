---
id: computing-software.cryptography-implementation.libsodium.crypto-core-ed25519-point-operations
name: crypto-core-ed25519-point-operations
category: computing-software
field: cryptography-implementation
product: libsodium
tags: [cryptography-implementation, crypto-core-ed25519, ed25519, elliptic-curve, libsodium, point-validation, hash-to-curve]
level: sme
status: verified
description: "Use libsodium crypto_core_ed25519 and crypto_scalarmult_ed25519 for low-level group math: point validation, hash-to-curve, scalar ops, and when ristretto255 is safer."
sources: ["https://doc.libsodium.org/advanced/point-arithmetic", "https://doc.libsodium.org/advanced/point-arithmetic/ristretto", "https://www.rfc-editor.org/rfc/rfc9380", "https://github.com/jedisct1/libsodium/blob/master/ChangeLog"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# crypto_core_ed25519 point operations

## Functions
- `crypto_core_ed25519_is_valid_point(p)`: canonical encoding, on curve, not small order, in the main subgroup (docs). The 1.0.20-stable changelog lists a security fix to this function, so use 1.0.20 or later.
- `crypto_core_ed25519_add` / `_sub`: point addition (inputs must be valid points).
- `crypto_core_ed25519_from_uniform(p, r32)`: Elligator 2 map from 32 uniform bytes (1.0.16+).
- `crypto_core_ed25519_from_hash(p, h64)` (1.0.18+): hash-to-curve style map from 64 bytes. Both are in the 1.0.20 header and exported by libsodium.js 1.0.22; the current master header instead declares `crypto_core_ed25519_from_string[_nu]` (with `crypto_core_ed25519_H2CSHA256`/`H2CSHA512`), so check your installed header.
- `crypto_core_ed25519_random(p)`.
- Scalars mod L: `crypto_core_ed25519_scalar_random`, `_add`, `_sub`, `_mul`, `_invert`, `_negate`,
  `_complement`, `_reduce` (64-byte input to scalar).
- `crypto_scalarmult_ed25519(q, n, p)` clamps n; `crypto_scalarmult_ed25519_noclamp` does not.
  `crypto_scalarmult_ed25519_base[_noclamp]`.
- Not in `--enable-minimal` builds (`core_ed25519.c` and `core_ristretto255.c` sit under `if !MINIMAL` in Makefile.am).

## Cofactor trouble
Ed25519 has cofactor 8. Points outside the prime-order subgroup and the clamping of scalars break naive
protocol designs (key blinding, threshold schemes, OPRFs). Always validate untrusted points with
`is_valid_point`, and prefer `crypto_core_ristretto255_*`, which provides a prime-order group without the cofactor pitfalls.

## Rules
- Use `_noclamp` variants when the protocol works with scalars mod L (clamping changes the scalar).
- Check the return value: per the docs `crypto_scalarmult_ed25519` returns -1 if `n` is 0 or `p` is not on the curve, not on the main subgroup, of small order or not canonical (libsodium.js threw for `n = 0`).
- Do not build signature schemes from these primitives without a specification and review.

## Verify
- [ ] Untrusted inputs pass `is_valid_point` before use; protocol test vectors (e.g. FROST, RFC 9380 suites) match.
