---
id: computing-software.cryptography-implementation.applied-cryptography.limiting-password-hashing-dos
name: limiting-password-hashing-dos
category: computing-software
field: cryptography-implementation
product: applied-cryptography
tags: [applied-cryptography, cryptography-implementation, password-hash-dos, denial-of-service, argon2id, bcrypt, pbkdf2, work-factor, password-length-limit]
level: practitioner
status: docs-checked
description: "Keep slow password hashes from becoming a DoS vector: work factor sizing, bcrypt 72-byte limit and safe pre-hashing, and PBKDF2 long-password cost."
sources: ["https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Limiting password hashing DoS

Slow hashes are deliberately expensive. The OWASP Password Storage Cheat Sheet warns that if the work factor is too high,
application performance may degrade, and an attacker could exploit that for denial of service by exhausting the server CPU with
a large number of login attempts.

## Work factor
- There is no golden rule for the right work factor: it depends on the server's performance and the number of users;
  determine it by experimentation on the servers in use. As a general rule, calculating a hash should take less than one
  second.
- Argon2id minimum configurations listed by OWASP (equal defence, trading CPU for RAM): m=47104 KiB t=1 p=1; m=19456 t=2 p=1;
  m=12288 t=3 p=1; m=9216 t=4 p=1; m=7168 t=5 p=1. Benchmark on the target system under expected load.
- Work factors can be raised over time; the common approach is to re-hash at the user's next successful login.

## bcrypt input limit
- bcrypt has a maximum input length of 72 bytes in most implementations, so enforce a maximum password length of 72 bytes (or
  less if the implementation has a smaller limit). OWASP recommends bcrypt only for legacy systems, with a work factor of at
  least 10.
- Pre-hashing before bcrypt is possible but risky: the hash output may contain null bytes, and bcrypt reads a
  null-terminated string (so `H($password)` with a leading zero byte collides with the empty password); encode the hash as
  printable text such as base64. Pre-hashing with a bare hash also allows password shucking against leaked hashes.
- OWASP's summary for pre-hashing is `bcrypt(base64(hmac-sha384(data: $password, key: $pepper)), $salt, $cost)`, with the
  pepper stored outside the database.

## PBKDF2 and long passwords
When PBKDF2 uses an HMAC and the password is longer than the hash function's block size (64 bytes for SHA-256), it is
automatically pre-hashed. Good implementations do this once before the iterated phase, but some do it on every iteration,
which makes hashing long passwords significantly more expensive than short ones. With very long user-supplied passwords that
can cause denial of service, as in the Django vulnerability published in 2013. Manual pre-hashing reduces the risk but
needs a salt in the pre-hash step.

## Other
- Hashing libraries should accept all Unicode code points and input containing a null byte, without reducing entropy before
  hashing.

## Verify
- [ ] Measured hash time on production hardware is under about one second at the chosen parameters.
- [ ] bcrypt deployments enforce the 72-byte maximum, or pre-hash with a base64-encoded HMAC.

## Checked
Date: 2026-11-09. Read in full: OWASP Password Storage Cheat Sheet. The Django 2013 weblog post and NIST SP 800-63B-4 were
not fetched and were dropped. Removed as not on the cheat sheet: the NIST 64-character minimum and a 1-4 KiB cap, the
CVE number, concurrency semaphores and 429 handling, rate limiting and CAPTCHA, dummy hashing for unknown users, dedicated
login worker pools, and the container OOM and event-loop gotchas.
Method: docs-checked 2026-11-09 against the OWASP Password Storage Cheat Sheet.
