---
id: computing-software.cryptography-implementation.applied-cryptography.pbkdf2-iteration-counts-for-fips
name: pbkdf2-iteration-counts-for-fips
category: computing-software
field: cryptography-implementation
product: applied-cryptography
tags: [cryptography-implementation, applied-cryptography, password-hashing, pbkdf2, pbkdf2-iterations, fips-140, sp-800-132, owasp, password-storage]
level: practitioner
status: verified
description: "Use PBKDF2 when FIPS 140 rules out Argon2: OWASP iteration counts per hash, SP 800-132 salt rules, OpenSSL FIPS provider checks, and stored formats."
sources: ["https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html#pbkdf2", "https://csrc.nist.gov/pubs/sp/800/132/final", "https://docs.openssl.org/3.0/man7/EVP_KDF-PBKDF2/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# PBKDF2 iteration counts for FIPS environments

PBKDF2 is the password KDF approved in FIPS 140 modules (SP 800-132). It is
not memory-hard, so iterations must be high.

## Iterations (OWASP Password Storage Cheat Sheet)

| PRF | Minimum iterations |
|---|---|
| HMAC-SHA-256 | 600,000 |
| HMAC-SHA-512 | 220,000 |
| HMAC-SHA-1 (legacy only) | 1,400,000 |

Raise them as hardware allows; frameworks bump defaults each release
(Django, for example). Benchmark on production hardware and keep the hash
time within your login latency budget.

## SP 800-132 rules

- Salt: the random portion at least 128 bits, from an approved RBG (section 5.1).
- Derived key length at least 112 bits (section 5).
- Iteration count "as large as possible" while acceptable to users; a minimum
  of 1,000 is recommended and 10,000,000 may suit critical keys on powerful
  systems (section 5.2). 1,000 is far too low for passwords today.

OpenSSL 3 PBKDF2 has a `pkcs5` parameter: 0 enables the SP 800-132 checks
(iterations >= 1000, salt >= 128 bits, key >= 112 bits), 1 disables them. The
FIPS provider defaults to 0, the default provider to 1.

## Store the parameters

```
pbkdf2_sha256$600000$<base64 salt>$<base64 hash>
```

Store algorithm, iterations and salt with each hash so you can raise the
count and rehash on next login.

```python
import hashlib, os, hmac
salt = os.urandom(16)
dk = hashlib.pbkdf2_hmac("sha256", pw.encode(), salt, 600_000, dklen=32)
hmac.compare_digest(dk, stored_dk)
```

Java and .NET expose the same function (`SecretKeyFactory` "PBKDF2WithHmacSHA256",
`Rfc2898DeriveBytes.Pbkdf2`); check their docs for the call, not run here.
Python above: 600,000 iterations of SHA-256 took 0.23 s on the test PC; RFC 6070 vector 2 passes.

## Pitfalls

- Using PBKDF2 output longer than the hash length multiplies defender cost
  but not attacker cost (attacker computes only the first block; run: the
  first 32 bytes of a 64-byte output equal the 32-byte output).
- HMAC-SHA-1 PBKDF2 with low counts in old data: migrate.

## Verify

- [ ] Iterations meet the table; benchmark recorded.
- [ ] dkLen <= hash output length; salt 16 bytes random.
