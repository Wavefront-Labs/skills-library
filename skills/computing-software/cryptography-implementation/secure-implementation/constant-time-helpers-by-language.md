---
id: computing-software.cryptography-implementation.secure-implementation.constant-time-helpers-by-language
name: constant-time-helpers-by-language
category: computing-software
field: cryptography-implementation
product: secure-implementation
tags: [secure-implementation, cryptography-implementation, subtle-crate, constant-time, constant-time-compare, crypto-subtle, rust, golang, java, dotnet, python, nodejs]
level: practitioner
status: docs-checked
description: "Use each language's constant-time primitives correctly: Rust subtle crate, Go crypto/subtle, Java MessageDigest.isEqual, .NET FixedTimeEquals, Python, Node, PHP."
sources: ["https://docs.rs/subtle/latest/subtle/", "https://pkg.go.dev/crypto/subtle", "https://learn.microsoft.com/en-us/dotnet/api/system.security.cryptography.cryptographicoperations.fixedtimeequals", "https://docs.python.org/3/library/hmac.html", "https://nodejs.org/api/crypto.html", "https://www.php.net/manual/en/function.hash-equals.php", "https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/security/MessageDigest.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Constant-time helpers by language

| Language | Compare | Select / other |
|---|---|---|
| Rust | `subtle::ConstantTimeEq` trait produces a `Choice` instead of a `bool` | `ConditionallySelectable` trait; `CtOption` instead of `Option` for secret-dependent presence |
| Go | `subtle.ConstantTimeCompare(a, b) == 1` (returns 0 immediately if lengths differ) | `ConstantTimeSelect`, `ConstantTimeByteEq`, `ConstantTimeCopy`, `XORBytes`; Go 1.24+ `subtle.WithDataIndependentTiming(f)` |
| Java | `MessageDigest.isEqual(a, b)` (time depends only on the length of the first argument) | none here |
| .NET | `CryptographicOperations.FixedTimeEquals(a, b)` (time depends on length, not values) | none here |
| Python | `hmac.compare_digest(a, b)` | none here |
| Node | `crypto.timingSafeEqual(a, b)` on equal-length buffers | none here |
| PHP | `hash_equals($known, $user)`; put the user-supplied string second | none here |

## Notes per language

- Rust `subtle` is a "best-effort" crate: its traits are bitwise operations
  that should run in constant time provided the operations are constant-time
  and the compiler does not turn them back into a branch. It tries to stop
  that by passing the inner value of `Choice` through a volatile read. Its
  debug assertions contain secret-dependent branches, so use release builds.
  Keep values as `Choice` through secret-dependent logic and convert to
  `bool` only at the decision point.
- Go `ConstantTimeSelect` and `ConstantTimeCopy` are undefined unless the
  selector `v` is 0 or 1. `WithDataIndependentTiming` only enables CPU
  data-independent-timing features (Arm64 with FEAT_DIT; a no-op elsewhere)
  and does not make variable-time code constant-time; it also covers
  goroutines spawned inside it.
- PHP `hash_equals` returns false immediately for unequal lengths, which can
  leak the length of the known string.
- Python docs recommend `compare_digest` over `==` when checking an HMAC
  digest against an externally supplied one.

## Pitfalls
- Comparing hex or base64 strings is fine with these helpers, but normalise case first (outside the secret path).
- Converting the result into an early `return` inside a loop over secrets reintroduces timing.
- These helpers protect the comparison only; surrounding code (lookups, parsing) must not branch on secrets either.
- For primitives, rely on vetted libraries rather than hand-rolled code.

## Verify
- [ ] Lint rule flags `==` on variables named `*mac*`, `*token*`, `*signature*`, `*hash*`.
- [ ] A statistical timing test on the comparison shows no distinguishable distributions.

## Checked

2026-11-01. Confirmed against the cited pages: docs.rs subtle (traits,
`Choice`, `CtOption`, best-effort caveat, volatile read, debug assertions),
pkg.go.dev crypto/subtle (all listed functions, undefined behaviour, Go 1.24
`WithDataIndependentTiming`, Arm64 FEAT_DIT, no-op elsewhere), MessageDigest
`isEqual` implementation note, .NET FixedTimeEquals description, Python hmac
`compare_digest` recommendation, Node `timingSafeEqual` with equal-length
buffers, PHP `hash_equals` notes. Removed: `ct_eq`/`conditional_select`
method names and the code example, Java BigInteger
claim, `secrets.compare_digest`, `ZeroMemory`, Node throw-on-mismatch,
Ruby, C (libsodium, OpenSSL, BoringSSL) rows, PHP `sodium_memcmp`, dudect name.

Method: documentation only; no commands were run.
