---
id: computing-software.cryptography-implementation.applied-cryptography.bcrypt-cost-and-72-byte-limit
name: bcrypt-cost-and-72-byte-limit
category: computing-software
field: cryptography-implementation
product: applied-cryptography
tags: [cryptography-implementation, applied-cryptography, password-hashing, bcrypt, bcrypt-limits, cost-factor, password-truncation, prehashing, pepper]
level: practitioner
status: verified
description: "Run bcrypt safely: choosing the cost factor, the 72-byte input limit and NUL issues, safe prehashing, $2a/$2b/$2y prefixes and rehash on login."
sources: ["https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html#bcrypt", "https://pkg.go.dev/golang.org/x/crypto/bcrypt", "https://trust.okta.com/security-advisories/okta-ad-ldap-delegated-authentication-username/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# bcrypt cost factor and the 72-byte limit

bcrypt is still acceptable for passwords where Argon2id is unavailable. Two
things go wrong in practice: a cost that is too low, and its input limit.

## Cost factor

- Cost is log2 of the work: cost 12 is twice cost 11. OWASP: "as large as verification server performance will allow, with a
  minimum of 10". Cost 10/12/14 took 0.05/0.19/0.75 s here (pyca bcrypt 5.0.0,
  one machine; benchmark yours). Benchmark: pick the highest cost that
  keeps hashing under your latency target on production hardware.
- The cost is stored in the hash (`$2b$12$...`). Raise it over time and
  rehash on successful login when the stored cost is lower.

## The 72-byte limit

bcrypt uses at most the first 72 bytes of input. Bytes after that are
silently ignored by many implementations, so:

- Long passphrases that share a 72-byte prefix are equivalent.
- Using bcrypt as a generic hash over `user_id + username + password` lets a
  long username push the password beyond byte 72. Okta's 2024 AD/LDAP
  delegated-auth advisory was exactly this: a cache key generated with bcrypt
  over userId, username and password allowed login without the correct
  password when the username was 52 characters or longer (introduced 23 July
  2024, fixed 30 October 2024 by moving to PBKDF2).
- Go's `golang.org/x/crypto/bcrypt` returns `ErrPasswordTooLong` for > 72
  bytes (run on v0.58.0); pyca `bcrypt` 5.0.0 raises `ValueError` ("password
  cannot be longer than 72 bytes"). Both were run with 73+ byte input.
  Check your library's behaviour.

UTF-8 means 72 bytes can be fewer than 72 characters.

## Options for long inputs

1. Enforce a 72-byte maximum and tell users (simple, honest).
2. Prehash: `bcrypt(base64(HMAC-SHA-256(pepper, password)))`. Base64 avoids
   NUL bytes (OWASP: the original bcrypt reads a null-terminated string;
   Go and pyca bcrypt both treat an embedded NUL as ordinary input in my
   run). Use HMAC with a secret key, not plain SHA-256, to avoid "password
   shucking" with leaked unsalted hash lists; OWASP warns prehashing "can be
   dangerous" and suggests HMAC-SHA-384 keyed with a pepper, base64-encoded.
3. Prefer Argon2id for new systems.

## Prefixes

`$2a$`, `$2b$`, `$2y$` are variants from historic bugs; modern libraries
verify all. pyca `bcrypt` 5.0.0 produces `$2b$`, Go's x/crypto produces
`$2a$` (both run). Do not rewrite prefixes by hand.

## Verify

- [ ] Test: two passwords differing only after byte 72 do not both verify (or are rejected).
- [ ] bcrypt is never used to hash concatenated identifiers.
- [ ] Cost recorded and rehash-on-login in place.
