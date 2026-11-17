---
id: computing-software.cryptography-implementation.applied-cryptography.replacing-non-cryptographic-prngs
name: replacing-non-cryptographic-prngs
category: computing-software
field: cryptography-implementation
product: applied-cryptography
tags: [applied-cryptography, cryptography-implementation, insecure-prng, csprng, math-random, java-util-random, python-random, secure-random]
level: practitioner
status: docs-checked
description: "Replace Math.random, java.util.Random, Python random, rand() and similar PRNGs in security code with the CSPRNG APIs OWASP and Python document."
sources: ["https://cheatsheetseries.owasp.org/cheatsheets/Cryptographic_Storage_Cheat_Sheet.html#secure-random-number-generation", "https://docs.python.org/3/library/secrets.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Replacing non-cryptographic PRNGs

PRNGs give low-quality randomness that is much faster and fine for non-security work such as ordering results or
randomizing UI elements. They must not be used for anything security critical, because attackers can often guess or
predict the output. Keys, IVs, session IDs, CSRF tokens and password reset tokens need a CSPRNG.

## Replacement table (OWASP)
| Language | Insecure | Secure |
|---|---|---|
| C | `random()`, `rand()` | `getrandom(2)` |
| Java | `Math.random()`, `StrictMath.random()`, `java.util.Random`, `SplittableRandom`, `ThreadLocalRandom` | `java.security.SecureRandom`, `java.util.UUID.randomUUID()` |
| PHP | `array_rand()`, `lcg_value()`, `mt_rand()`, `rand()`, `uniqid()` | `random_bytes()`, `random_int()` (PHP 7); `Random\Engine\Secure` (PHP 8.2) |
| .NET/C# | `Random()` | `RandomNumberGenerator` |
| Objective-C | `GKRandomSource` subclasses, `rand()`, `random()` | `SecRandomCopyBytes`, the `arc4random` family on current Apple platforms |
| Python | `random()` | `secrets` |
| Ruby | `rand()`, `Random` | `SecureRandom` |
| Node.js | `Math.random()` | `crypto.randomBytes()`, `crypto.randomInt()`, `crypto.randomUUID()` |

## Python secrets
- The `secrets` module is for passwords, account authentication and security tokens; prefer it over the default `random`
  module, which is designed for modelling and simulation, not security.
- `secrets.token_bytes`, `token_hex` and `token_urlsafe` make tokens; `secrets.choice`, `randbelow` and `randbits` pick
  values. Omitting the byte count uses `DEFAULT_ENTROPY`, which may change at any time, even in maintenance releases.
- As of 2015 the docs consider 32 bytes (256 bits) sufficient for typical use; pass an explicit size if you need to control it.
- `secrets.compare_digest` is a constant-time comparison.

## Triage
Search the code for the insecure names in the table. Each hit that feeds a token, key, ID, reset link, CSRF value or
similar is a bug; UI ordering and similar is fine.

## UUIDs
Version 1 UUIDs hold a timestamp and MAC address, so they are not random. Version 4 UUIDs are random, but whether a
CSPRNG is used depends on the implementation; do not rely on that unless it is known to be secure in your language or
framework.

## Checked
Date: 2026-11-09. Read: the OWASP Cryptographic Storage Cheat Sheet (secure random number generation and UUID sections)
and the Python `secrets` documentation. Removed as not confirmed on those pages: the Mersenne Twister, java.util.Random
and V8 state-recovery claims, the Go, libsodium, `BCryptGenRandom` and `arc4random_buf` rows, the `rg` and Semgrep
commands, the modulo-bias and shuffle notes, the "seeding does not help" gotcha and the 128-bit token minimum. The CWE-338 page was not relied on.
Method: docs-checked 2026-11-09 against the OWASP Cryptographic Storage Cheat Sheet and the Python secrets documentation.
