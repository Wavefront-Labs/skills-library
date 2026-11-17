---
id: computing-software.cryptography-implementation.secure-implementation.injecting-deterministic-rngs-in-tests
name: injecting-deterministic-rngs-in-tests
category: computing-software
field: cryptography-implementation
product: secure-implementation
tags: [secure-implementation, cryptography-implementation, deterministic-test-rng, testing, known-answer-tests, drbg, dependency-injection, crypto-testing]
level: practitioner
status: verified
description: "Inject deterministic RNGs into crypto tests to reproduce known-answer vectors: test-only seams, seeded DRBGs, guarding against production use, and library hooks."
sources: ["https://pkg.go.dev/crypto/rand", "https://docs.rs/rand_chacha/latest/rand_chacha/", "https://github.com/C2SP/CCTV"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Injecting deterministic RNGs in tests

Randomised algorithms (ECDSA without RFC 6979, RSA-PSS, ML-KEM encapsulation, key generation) need fixed
randomness to compare against test vectors.

## Patterns
- **Explicit RNG parameter**: Go APIs take `io.Reader` (`ecdsa.GenerateKey(curve, rand)`); Rust `rand_core`
  traits (`&mut impl CryptoRng` in rand_core 0.10, where `CryptoRngCore` no longer exists; it was the name in 0.6; compiled with rand_chacha 0.10). Pass a seeded `ChaCha20Rng::from_seed(seed)` in tests only.
- **Internal deterministic functions**: expose `KeyGen_internal(d, z)` style functions (FIPS 203/204 define them)
  behind a test-only build tag or feature flag; public API draws its own randomness.
- **Vector-driven reader**: a reader that returns exactly the bytes from the test vector and fails if asked for
  more, catching changes in how much randomness the code consumes.

## Guard production
- Feature gate: `#[cfg(test)]` / `//go:build testvectors` / separate test module. Never a runtime flag.
- Since Go 1.26 (not 1.24; the 1.24 and 1.25 release notes do not mention it) `crypto/ecdsa` (`GenerateKey`, `Sign`, `SignASN1`), `crypto/ecdh` `GenerateKey` and `crypto/dsa` ignore the caller's `rand` argument and always use system randomness; use `testing/cryptotest.SetGlobalRandom` for deterministic tests, or `GODEBUG=cryptocustomrand=1` to temporarily restore the old behaviour (go.dev/doc/go1.26).
- Lint for imports of the deterministic RNG outside tests.

## Accumulated tests
For algorithms with internal randomness consumption, CCTV-style "accumulated" vectors (the C2SP CCTV repository has ML-KEM and ML-DSA directories) run thousands of
deterministic iterations seeded from SHAKE and compare a final hash, catching subtle divergence fast.

## Verify
- [ ] Production binary does not contain the deterministic RNG symbol; KAT tests fail if randomness consumption changes.
