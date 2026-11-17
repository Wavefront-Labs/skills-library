---
id: computing-software.cybersecurity-defensive.security-architecture.password-hashing-storage
name: password-hashing-storage
category: computing-software
field: cybersecurity-defensive
product: security-architecture
tags: [cryptography, password-hashing, argon2id, bcrypt, scrypt, pbkdf2, salting, key-stretching, pepper, credential-storage]
level: practitioner
status: docs-checked
description: "Store passwords with a slow salted hash (Argon2id, scrypt, bcrypt, PBKDF2) with correct parameters, migrate legacy hashes and avoid common mistakes."
sources:
  - https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html
  - https://www.rfc-editor.org/rfc/rfc9106.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Password hashing and storage

**Goal:** if the user database leaks, cracking passwords is too slow to be worthwhile for
most accounts.

## Choose an algorithm (OWASP current guidance)
| Algorithm | Minimum parameters |
|---|---|
| Argon2id (preferred) | any of: m=46 MiB (47104 KiB), t=1, p=1; m=19 MiB (19456 KiB), t=2, p=1; m=12 MiB, t=3, p=1; m=9 MiB, t=4, p=1; m=7 MiB, t=5, p=1 |
| scrypt | N=2^17 (128 MiB), r=8, p=1 (other trade-offs listed by OWASP) |
| bcrypt (legacy systems) | work factor 10 or more; input limited to 72 bytes |
| PBKDF2 (FIPS-140 required) | PBKDF2-HMAC-SHA256 with 600,000 iterations (SHA-512: 220,000) |
Argon2id has three cost parameters: memory in KiB (m), passes (t) and parallelism (p). Increasing p does not multiply memory or act as an iteration count. Benchmark the chosen parameters on the target system and balance security against login latency.

## Rules
- Unique random salt per password. Libraries generate and manage it automatically; never use one global salt.
- Optional **pepper** for defence in depth: a secret shared across passwords, stored separately from the database (secrets vault or HSM), never next to the hash. Either add it before hashing, or HMAC the finished hash with it (post-hashing). Changing a pepper means forcing affected users to reset passwords.
- Hashes must be slow and salted; fast hashes can be attacked cheaply on GPUs and cloud servers.
- Prefer a library's encoded string, which keeps the work factor with the hash so it can be raised later.

## Migrating legacy hashes
Two documented methods: expire and delete the hashes of long-inactive users and require a reset (secure but unfriendly), or layer, for example `bcrypt(md5(password))` over existing hashes so nobody waits. Replace layered hashes with a direct hash of the password at next login. Layering can make hashes easier to crack than a direct hash.

## Gotchas
- bcrypt takes at most 72 bytes in most implementations: enforce that limit. If pre-hashing, encode the hash with base64 to avoid null bytes, and use a pepper (for example HMAC-SHA384 keyed with the pepper) to defeat password shucking; plain `bcrypt(base64(sha512(password)))` is dangerous.
- A work factor that is too high can be abused for denial of service by many login attempts exhausting server CPU: balance it.
- The hashing library must accept all Unicode code points and passwords containing NUL bytes, without reducing entropy before hashing.

## Verify
- [ ] Database contains only encoded Argon2id/scrypt/bcrypt/PBKDF2 hashes (no legacy formats after migration window).
- [ ] Hash time measured on production hardware within target.

## Checked
Confirmed against the OWASP Password Storage Cheat Sheet (raw Markdown, read for the algorithm settings, salting, peppering, work factor, bcrypt, PBKDF2 and legacy upgrade sections): all parameter sets, bcrypt 72-byte limit and pre-hashing advice, PBKDF2 iteration counts, pepper rules, upgrade methods, DoS note, Unicode/NUL note. RFC 9106 is cited by OWASP for the Argon2 parameter definitions (m, t, p). Removed: the Python argon2-cffi example and its claim that defaults meet OWASP minimums, the 500 ms latency figure, "never encrypt passwords reversibly", "constant-time comparison", the MFA and breached-password remark, and the NIST SP 800-63B citation (not read in this batch).
Method: docs-checked 2026-11-09 against the OWASP Password Storage Cheat Sheet and the Argon2 RFC 9106 pointers within it.
