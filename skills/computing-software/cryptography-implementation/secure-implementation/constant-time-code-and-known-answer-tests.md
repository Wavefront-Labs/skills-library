---
id: computing-software.cryptography-implementation.secure-implementation.constant-time-code-and-known-answer-tests
name: constant-time-code-and-known-answer-tests
category: computing-software
field: cryptography-implementation
product: secure-implementation
tags: [cryptography-implementation, secure-implementation, constant-time, timing-attack, side-channel, compare-digest, timingsafeequal, constanttimecompare, crypto-memcmp, sodium-memcmp, dudect, ctgrind, valgrind, timecop, known-answer-tests, kat, test-vectors, nist-cavp, acvp, wycheproof, padding-oracle, error-oracle, fuzzing, cryptofuzz, zeroization, invalid-curve-attack, point-validation, constant-time-compare]
level: advanced
status: draft
description: "Side-channel-safe crypto code: constant-time comparison per language, branch and table leaks, dudect/ctgrind checks, KAT and Wycheproof vectors, uniform errors, point validation."
sources: ["https://github.com/C2SP/wycheproof", "https://csrc.nist.gov/projects/cryptographic-algorithm-validation-program", "https://github.com/oreparaz/dudect", "https://github.com/agl/ctgrind", "https://github.com/guidovranken/cryptofuzz"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Constant-time code and known-answer tests

**Goal:** make code that handles secrets leak nothing through timing or error
behaviour, and prove the arithmetic is right with published test vectors.

## 1. Compare secrets in constant time
Any check of a MAC, token, password hash or API key must not exit early.

| Language | Use | Note |
|---|---|---|
| Python | `hmac.compare_digest(a, b)` | bytes or ASCII str |
| Node | `crypto.timingSafeEqual(a, b)` | **throws** on length mismatch; check length first or compare fixed-length HMACs |
| Go | `subtle.ConstantTimeCompare(a, b) == 1` | returns 0 at once if lengths differ (length is not secret) |
| Java | `MessageDigest.isEqual(a, b)` | constant-time in modern JDKs |
| .NET | `CryptographicOperations.FixedTimeEquals` | |
| C (OpenSSL) | `CRYPTO_memcmp(a, b, n)` | 0 = equal |
| C (libsodium) | `sodium_memcmp(a, b, n)` | 0 = equal, -1 otherwise |
| Rust | `subtle::ConstantTimeEq` | |

Never use `==`, `memcmp` or `Arrays.equals`. For variable-length values, compare
fixed-length `HMAC(k, x)` digests.

## 2. What else leaks
- **Secret-dependent branches** (`if (bit) ...`) and loop counts that depend on secret values.
- **Secret-dependent memory addresses:** table lookups (classic AES T-tables, S-box
  arrays) leak through the cache. Use bitsliced or hardware (AES-NI/ARMv8) implementations.
- **Variable-time instructions:** integer division and modulo; on some older CPUs,
  multiplication. Some CPUs offer a data-independent-timing mode (Arm DIT, Intel
  DOIT). Whether you must enable it depends on the CPU and OS; check.
- **Early returns** in decoding, padding checks and point decompression.

Constant-time select idiom:
```c
uint32_t mask = (uint32_t)0 - (uint32_t)(bit & 1);   /* 0x00000000 or 0xFFFFFFFF */
r = (a & mask) | (b & ~mask);
```
**Compiler gotcha:** optimisers can turn mask arithmetic back into branches, or
remove a `memset` they consider dead. Use value barriers
(`__asm__ volatile("" : "+r"(x))` on GCC/Clang), check the generated assembly at
the optimisation level you ship, and re-test after compiler upgrades.

## 3. Test for timing leaks
- **ctgrind / timecop trick (Valgrind memcheck):** mark secret buffers as
  uninitialised with `VALGRIND_MAKE_MEM_UNDEFINED(key, len)`, then run under
  `valgrind --track-origins=yes`. Each "conditional jump depends on uninitialised
  value" or "use of uninitialised value" in an address calculation is a
  secret-dependent branch or lookup. Mark outputs defined again
  (`VALGRIND_MAKE_MEM_DEFINED`) once they are public. This finds structural leaks
  deterministically.
- **dudect:** statistically compares timing distributions for two input classes
  (fixed vs. random) with Welch's t-test. Run many measurements on a quiet machine;
  |t| above about 4.5 is the usual leak signal. A negative result is evidence, not
  proof.

## 4. Known-answer tests
- Run official vectors in CI for every primitive you implement or wrap: RFC appendix
  vectors (RFC 8439 for ChaCha20-Poly1305, RFC 7748 for X25519, RFC 8032 for Ed25519,
  RFC 5869 for HKDF), and NIST CAVP response files (`.rsp`, now served under ACVP)
  for AES modes and SHA.
- **Project Wycheproof** (now maintained under C2SP) provides JSON vectors for edge
  cases: invalid curve points, signature malleability, wrong tag lengths, bad
  padding. Each case carries `valid`/`invalid`/`acceptable`. Fail the test if any
  `invalid` case is accepted.
- Also test wrong key, wrong AAD, a flipped tag bit and truncated input.

## 5. Uniform errors (no oracles)
- Padding-oracle (Vaudenay) and Bleichenbacher attacks need only *one bit* of
  difference: a distinct error message, status code or timing.
- Verify the MAC/tag **before** any decryption or parsing. Return one generic
  "decryption failed" with the same timing; details go to server logs only.
- For RSA PKCS#1 v1.5 decryption that you cannot remove, use implicit rejection:
  continue with a random key instead of failing.

## 6. Fuzzing
libFuzzer or AFL++ on every parser (DER, PEM, wire formats, point decoding).
**Differential fuzzing** against a reference library (cryptofuzz runs many libraries
side by side) catches wrong arithmetic that no crash would reveal.

## 7. Zeroise and validate
- Wipe keys with `explicit_bzero`, `memset_s`, `OPENSSL_cleanse` or `sodium_memzero`,
  or Rust's `zeroize`. A plain `memset` before `free` is often optimised away. In GC languages wiping
  is best-effort; hold secrets in byte arrays, not strings.
- **Validate public points** from peers: on the curve, not the identity, in the
  prime-order subgroup. Skipping this allows invalid-curve attacks on ECDH (P-256 and
  similar). For X25519, reject an all-zero
  shared secret if your protocol needs contributory behaviour.

## Verify
- [ ] No `==`/`memcmp` on secret material (grep plus review).
- [ ] The ctgrind-style Valgrind run reports no secret-dependent branches in the hot paths.
- [ ] dudect runs on comparison and decryption functions without |t| > 4.5.
- [ ] RFC/CAVP and Wycheproof vectors run in CI, and every `invalid` case is rejected.
- [ ] Every decryption failure produces the same error and timing.
- [ ] Peer public keys are validated before use, and secrets are wiped after use.
