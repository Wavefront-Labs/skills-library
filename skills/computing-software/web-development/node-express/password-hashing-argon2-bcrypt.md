---
id: computing-software.web-development.node-express.password-hashing-argon2-bcrypt
name: password-hashing-argon2-bcrypt
category: computing-software
field: web-development
product: node-express
tags: [authentication-failures, web-authentication, password-hashing, argon2, argon2id, bcrypt, breached-passwords, pwned-passwords, rehash-on-login]
level: practitioner
status: verified
description: "Storing passwords with argon2id or bcrypt at tuned cost, NIST 800-63B rules, breached-password checks via k-anonymity, and transparent rehash on login."
sources:
  - https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html
  - https://pages.nist.gov/800-63-4/sp800-63b.html
  - https://haveibeenpwned.com/API/v3#PwnedPasswords
  - https://github.com/ranisalt/node-argon2
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Password hashing (argon2id / bcrypt)

**Goal:** a database leak doesn't turn into cracked passwords, and password rules stop weak/breached passwords without annoying users.

## 1. Algorithm and parameters (OWASP cheat sheet)
- **argon2id**: m=19 MiB, t=2, p=1 minimum (or m=46 MiB, t=1). Tune so a hash takes ~100-500 ms on your servers under expected login load.
- **bcrypt**: cost 10+ (12 common); bcrypt **truncates input at 72 bytes** (bcryptjs 3 silently ignored byte 73 onwards: two 73-byte passwords differing only in the last byte compared equal) - enforce a max length of 72 bytes or pre-hash carefully (OWASP: `bcrypt(base64(hmac-sha384(password, pepper)))` with the pepper outside the database; never raw binary, which may contain NULs).
- scrypt (N=2^17, r=8, p=1) or PBKDF2-HMAC-SHA256 (600 000 iterations) when FIPS is required.
- Never: MD5/SHA-1/SHA-256 alone, unsalted hashes, encryption of passwords.

```js
import argon2 from 'argon2';
const opts = { type: argon2.argon2id, memoryCost: 19456, timeCost: 2, parallelism: 1 };   // memoryCost is in KiB
const hash = await argon2.hash(pw, opts);
const ok = await argon2.verify(hash, pw);                    // constant-time; salt+params are in the PHC string
if (ok && argon2.needsRehash(hash, opts)) await saveHash(user, await argon2.hash(pw, opts));
```
Django: `PASSWORD_HASHERS` with `Argon2PasswordHasher` first (needs `argon2-cffi`) - upgrades on login automatically. Rails: `has_secure_password` (bcrypt, cost via `BCrypt::Engine.cost`).

## 2. Password rules (NIST SP 800-63B)
- NIST SP 800-63B-4: SHALL require at least 15 characters for single-factor passwords (8 minimum when used only inside MFA); SHOULD permit a maximum length of at least 64, accept printing ASCII, space and Unicode, and permit paste. SHALL NOT impose composition rules or periodic rotation.
- Rotate only on evidence of compromise.
- **Block known-breached passwords**: HIBP Pwned Passwords range API - send the first 5 hex chars of SHA-1, compare suffixes locally (k-anonymity); add `Add-Padding: true` (padded responses contain extra entries with count `:0`; checked live: 5-char prefix `CBFDA` returned the `password123` suffix with a count in the millions).
- Show a strength meter (zxcvbn) rather than rules.

## 3. Operational
- Hashing is CPU/memory heavy: rate-limit login and registration to avoid self-DoS, and run verification even for unknown users (dummy hash) to keep timing equal.
- Migrating legacy hashes: wrap (`argon2(md5hash)`) for all rows now, then rehash plain on next login.

## Verify
- [ ] Stored values look like `$argon2id$v=19$m=19456,t=2,p=1$…` (checked with `@node-rs/argon2` using the same parameters; the native `argon2` package would not build on this Windows host, so its calls are checked against its published typings: `hash`, `verify`, `needsRehash`, `argon2id`, `memoryCost` default 65536 KiB).
- [ ] Login p95 latency acceptable at peak; hashing time measured.
- [ ] `password123` and a known breached password are refused at sign-up.
