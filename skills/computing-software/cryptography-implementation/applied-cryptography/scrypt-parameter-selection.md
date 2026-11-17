---
id: computing-software.cryptography-implementation.applied-cryptography.scrypt-parameter-selection
name: scrypt-parameter-selection
category: computing-software
field: cryptography-implementation
product: applied-cryptography
tags: [applied-cryptography, cryptography-implementation, scrypt-parameters, scrypt, rfc-7914, password-hashing, memory-hard, kdf, owasp]
level: practitioner
status: verified
description: "Choose scrypt N, r, p from memory and latency budgets, avoid library maxmem errors, and encode parameters for future upgrades."
sources: ["https://www.rfc-editor.org/rfc/rfc7914", "https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html", "https://docs.python.org/3/library/hashlib.html#hashlib.scrypt"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# scrypt parameter selection

## Parameters
- **N** (CPU/memory cost, power of two), **r** (block size, usually 8), **p** (parallelism).
- Memory used is about `128 * N * r` bytes; time scales with `N * r * p`.
- OWASP minimum for password storage: N=2^17, r=8, p=1 (128 MiB). Lower-memory equivalents: N=2^16, r=8, p=2;
  N=2^15, r=8, p=3; N=2^14, p=5; N=2^13, p=10 (all r=8). Prefer Argon2id for new systems; use scrypt where it is already standard or Argon2 is missing.

## Tune on production hardware
```python
import hashlib, os, time
salt = os.urandom(16)
for logN in (14, 15, 16, 17):
    t = time.perf_counter()
    hashlib.scrypt(b"pw", salt=salt, n=2**logN, r=8, p=1, maxmem=2**28, dklen=32)
    print(logN, round(time.perf_counter() - t, 3))
```
Pick the largest N that keeps a login under your latency budget (often 100-500 ms) at peak concurrency.

## Library limits
- Python `hashlib.scrypt` (maxmem 0 means the OpenSSL default of 32 MiB): N=2^14, r=8 works, N=2^15, r=8
  raises `ValueError: [digital envelope routines] memory limit exceeded` unless you pass `maxmem` (run).
- Node `crypto.scrypt`/`scryptSync` behaves the same: N=2^14 ok, N=2^15 throws `memory limit exceeded`,
  fine with `{N, r, p, maxmem: 2**28}` (run).
- OpenSSL: `openssl kdf -keylen 32 -kdfopt n:131072 -kdfopt r:8 -kdfopt p:1 -kdfopt maxmem_bytes:268435456 -kdfopt pass:pw -kdfopt salt:salt SCRYPT`
  works on 3.2.3; without `maxmem_bytes` it fails with `memory limit exceeded`.
- libsodium `crypto_pwhash_scryptsalsa208sha256` takes opslimit/memlimit instead of N/r/p.

## Storage format
Store algorithm, parameters and salt with the hash, e.g. `$scrypt$ln=17,r=8,p=1$<salt b64>$<hash b64>` (PHC style),
so you can raise N later and rehash on next login.

## Gotchas
- Increasing p multiplies CPU time without raising memory; attackers parallelise across guesses anyway.
- Memory-hard settings need a concurrency cap on login endpoints, or a burst of logins exhausts RAM.
- OWASP: where FIPS-140 validated implementations are required, prefer PBKDF2; scrypt is not the FIPS route.

## Verify
- [ ] RFC 7914 section 12 test vectors pass in your binding (the first two, empty password N=16 r=1 p=1 and
  "password"/"NaCl" N=1024 r=8 p=16, pass in Python `hashlib.scrypt`).
- Timing here (one PC): N=2^14 0.04 s, 2^15 0.08 s, 2^16 0.17 s, 2^17 0.34 s at r=8, p=1.
- [ ] Measured latency at p99 under load is within budget.
- [ ] Stored hashes carry parameters; rehash-on-login upgrades old ones.
