---
id: computing-software.software-engineering.java.securerandom-and-password-hashing
name: securerandom-and-password-hashing
category: computing-software
field: software-engineering
product: java
tags: [java, java-security, securerandom, password-hashing, bcrypt, argon2, pbkdf2, constant-time-compare]
level: practitioner
status: docs-checked
description: "Generate tokens with SecureRandom, hash passwords with Argon2id/bcrypt/PBKDF2 at OWASP minimums, compare digests with MessageDigest.isEqual, and use Spring's delegating encoder."
sources: ["https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/security/SecureRandom.html", "https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/security/MessageDigest.html", "https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html", "https://docs.spring.io/spring-security/reference/features/authentication/password-storage.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SecureRandom and password hashing

## Randomness
```java
private static final SecureRandom RNG = new SecureRandom();   // safe for use by multiple threads; reuse it
byte[] tok = new byte[32];
RNG.nextBytes(tok);                                            // 256 bits of random data
```
- `SecureRandom` output must be non-deterministic and cryptographically strong; any seed material passed in must be unpredictable. A new PRNG instance seeds itself from an implementation-specific entropy source on the first `nextBytes`, and that self-seeding does not happen if `setSeed` was called first, so do not seed it manually.
- Depending on the implementation, `generateSeed`, `reseed` and `nextBytes` may block while entropy is gathered (the Javadoc's example is `/dev/random` on Unix-like systems).
- `SecureRandom.getInstance("NativePRNG")` selects an algorithm explicitly; `SecureRandom.getInstanceStrong()` returns the configured strongest instance. Use the default constructor unless you have a reason to name an algorithm.

## Passwords (OWASP Password Storage Cheat Sheet)
Use a modern adaptive hash, not encryption and not a fast hash such as MD5 or SHA-1.
| Algorithm | OWASP guidance |
|---|---|
| Argon2id | first choice: at least 19 MiB memory (m=19456), 2 iterations, parallelism 1 |
| scrypt | if Argon2id is unavailable: cost parameter at least 2^17, block size 8, parallelism 1 |
| bcrypt | legacy systems only; work factor at least 10; maximum input 72 bytes, so enforce a 72-byte maximum password length |
| PBKDF2 | when FIPS-140 compliance is required; HMAC-SHA-256 with 600,000 iterations |

- Salts must be unique per password; the cheat sheet notes that most libraries generate and manage salts internally. The work factor is typically stored in the hash output, and raising it over time is supported.
- A pepper is an optional extra: a secret shared between passwords, stored separately from the database (for example in a secrets vault or HSM), not stored with the hash.
- Choose the work factor by measurement on your server; as a general rule one hash should take under one second.

Spring Security's delegating encoder keeps old hashes verifiable while new ones use the current default:
```java
PasswordEncoder enc = PasswordEncoderFactories.createDelegatingPasswordEncoder();
String stored = enc.encode(raw);          // result is prefixed with {bcrypt}
boolean ok = enc.matches(raw, stored);    // dispatches on the {id} prefix
```
`matches` with an id that is not mapped throws `IllegalArgumentException` unless a default is set with `setDefaultPasswordEncoderForMatches`. The same page lists `Argon2PasswordEncoder` and `Pbkdf2PasswordEncoder`.

## Comparing secrets
`MessageDigest.isEqual(a, b)` examines all bytes of the first array, and its running time depends only on the length of `digesta`, not on the contents of either array or the length of `digestb`. Prefer it over `Arrays.equals` when comparing digests.

## Verify
Unit-test that two hashes of the same password differ and `matches` is true; check your parameters against the current OWASP cheat sheet.

## Checked
2026-11-03. Confirmed against SecureRandom and MessageDigest Javadoc (Java SE 21), the OWASP Password Storage Cheat Sheet and the Spring Security password storage page: thread safety, self-seeding, blocking note, NativePRNG/getInstanceStrong, Argon2id/scrypt/bcrypt/PBKDF2 parameters, 72-byte bcrypt limit, salts, pepper, work-factor timing rule, delegating encoder behaviour, isEqual timing note.
Removed (not in the pages read): `/dev/urandom` and "does not block on modern JDKs", claims about `java.util.Random`, `ThreadLocalRandom`, `SplittableRandom`, `RandomGenerator`, Base64 token encoding, "JDK 6u17", the `PBKDF2WithHmacSHA256` factory call, a 16-byte salt size, bcrypt work factor 12, `upgradeEncoding`, `char[]` zeroing and rate-limiting advice.
Method: documentation only; no commands were run.
